# Agora RTM (Real-Time Messaging / Signaling)

Signaling, text messaging, presence, and metadata — used alongside or independently from RTC. RTC and RTM are **independent systems**: RTC channels and RTM channels are separate namespaces.

## When to Use RTM

- Text chat during video calls
- Signaling (call invitations, control messages)
- User presence/status tracking
- Custom data exchange (VAD signals, resolution requests)
- Sending text messages to AI agents (Conversational AI)

## Key Concepts

- **Message channels**: Pub/sub messaging. Subscribe to receive messages, publish to send.
- **Stream channels**: Joined channels with topics. More structured than message channels.
- **Presence**: Track who is online, user status metadata.
- **Storage**: Channel and user metadata (key-value store with versioning).
- **Lock**: Distributed locking for shared resources.
- RTM uses **string UIDs** (not numeric like RTC). When using RTC and RTM together, use `String(rtcUid)` as the RTM user ID to maintain a consistent mapping.

## Platform Reference Files

- **[web.md](web.md)** — `agora-rtm` v2 (JS/TS): RTM client, messaging, presence, v1 legacy API
- **iOS / Android** — <https://docs-md.agora.io/en/signaling/get-started/sdk-quickstart.md>
