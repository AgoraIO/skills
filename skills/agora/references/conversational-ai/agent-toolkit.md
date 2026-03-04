# Agent Toolkit SDK

TypeScript SDK (`@agora/conversational-ai`) — framework-agnostic core for ConvoAI clients.

**Repo:** <https://github.com/AgoraIO-Conversational-AI/agent-toolkit>
**npm:** `@agora/conversational-ai`

## Installation

> See [README — Quick Start](https://github.com/AgoraIO-Conversational-AI/agent-toolkit#quick-start)

## ConversationalAIAPI

Main orchestration class. Handles init, agent connection, message sending, transcript management.

> **[README — ConversationalAIAPI](https://github.com/AgoraIO-Conversational-AI/agent-toolkit#conversationalapiapi)** — init(), getInstance(), sendMessage(), getTranscript(), events

## RTCHelper

Agora RTC wrapper. Audio/video track management, join/leave, publish/unpublish, volume monitoring.

- `createVideoTrack()`, `setVideoEnabled()`, `getVideoEnabled()` for video lifecycle
- Subscription filters: `shouldSubscribeAudio(uid)`, `shouldSubscribeVideo(uid)` callbacks in init config

> **[README — RTCHelper](https://github.com/AgoraIO-Conversational-AI/agent-toolkit#rtchelper)** — join, tracks, shouldSubscribeAudio/Video callbacks

## RTMHelper

Agora RTM wrapper for text messaging alongside voice.

- Dynamic key auth fix: token now correctly passed for `APP_CERTIFICATE`-enabled projects

> **[README — RTMHelper](https://github.com/AgoraIO-Conversational-AI/agent-toolkit#rtmhelper)**

## SubRenderController

Queue-based message processing with PTS sync, deduplication, render modes.

> **[README — SubRenderController](https://github.com/AgoraIO-Conversational-AI/agent-toolkit#subrendercontroller)**

## React Hooks

- `useLocalVideo` — local camera track management
- `useRemoteVideo` — remote video subscription

> **[README — React Integration](https://github.com/AgoraIO-Conversational-AI/agent-toolkit#react-integration)**

## Events

- `transcript-updated` — new/updated transcript items
- `connection-state-changed` — agent connection lifecycle
- `agent-error` — error events

> **[README — Events](https://github.com/AgoraIO-Conversational-AI/agent-toolkit#events)**

## Types

- `TranscriptItem`, `UserTranscription`, `AgentTranscription`
- `AgentState`, `TurnStatus`, `ConnectionState`
- `MessageInterrupt`, `Word`

> **[README — Types](https://github.com/AgoraIO-Conversational-AI/agent-toolkit#types)**
