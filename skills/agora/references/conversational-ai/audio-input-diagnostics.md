# ConvoAI Audio Input Diagnostics

Load this file when VAD, turn detection, interruption (barge-in), or multi-turn behavior is unreliable — especially when the user's audio comes from custom capture code, embedded hardware, Linux/ALSA, or any SDK path that pushes raw PCM.

> **RULE:** Verify the input audio before tuning ConvoAI parameters. VAD, ASR, end-of-turn detection, and interruption all assume the PCM they receive matches its declared sample rate, channel count, and real-time cadence. If the input is wrong, no VAD or turn-detection setting will fix it. Do not recommend changing VAD thresholds, silence durations, or interruption settings until the checks below pass.

## Symptoms That Point Upstream

These symptoms usually mean the agent receives mistimed, malformed, or echo-contaminated audio — not that ConvoAI's VAD is misconfigured:

| Symptom | Likely cause to check first |
|---|---|
| First question works, later questions are ignored | Capture rate or format changed mid-session (often after playback starts, stops, or restarts) |
| Agent answers an earlier question instead of the latest one | Audio arriving late, in bursts, or faster than real time |
| Interruption works sometimes, or only at session start | Cadence drift around playback restart; echo of the agent's own voice |
| Agent interrupts itself or reacts to its own speech | No echo cancellation on the device — the mic hears the speaker |
| Transcripts are garbled, sped up, slowed down, or pitch-shifted | Declared sample rate or channel count does not match the actual PCM |
| RTC connection and mic capture look healthy, but conversation is unreliable | Any of the above — a healthy connection does not prove correctly timed audio |

## Diagnostic Order

Work through these in order. Stop at the first failure and fix it before moving on.

### 1. Confirm the agent can hear the user at all

- The user's RTC UID is covered by the agent's `remote_rtc_uids` (`["*"]` or the exact string UID).
- The device publishes an audio track in the same channel the agent joined.
- Wait for the agent's RTC `user-joined` event before testing speech; `/join` success alone does not mean the agent is in the channel.

### 2. Measure actual throughput against the declared format

Log, once per second, from the code that hands PCM to the Agora SDK:

- frames sent per second
- samples per channel sent per second
- the sample rate and channel count declared on each send call

Expected values follow from the frame size your SDK path uses. The Server Gateway (Linux) `sendAudioPcmData` takes `samples_per_channel` as the number of samples **in 10 ms** per channel, so that path always runs at 100 frames/s. Other paths (native custom audio tracks, device SDKs) may use other frame durations; compute the expectation from the duration your code actually sends.

```text
samples_per_frame = sample_rate × frame_duration_seconds
frames_per_second = 1 / frame_duration_seconds
bytes_per_frame   = samples_per_frame × channels × bytes_per_sample   (16-bit PCM → 2)

16 kHz, 10 ms frames → 160 samples/frame, 100 frames/s, 16,000 samples/s
16 kHz, 20 ms frames → 320 samples/frame,  50 frames/s, 16,000 samples/s
```

Any sustained deviation — for example 100 frames/s when 50 are expected — means the declared format no longer matches reality. Treat that as the bug.

A minimal cadence monitor, to adapt to the user's language:

```python
import time

class CadenceMonitor:
    def __init__(self, declared_rate, label="mic"):
        self.declared_rate = declared_rate
        self.label = label
        self.window_start = time.monotonic()
        self.frames = 0
        self.samples = 0

    def on_frame(self, samples_per_channel):
        self.frames += 1
        self.samples += samples_per_channel
        elapsed = time.monotonic() - self.window_start
        if elapsed >= 1.0:
            actual_rate = self.samples / elapsed
            drift = actual_rate / self.declared_rate
            flag = "  <-- MISMATCH" if abs(drift - 1.0) > 0.05 else ""
            print(f"[{self.label}] {self.frames / elapsed:.1f} frames/s, "
                  f"{actual_rate:.0f} samples/s (declared {self.declared_rate}){flag}")
            self.window_start = time.monotonic()
            self.frames = 0
            self.samples = 0
```

### 3. Log audio state transitions next to the cadence

Timestamp these events in the same log as the cadence output:

