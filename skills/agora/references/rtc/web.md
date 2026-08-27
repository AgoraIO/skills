# Agora RTC Web SDK (agora-rtc-sdk-ng)

## Table of Contents

- [Installation](#installation)
- [Client Creation](#client-creation)
- [Joining a Channel](#joining-a-channel)
- [Creating Tracks](#creating-tracks)
- [Publishing and Subscribing](#publishing-and-subscribing)
- [Event Handling](#event-handling)
- [Leaving and Cleanup](#leaving-and-cleanup)
- [Token Renewal](#token-renewal)
- [Volume Monitoring](#volume-monitoring)
- [Network Quality](#network-quality)
- [Device Enumeration](#device-enumeration)
- [Complete Example: Video Call](#complete-example-video-call)
- [Large-Scale Subscription Management](#large-scale-subscription-management)
- [Track Muting](#track-muting)
- [Screen Sharing](#screen-sharing)

## Installation

```bash
npm install agora-rtc-sdk-ng
```

Package: `agora-rtc-sdk-ng` (v4.x). Do NOT use deprecated `agora-rtc-sdk` (v3.x).

## Client Creation

Choose one mode for a client instance.

Communication mode (all peers equal):

```typescript
import AgoraRTC from "agora-rtc-sdk-ng"

// Communication mode (all peers equal)
const client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" })
```

Live broadcasting mode (host/audience roles):

```typescript
import AgoraRTC from "agora-rtc-sdk-ng"

// Live broadcasting mode (host/audience roles)
const client = AgoraRTC.createClient({ mode: "live", codec: "vp8" })
```

Codec options: `"vp8"`, `"vp9"`, `"h264"`, `"h265"`, `"av1"`. Use `"vp8"` for broadest browser support. Safari 12.1 and earlier does not support VP8. `"av1"` is available in newer SDK versions for modern browsers.

## Joining a Channel

Choose one UID strategy for communication mode.

Auto-assigned UID:

```typescript
// Join with auto-assigned UID
const uid = await client.join(APP_ID, "channel-name", TOKEN, null)
```

Specific UID:

```typescript
// Join with specific UID
const uid = await client.join(APP_ID, "channel-name", TOKEN, 12345)
```

For live broadcasting, choose one role and set it before joining:

```typescript
// For live broadcasting, set role before joining
const role = isHost ? "host" : "audience"
await client.setClientRole(role)
const uid = await client.join(APP_ID, "channel-name", TOKEN, null)
```

- `TOKEN`: Pass `null` for testing without tokens enabled. In production, always use a server-generated token.
- `uid`: Pass `null` for auto-assignment, or a specific number. String UIDs also supported.

### UID Constraints (Easy to Miss)

- Numeric UID: `0` to `2^32 - 1` (32-bit unsigned integer).
- String UID: ASCII only, maximum `255` characters.
- Keep UID type consistent per channel: all users should use either numeric or string UIDs, not a mix.

## Creating Tracks

### Microphone Audio

```typescript
const audioTrack = await AgoraRTC.createMicrophoneAudioTrack({
  encoderConfig: "high_quality_stereo",
  AEC: true,  // Acoustic Echo Cancellation
  ANS: true,  // Automatic Noise Suppression
  AGC: true,  // Automatic Gain Control
})
```

### Camera Video

```typescript
const videoTrack = await AgoraRTC.createCameraVideoTrack({
  encoderConfig: "720p_2",
  cameraId: deviceId, // optional specific camera
})
```

### Both Simultaneously

```typescript
const [audioTrack, videoTrack] = await AgoraRTC.createMicrophoneAndCameraTracks(
  { encoderConfig: "high_quality_stereo" },
  { encoderConfig: "720p_2" }
)
```

### Custom Encoder Config

```typescript
const videoTrack = await AgoraRTC.createCameraVideoTrack({
  encoderConfig: {
    width: 640,
    height: 360,
    frameRate: 24,
    bitrateMin: 400,
    bitrateMax: 1000,
  }
})
```

## Publishing and Subscribing

### Publish Local Tracks

```typescript
// Publish after joining
await client.publish([audioTrack, videoTrack])

// Play local video in DOM element
videoTrack.play("local-player") // element ID or HTMLElement
```

### Subscribe to Remote Users

```typescript
client.on("user-published", async (user, mediaType) => {
  await client.subscribe(user, mediaType)

  if (mediaType === "video") {
    user.videoTrack.play(`player-${user.uid}`)
  }
  if (mediaType === "audio") {
    user.audioTrack.play() // no DOM element needed for audio
  }
})
```

### Selective Subscription

```typescript
// Don't auto-subscribe to everyone; filter by UID
client.on("user-published", async (user, mediaType) => {
  if (shouldSubscribe(user.uid)) {
    await client.subscribe(user, mediaType)
  }
})
```

## Event Handling

Register ALL event handlers BEFORE calling `client.join()`.

```typescript
// Remote user joins channel
client.on("user-joined", (user) => {
  console.log("User joined:", user.uid)
})

// Remote user publishes track (fires separately for audio and video)
client.on("user-published", async (user, mediaType) => {
  await client.subscribe(user, mediaType)
  if (mediaType === "video") user.videoTrack.play(`player-${user.uid}`)
  if (mediaType === "audio") user.audioTrack.play()
})

// Remote user unpublishes track
client.on("user-unpublished", (user, mediaType) => {
  if (mediaType === "video") {
    document.getElementById(`player-${user.uid}`)?.remove()
  }
})

// Remote user leaves
client.on("user-left", (user) => {
  document.getElementById(`player-${user.uid}`)?.remove()
})

// Connection state changes
client.on("connection-state-change", (curState, prevState, reason) => {
  console.log(`${prevState} -> ${curState}, reason: ${reason}`)
})

// Network quality (fires every 2 seconds after joining)
client.on("network-quality", (stats) => {
  // uplinkNetworkQuality/downlinkNetworkQuality: 0-6 (0=unknown, 1=excellent, 5=very bad, 6=disconnected)
})

// Stream messages from data channel (used by Conversational AI)
client.on("stream-message", (uid, stream) => {
  const text = new TextDecoder().decode(stream)
  console.log("Stream message from", uid, text)
})

// Token expiry warning
client.on("token-privilege-will-expire", async () => {
  const newToken = await fetchTokenFromServer()
  await client.renewToken(newToken)
})

// SDK exceptions
client.on("exception", (event) => {
  console.warn("SDK exception:", event)
})
```

## Leaving and Cleanup

```typescript
async function leave() {
  // 1. Stop and close local tracks
  if (audioTrack) {
    audioTrack.stop()
    audioTrack.close()
  }
  if (videoTrack) {
    videoTrack.stop()
    videoTrack.close()
  }

  // 2. Leave channel
  await client.leave()
}
```

Always `stop()` then `close()`. Failure to close tracks leaves microphone/camera locked.

## Token Renewal

```typescript
client.on("token-privilege-will-expire", async () => {
  // Fetch new token from your server
  const response = await fetch(`/api/token?channel=${channel}&uid=${uid}`)
  const { token } = await response.json()
  await client.renewToken(token)
})

// Also handle token-privilege-did-expire as fallback
client.on("token-privilege-did-expire", async () => {
  // Token already expired — re-join with new token
  const { token } = await fetch(`/api/token?channel=${channel}&uid=${uid}`).then(r => r.json())
  await client.leave()
  await client.join(APP_ID, channel, token, uid)
})
```

## Volume Monitoring

```typescript
// Poll volume levels at interval
setInterval(() => {
  // Local
  if (audioTrack) {
    const level = audioTrack.getVolumeLevel() // 0.0 - 1.0
  }

  // Remote
  client.remoteUsers.forEach(user => {
    if (user.audioTrack) {
      const level = user.audioTrack.getVolumeLevel()
    }
  })
}, 200)
```

## Network Quality

```typescript
client.on("network-quality", (stats) => {
  // stats.uplinkNetworkQuality: 0-6
  // stats.downlinkNetworkQuality: 0-6
  // 0=unknown, 1=excellent, 2=good, 3=poor, 4=bad, 5=very bad, 6=disconnected
})

// Get detailed stats
const localStats = client.getLocalAudioStats()
const remoteStats = client.getRemoteAudioStats()
const localVideoStats = client.getLocalVideoStats()
```

## Device Enumeration

```typescript
const cameras = await AgoraRTC.getCameras()
const microphones = await AgoraRTC.getMicrophones()
const speakers = await AgoraRTC.getPlaybackDevices()

// Switch device on existing track
await videoTrack.setDevice(newCameraId)
await audioTrack.setDevice(newMicrophoneId)

// Listen for device changes
AgoraRTC.onMicrophoneChanged = (info) => {
  console.log("Mic changed:", info.state, info.device)
}
AgoraRTC.onCameraChanged = (info) => {
  console.log("Camera changed:", info.state, info.device)
}
```

## Complete Example: Video Call

```typescript
import AgoraRTC, {
  IAgoraRTCClient,
  ICameraVideoTrack,
  IMicrophoneAudioTrack,
} from "agora-rtc-sdk-ng"

const APP_ID = "your-app-id"
let client: IAgoraRTCClient
let localAudioTrack: IMicrophoneAudioTrack
let localVideoTrack: ICameraVideoTrack

async function join(channel: string, token: string | null) {
  client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" })

  // Register events BEFORE joining
  client.on("user-published", async (user, mediaType) => {
    await client.subscribe(user, mediaType)
    if (mediaType === "video") {
      const container = document.createElement("div")
      container.id = `player-${user.uid}`
      container.style.width = "640px"
      container.style.height = "480px"
      document.getElementById("remote-players")!.appendChild(container)
      user.videoTrack!.play(container)
    }
    if (mediaType === "audio") {
      user.audioTrack!.play()
    }
  })

  client.on("user-unpublished", (user, mediaType) => {
    if (mediaType === "video") {
      document.getElementById(`player-${user.uid}`)?.remove()
    }
  })

  client.on("user-left", (user) => {
    document.getElementById(`player-${user.uid}`)?.remove()
  })

  // Join
  const uid = await client.join(APP_ID, channel, token, null)

  // Create and publish tracks
  ;[localAudioTrack, localVideoTrack] = await AgoraRTC.createMicrophoneAndCameraTracks()
  localVideoTrack.play("local-player")
  await client.publish([localAudioTrack, localVideoTrack])
}

async function leave() {
  localAudioTrack?.stop()
  localAudioTrack?.close()
  localVideoTrack?.stop()
  localVideoTrack?.close()
  await client?.leave()
}
```

## Large-Scale Subscription Management

For multi-channel viewing and priority-based dynamic subscription patterns,
read [large-scale-subscriptions.md](large-scale-subscriptions.md). Fetch current
Agora documentation before stating channel or publisher capacity limits.

## Track Muting

Use `setEnabled()` to mute/unmute local tracks. This stops the media capture (camera light turns off when video is disabled):

```typescript
// Mute/unmute audio
await localAudioTrack.setEnabled(false) // mute (stops mic capture)
await localAudioTrack.setEnabled(true)  // unmute

// Mute/unmute video
await localVideoTrack.setEnabled(false) // camera off
await localVideoTrack.setEnabled(true)  // camera on
```

`setEnabled(false)` differs from `setMuted(true)`: `setEnabled` stops the device, while `setMuted` sends silence/black frames but keeps the device active.

## Screen Sharing

For the dual-client screen-sharing pattern, including system audio, separate
identity/token handling, `track-ended`, and cleanup, read
[screen-sharing.md](screen-sharing.md).

## Official Documentation

For APIs or features not covered above:

- API Reference: <https://api-ref.agora.io/en/video-sdk/web/4.x/index.html>
- Guides: <https://docs.agora.io/en/video-calling/overview/product-overview>
