# Agora RTC Web Screen Sharing

Use a separate client instance for screen sharing so publishing the screen does
not replace the camera track. The screen-share client joins the same channel
with a different UID and matching token.

## Dual-Client Pattern

```typescript
import AgoraRTC from "agora-rtc-sdk-ng"

// 1. Create a second client for screen sharing
const screenClient = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" })

// 2. Allocate a distinct screen-share UID and mint its matching token
const screenUid = await allocateScreenShareUid(cameraUid)
const screenToken = await fetchRtcToken(channelName, screenUid)

// 3. Create screen track — returns single track or [video, audio] tuple
const screenTrackOrTracks = await AgoraRTC.createScreenVideoTrack({
  encoderConfig: { width: 1920, height: 1080, frameRate: 15 },
  optimizationMode: "detail", // "detail" for text/slides, "motion" for video
}, "auto") // "auto" = include system audio if available

// Handle the return type (single track or tuple)
const screenVideoTrack = Array.isArray(screenTrackOrTracks)
  ? screenTrackOrTracks[0]
  : screenTrackOrTracks
const screenAudioTrack = Array.isArray(screenTrackOrTracks)
  ? screenTrackOrTracks[1]
  : null

// 4. Join the same channel with a different UID and token
await screenClient.join(APP_ID, channelName, screenToken, screenUid)

// 5. Publish screen track(s)
const tracksToPublish = screenAudioTrack
  ? [screenVideoTrack, screenAudioTrack]
  : [screenVideoTrack]
await screenClient.publish(tracksToPublish)

// 6. CRITICAL: Listen for "track-ended" — fires when user stops sharing
screenVideoTrack.on("track-ended", async () => {
  for (const track of tracksToPublish) {
    track.stop()
    track.close()
  }
  await screenClient.leave()
})

// 7. Provide an explicit cleanup path for application controls
async function stopScreenShare() {
  for (const track of tracksToPublish) {
    track.stop()
    track.close()
  }
  await screenClient.leave()
}
```

## Coordination Rules

- Use RTM to announce screen-share start and stop when other participants need
  explicit state; include the screen UID so viewers can identify the stream.
- Remote participants see the screen share as another user. Keep the mapping
  between camera UID and screen UID explicit in application state.
- Allocate the screen UID through application identity logic; do not rely on
  arithmetic offsets that can collide or exceed a platform's UID range.
- Generate a separate token whose UID matches the screen-share client UID.
- Always handle `track-ended` and provide explicit cleanup for application UI.

## Official Documentation

- [Web SDK API reference](https://api-ref.agora.io/en/video-sdk/web/4.x/index.html)
- [Agora video calling guides](https://docs.agora.io/en/realtime-media/rtc)
