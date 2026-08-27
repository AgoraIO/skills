# Agora RTC Web Large-Scale Subscriptions

Use this reference when a Web application needs multi-channel viewing or must
limit subscriptions dynamically. Fetch current Agora documentation before
stating channel, host, or publisher capacity limits.

## Multi-Channel Pattern

Use multiple audience client instances when the application architecture
requires viewers to consume publishers from separate channels:

```typescript
import AgoraRTC, { IAgoraRTCClient } from "agora-rtc-sdk-ng"

const clients: IAgoraRTCClient[] = []
const channelNames = getChannelNames()

for (const channelName of channelNames) {
  const client = AgoraRTC.createClient({ mode: "live", codec: "vp8" })
  await client.setClientRole("audience")

  client.on("user-published", async (user, mediaType) => {
    // Apply the application's subscription policy for this channel.
  })

  const uid = await allocateViewerUid(channelName)
  const token = await fetchRtcToken(channelName, uid)
  await client.join(APP_ID, channelName, token, uid)
  clients.push(client)
}
```

Register events before each client joins. Generate tokens for the exact channel
and identity used by that client, and leave every client during cleanup.

## Dynamic Subscription Management

For apps with many publishers, keep an available-publisher set and subscribe
only to the users selected by the application's priority policy:

```typescript
const videoPublishers = new Map()    // uid -> client
const videoSubscriptions = new Map() // uid -> subscription info

client.on("user-published", (user, mediaType) => {
  if (mediaType === "video") {
    videoPublishers.set(user.uid, client)
  }
})

async function manageSubscriptions(maxSubs: number) {
  const prioritized = [...videoPublishers.keys()].slice(0, maxSubs)

  for (const uid of prioritized) {
    if (!videoSubscriptions.has(uid)) {
      const user = client.remoteUsers.find(user => user.uid === uid)
      if (user) {
        await client.subscribe(user, "video")
        user.videoTrack?.play(`player-${uid}`)
        videoSubscriptions.set(uid, { startTime: Date.now() })
      }
    }
  }

  for (const uid of videoSubscriptions.keys()) {
    if (!prioritized.includes(uid)) {
      const user = client.remoteUsers.find(user => user.uid === uid)
      if (user) await client.unsubscribe(user, "video")
      videoSubscriptions.delete(uid)
    }
  }
}
```

Base priority and `maxSubs` on the product experience and observed device and
network conditions. Do not copy a cached capacity number from this skill.

## Official Documentation

- [Web SDK API reference](https://api-ref.agora.io/en/video-sdk/web/4.x/index.html)
- [Agora video calling guides](https://docs.agora.io/en/realtime-media/rtc)