- playback open, start, stop, close, and reopen
- capture open and close
- agent state changes, interruption events, and transcripts (when RTM events are enabled)

Then reproduce the failure. A cadence jump that lines up with a playback transition shows that the failure starts in the device audio stack, not in ConvoAI.

### 4. Check format consistency on every send

- The sample rate passed to the SDK equals the rate the capture device actually delivers. The SDK cannot detect a mismatch: it trusts the declared value.
- The channel count passed to the SDK equals the channel layout of the buffer. Interleaved stereo sent as mono doubles the apparent sample count.
- Values are within what the send API accepts:
  - Server Gateway `sendAudioPcmData`: sample rate ≥ 8000 Hz, `samples_per_channel` sized for 10 ms.
  - Native custom audio tracks (`pushExternalAudioFrame`): sample rate 8000, 16000, 32000, 44100, or 48000 Hz; 1 or 2 channels; generally 2 bytes per sample; a timestamp on every frame.
  - For other SDKs, check the send method in the [API reference](https://api-ref.agora.io/en/) for the user's platform.
- Frames are sent at real-time cadence. Do not flush a backlog of buffered audio in a burst after a stall; drop it instead.

### 5. Check for echo

If the microphone picks up the agent's voice from the speaker, the agent hears itself and can interrupt itself or treat its own speech as user input.

- **Custom capture does not get echo cancellation by default.** On native SDK custom audio tracks, `AudioTrackConfig.enableAudioProcessing` controls AEC, noise suppression (ANS), and gain control (AGC). It defaults to `false` and only takes effect for `AUDIO_TRACK_DIRECT` tracks. Without it, or an equivalent on the device, pushed PCM carries any speaker echo straight to the agent.
- Echo cancellation needs the playback signal as a reference. If the device plays agent audio through a path the echo canceller never sees (for example, direct ALSA playback while PCM is pushed into the SDK separately), echo is not removed even when processing is enabled.
- Test with headphones or a muted speaker. If interruption becomes reliable, echo is the cause.
- Fix by enabling SDK audio processing where the custom track supports it, using codec or hardware AEC, or routing playback through the same component that performs echo cancellation.

### 6. Only then tune ConvoAI turn settings

Once input is verified, VAD, turn detection, and interruption settings are legitimate tuning targets. The join payload configures start-of-speech and end-of-speech detection separately from interruption behavior, and it includes client-signaled (manual) modes that suit push-to-talk hardware. Field names, defaults, and allowed values change, so fetch the current schema from the [Join Endpoint](https://docs-md.agora.io/en/conversational-ai/rest-api/agent/join.md) instead of answering from memory.

## Embedded Linux / ALSA Notes

These are general Linux audio practices, not Agora APIs. They come from field reports where capture rate changed after playback restarted; treat them as things to try and measure, not guaranteed fixes.

Shared audio codecs on embedded boards often clock capture and playback together. Reconfiguring one direction can silently change the other.

- **Read the actual hardware parameters while the stream runs**, not just the requested ones:

  ```bash
  cat /proc/asound/card*/pcm*c/sub*/hw_params   # capture
  cat /proc/asound/card*/pcm*p/sub*/hw_params   # playback
  ```

  Compare `rate` and `channels` before and after playback restarts.
- **Capture in the codec's native channel layout and downmix in software.** If the codec runs stereo, capturing stereo and extracting one channel is often more stable than requesting mono from the driver.
- **Keep the playback stream open between agent turns.** Write silence instead of closing and reopening playback on every interruption or response; each reopen is a chance for the codec to reconfigure.
- **Open capture and playback with compatible rates**, or use one full-duplex configuration, so neither direction forces the shared clock to change.
- The underlying driver or codec defect may never be pinned down. A configuration that keeps measured cadence stable across playback restarts is a valid fix.

## Explaining Findings to the User

Many people building on hardware are not audio engineers. When reporting diagnostics:

- Say plainly what was measured and what it means: "Your microphone is delivering twice as many samples as it says it is, so speech looks twice as fast to the agent."
- State which layer is at fault: device audio stack, application send loop, echo path, or ConvoAI configuration.
- Do not suggest an Agora-side change unless the input checks pass and the problem persists.
