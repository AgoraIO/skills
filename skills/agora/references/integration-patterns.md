# Multi-Product Integration Patterns

This file covers how RTC, RTM, and Conversational AI work together. For SDK-specific code, follow the Level 2 fetch links in each product's reference file.

## When to Use Multiple Products

| Scenario | Products |
|---|---|
| Video/voice call only | RTC only |
| Video call + chat or presence | RTC + RTM |
| AI agent in a call | RTC + ConvoAI REST API (server-side) |
| AI agent + live transcripts or state | RTC + RTM + ConvoAI REST API |
| Text-only signaling (no media) | RTM only |

## RTC + RTM Together

### Initialization Order

Always initialize both SDKs independently — they share no initialization path. The recommended order:

1. Create and initialize the RTC engine/client
2. Create and log in to the RTM client
3. Subscribe to the RTM channel
4. Join the RTC channel

Subscribe to RTM **before** joining RTC so that presence events for peers already in the channel are not missed.

### UID Strategy

RTC and RTM use different UID types:

| SDK | Platform | UID type |
|---|---|---|
| RTC | Web | `number` |
| RTC | iOS | `UInt` (unsigned 32-bit) |
| RTC | Android | `Int` (signed 32-bit) |
| RTM | All platforms | `String` |

Use `String(rtcUid)` as the RTM `userId`. This is the standard convention across platform demos and toolkits. UIDs greater than 2,147,483,647 wrap to negative on Android RTC — avoid them if Android clients are present.

### Channel Name Convention

Use the **same channel name** for both RTC and RTM. The RTM channel is the coordination layer for the RTC session — same name makes routing unambiguous and is required by the ConvoAI toolkit.

### Token Matrix

Both SDKs require separate tokens in production. Generate them independently on your server:

| Token | Scope | Renew on |
|---|---|---|
| RTC token | `appId` + `channelName` + `uid` | `token-privilege-will-expire` / `onTokenPrivilegeWillExpire` |
| RTM token | `appId` + `userId` | RTM connection state `TOKEN_EXPIRED` or equivalent |

See [server/tokens.md](server/tokens.md) for token generation details.

For Level 2 fetch: fetch `https://docs.agora.io/en/llms.txt`, find the token management guide for your platform, then fetch it.

## RTC + RTM + ConvoAI

### How the Products Connect

```
Client                          Server
──────────────────────────────────────────────────────
RTC Engine/Client ──── media ────► Agora RTC
RTM Client ────── messages ──────► Agora RTM
                                      │
                              [ConvoAI agent joins
                               same RTC channel,
                               publishes transcripts
                               and state to same
                               RTM channel]
                                      ▲
App Server ── REST POST /join ──────► Agora ConvoAI API
```

### Initialization Order for ConvoAI

1. Initialize RTC (but do not join the channel yet)
2. Initialize RTM and log in
3. Subscribe to the RTM channel (to receive agent events)
4. Call ConvoAI REST `POST /join` from your **app server** with `channelName`, `uid` (your user's RTC uid), and the RTM flags (see below)
5. Join the RTC channel — the agent will already be there or will join shortly

### Required ConvoAI Flags for RTM Delivery

When calling `POST /join`, include both of these in the request body:

```json
{
  "advanced_features": {
    "enable_rtm": true
  },
  "parameters": {
    "data_channel": "rtm"
  }
}
```

Both flags are required. Omitting either one means the agent publishes transcripts via RTC data channel instead of RTM, and RTM message events will not fire.

### RTM Channel Name = RTC Channel Name

The ConvoAI agent joins the RTM channel with the **same name** as the RTC channel it joined. When handling `onMessageEvent` / `didReceiveMessageEvent`, filter by `channelName` matching your RTC channel if you are subscribed to multiple channels.

### Agent Events via RTM

The agent publishes JSON messages to the RTM channel. Parse `event.message.data` (Android) or `event.message.stringData` (iOS) as JSON. The `customType` field indicates the event type (transcript, interruption, state change, etc.).

For the full event schema and `customType` values, use Level 2 fetch: fetch `https://docs.agora.io/en/llms.txt`, locate the Conversational AI event reference, then fetch it.

### Token Matrix for ConvoAI

ConvoAI sessions require three separate tokens:

| Token | Purpose | Who generates |
|---|---|---|
| RTC token (user) | User joins RTC channel | Your app server |
| RTM token (user) | User logs into RTM | Your app server |
| RTC token (agent) | ConvoAI agent joins RTC | Your app server, passed in POST /join |

See [conversational-ai/auth-flow.md](conversational-ai/auth-flow.md) for the full three-token flow (REST API implementors) or [conversational-ai/README.md](conversational-ai/README.md) for SDK-based flows.

## Codec Selection for Mixed Platforms

When Web clients share a channel with iOS or Android native clients:

- Web defaults to `codec: 'vp8'` — this scales well for multi-user calls and is the recommended choice
- `'vp9'` is also a good option with better compression
- `'h264'` does not scale well beyond small groups — avoid it for multi-user scenarios
- If codecs differ between Web and native clients, Agora transcodes server-side — this works but adds latency and is billed separately

See [rtc/cross-platform-coordination.md](rtc/cross-platform-coordination.md) for full cross-platform interop notes.

## Cleanup Order

Reverse of initialization:

1. Leave the RTC channel
2. Unsubscribe from RTM channels
3. Log out of RTM
4. Release both engines/clients

For ConvoAI: call `DELETE /leave` (or the SDK equivalent) from your app server before leaving the RTC channel, to give the agent time to exit gracefully.

## Reference Files by Product

| Product | Platform | File |
|---|---|---|
| RTC | Web | [rtc/web.md](rtc/web.md) |
| RTC | React | [rtc/react.md](rtc/react.md) |
| RTC | Next.js | [rtc/nextjs.md](rtc/nextjs.md) |
| RTC | iOS | [rtc/ios.md](rtc/ios.md) |
| RTC | Android | [rtc/android.md](rtc/android.md) |
| RTC | React Native | [rtc/react-native.md](rtc/react-native.md) |
| RTC | Flutter | [rtc/flutter.md](rtc/flutter.md) |
| RTM | Web | [rtm/web.md](rtm/web.md) |
| RTM | iOS | [rtm/ios.md](rtm/ios.md) |
| RTM | Android | [rtm/android.md](rtm/android.md) |
| ConvoAI | All | [conversational-ai/README.md](conversational-ai/README.md) |
| ConvoAI toolkit | iOS | [conversational-ai/agent-toolkit-ios.md](conversational-ai/agent-toolkit-ios.md) |
| ConvoAI toolkit | Android | [conversational-ai/agent-toolkit-android.md](conversational-ai/agent-toolkit-android.md) |
| Tokens | Server | [server/tokens.md](server/tokens.md) |
| Cross-platform | All | [rtc/cross-platform-coordination.md](rtc/cross-platform-coordination.md) |
