# Agora RTM (Real-Time Messaging / Signaling)

Signaling, text messaging, presence, and metadata — used alongside or independently from RTC. RTC and RTM are **independent systems**: RTC channels and RTM channels are separate namespaces.

## When to Use RTM

- Text chat during video calls
- Signaling (call invitations, control messages, hang-up)
- User presence and status tracking
- Custom data exchange (VAD signals, resolution requests, state sync)
- Receiving transcripts from Conversational AI agents

## Channel Types

RTM has two channel types with different semantics:

|                     | Message Channel                          | Stream Channel                              |
| ------------------- | ---------------------------------------- | ------------------------------------------- |
| **Model**           | Pub/sub                                  | Join + topic subscribe                      |
| **Join required**   | No — subscribe to publish/receive        | Yes — must join before publishing           |
| **Topics**          | No                                       | Yes — messages published per topic          |
| **Use for**         | Signaling, chat, ConvoAI transcripts     | High-frequency data, custom media streams   |
| **Presence events** | Via `presence.getOnlineUsers()` or event | Built-in via channel join/leave events      |

**Default choice**: Use message channels for most use cases. Use stream channels only if you need topic-based filtering or high-frequency updates (e.g., cursor positions, sensor data).

## Key Concepts

- **Presence**: Track online users and their metadata per channel. Subscribe to `presence` events to detect joins, leaves, and state changes in real time.
- **Storage**: Channel and user metadata — key-value store with versioning and compare-and-set (CAS) for conflict resolution.
- **Lock**: Distributed locking for coordinating shared resources across users.
- **RTM UIDs are strings** — not numeric like RTC. When using RTC and RTM together, use `String(rtcUid)` as the RTM user ID to keep both systems in sync.

## Gotchas & Critical Rules

- **UID type mismatch causes silent failures** — RTC UIDs are numbers; RTM UIDs are strings. Always use `String(rtcUid)` as the RTM user ID. Type mismatches don't throw errors — they silently break user lookups across both systems.
- **Namespace isolation** — RTC channels and RTM channels are completely separate. Joining RTC channel `"meeting-1"` does NOT auto-subscribe you to RTM channel `"meeting-1"`. Subscribe both explicitly.
- **Login before all operations** — `rtmClient.login()` must complete before any subscribe, publish, or presence call. Operations attempted before login resolves fail silently, not with an error.
- **Subscribe before presence** — Presence events (joins/leaves) require an active channel subscription. Publishing to a channel without subscribing means you won't receive presence notifications or responses.
- **RTM v2 API is a full rewrite** — Do NOT apply v1 patterns (`AgoraRTM.createInstance()`, `.createChannel()`) to v2. The APIs are incompatible. The Web reference (`web.md`) covers v2 only.
- **ConvoAI transcript delivery requires two flags** — For AI agent transcripts to arrive via RTM, the ConvoAI `/join` payload must include both `advanced_features.enable_rtm: true` AND `parameters.data_channel: "rtm"`. One flag alone is not sufficient.

## RTC + RTM Coordination Pattern

When pairing RTC and RTM in the same app:

1. Join RTC channel with numeric UID (or `0` for auto-assignment)
2. After RTC join resolves, log in to RTM with `String(rtcUid)`
3. Subscribe to the RTM message channel
4. Use RTC for media (audio/video tracks), RTM for all signaling and metadata

```javascript
// RTC join resolves with the assigned numeric UID
const rtcUid = await rtcClient.join(appId, channelName, token, null);

// Mirror UID into RTM as a string — keeps both systems in sync
await rtmClient.login({ uid: String(rtcUid) });
const { status } = await rtmClient.subscribe(channelName);
```

RTM channel name does not need to match the RTC channel name, but using the same name is the conventional approach.

## Platform Reference Files

- **[web.md](web.md)** — `agora-rtm` v2 (JS/TS): client, messaging, presence, stream channels, v1 legacy notes
- **iOS / Android** — Level 2 fetch required: use [doc-fetching.md](../doc-fetching.md) or fetch directly from <https://docs-md.agora.io/en/signaling/get-started/sdk-quickstart.md>
