---
name: conversational-ai-architecture
description: |
  System architecture and call sequence for Agora Conversational AI agents. Use when the user
  asks how ConvoAI works, what components are involved, initialization order, token flow,
  agent lifecycle, start/stop sequence, or how server, client, RTC, RTM, and the ConvoAI
  platform fit together.
license: MIT
metadata:
  author: agora
  version: '1.0.0'
---

# ConvoAI Architecture and Call Sequence

Read this file first when the user asks how a ConvoAI voice agent is wired end to end, what calls happen in what order, or how to manage agent lifecycle across server and client.

For implementation details after the architecture is clear:

| Topic                                      | File                                                     |
| ------------------------------------------ | -------------------------------------------------------- |
| Token types and auth headers               | [auth-flow.md](auth-flow.md)                             |
| Server SDK session management              | [server-sdks.md](server-sdks.md)                         |
| RTC + RTM + ConvoAI init order and cleanup | [../integration-patterns.md](../integration-patterns.md) |
| Client transcripts, state, sendText        | [agent-toolkit.md](agent-toolkit.md)                     |
| REST endpoint schemas                      | [README.md](README.md) + OpenAPI spec                    |
| Official quickstart source code            | [quickstarts.md](quickstarts.md)                         |

## System Components

```text
┌──────────────────────┐     start/stop session      ┌─────────────────┐    REST /join,/leave,/update   ┌──────────────────────┐
│ Browser/Mobile App   │ ──────────────────────────► │   Your Server   │ ─────────────────────────────► │ Agora ConvoAI Engine │
│ UI + app state       │ ◄──── channel + tokens ──── │  (app backend)  │ ◄────── agent_id,status ────── │  manages agent       │
└──────────┬───────────┘                             └─────────────────┘                                └──────────┬───────────┘
           │ uses RTC/RTM SDKs                                                                          creates/updates/stops
           ▼                                                                                                      ▼
┌──────────────────────┐                                                                    ┌──────────────────────┐
│ Agora RTC + RTM SDKs │                                                                    │   ConvoAI Agent      │
│ client-side runtime  │                                                                    │ managed participant  │
└──────────┬───────────┘                                                                    └──────────┬───────────┘
           │ joins/publishes/subscribes                                                                │ joins/publishes/subscribes
           ▼                                                                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      Agora Realtime Channels (SDRTN)                                           │
│  RTC channel: client mic audio flows to the agent; agent TTS audio flows back to the client                    │
│  RTM channel: transcripts, agent state, metrics, errors, and control messages use the same channel name        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Roles:

- **Your server** starts and stops agents, mints client tokens, and owns session state in your app.
- **ConvoAI Engine** manages the agent lifecycle and pipeline (speech in → ASR → LLM → TTS → speech out).
- **ConvoAI agent** is the managed realtime participant created by the engine. It joins the same RTC channel as the client and can publish RTM events to the matching RTM channel when enabled.
- **Client app** triggers the app backend to start/stop the agent. The app itself sits above the Agora RTC/RTM SDKs.
- **Agora RTC/RTM SDKs and the ConvoAI agent communicate through Agora realtime channels.** The channels are the lowest-level transport layer in this architecture.

The client toolkit does **not** start agents. The server does.

## End-to-End Start Sequence

Typical production flow when a user clicks "Start conversation":

```text
1. Client ──► Your server: "start session" (channel, user identity)
2. Your server ──► Token builder: mint RTC token + RTM token for the user
3. Your server ──► ConvoAI REST POST /join (or SDK session.start())
4. ConvoAI Engine ──► creates agent, agent joins RTC channel (async)
5. Your server ──► Client: { channel, rtcToken, rtmToken, agentId }
6. Client ──► RTM login + subscribe to channel
7. Client ──► RTC join(channel, rtcToken, uid)
8. Client waits for agent RTC user-joined / agent audio before treating session as live
9. User speaks ──► agent hears via RTC ──► agent responds via RTC
10. Transcripts/state arrive via RTM (if enabled) or RTC data channel
```

Important timing rules:

- `POST /join` success means the request was accepted, not that the agent is already in the channel. Wait for RTC `user-joined` or SDK/client agent-state events before expecting audio.
- RTM channel name must match the RTC channel name passed in the join payload.
- RTM login identity must match the RTM token subject.

For auto-assigned RTC UIDs, join RTC first, read the assigned UID, then log into RTM with `String(rtcUid)`. See [../integration-patterns.md](../integration-patterns.md).

## Initialization Order

Default client-side order when the user's RTC UID is known up front:

1. Initialize RTC engine/client (do not join yet)
2. Initialize RTM and log in
3. Subscribe to the RTM channel
4. Call `POST /join` from your server
5. Join the RTC channel

Auto-assigned UID variant:

1. Initialize RTC
2. Join RTC and wait for assigned UID
3. Log into RTM with `String(rtcUid)` and subscribe
4. Call `POST /join` from your server

## Tokens

Three distinct tokens appear in most integrations:

| Token                | Purpose                             | Used by                                        |
| -------------------- | ----------------------------------- | ---------------------------------------------- |
| RTC client token     | User joins RTC channel              | Browser/mobile RTC SDK                         |
| RTM client token     | User logs into RTM                  | Browser/mobile RTM SDK                         |
| ConvoAI server token | Authorize REST calls to ConvoAI API | Your server → `Authorization: agora token=...` |

The agent also needs an RTC token in the join payload (`properties.token`). Your server generates it and passes it to ConvoAI when starting the agent.

SDK users in App Credentials mode: pass `appId + appCertificate` to the server SDK and it generates the ConvoAI server token per request. You still mint the two client tokens yourself.

See [auth-flow.md](auth-flow.md) and [../server/tokens.md](../server/tokens.md).

## Agent Lifecycle

### Platform agent status (REST)

| Status     | Code | Meaning                    |
| ---------- | ---- | -------------------------- |
| IDLE       | 0    | Ready, not active          |
| STARTING   | 1    | Initialization in progress |
| RUNNING    | 2    | Active, processing audio   |
| STOPPING   | 3    | Shutdown in progress       |
| STOPPED    | 4    | Exited channel             |
| RECOVERING | 5    | Error recovery             |
| FAILED     | 6    | Execution failure          |

### Server SDK session states

When using `agora-agents`, map platform lifecycle to SDK session states:

| SDK state           | Typical action                               |
| ------------------- | -------------------------------------------- |
| `idle`              | call `start()`                               |
| `starting`          | wait                                         |
| `running`           | `stop()`, `say()`, `interrupt()`, `update()` |
| `stopping`          | wait                                         |
| `stopped` / `error` | may call `start()` again                     |

See [server-sdks.md](server-sdks.md).

## Managing Agents

Your server owns agent lifecycle. Common operations:

| Operation           | REST                          | SDK equivalent                             |
| ------------------- | ----------------------------- | ------------------------------------------ |
| Start agent         | `POST /join`                  | `session.start()`                          |
| Stop agent          | `POST /agents/{id}/leave`     | `session.stop()` or `client.stopAgent(id)` |
| Update config/token | `POST /agents/{id}/update`    | `session.update()`                         |
| Query status        | `GET /agents/{id}`            | platform query                             |
| List agents         | `GET /agents`                 | platform query                             |
| Broadcast speech    | `POST /agents/{id}/speak`     | `session.say()`                            |
| Interrupt speech    | `POST /agents/{id}/interrupt` | `session.interrupt()`                      |

Production patterns:

- **Stateful server**: hold `AgentSession` in memory; use in-process SDK events.
- **Stateless server**: store `agent_id` in your DB; use platform webhooks or poll `GET /agents/{id}` for state changes.
- **Client UI**: subscribe to RTM agent events for transcripts and live state in the browser.

Fetch full request/response schemas from the OpenAPI spec — do not invent fields:

```text
GET https://docs-md.agora.io/api/conversational-ai-api-v2.x.yaml
```

## RTM Event Delivery

To receive transcripts and agent state in the client via RTM, both join flags are required:

```json
{
  "advanced_features": { "enable_rtm": true },
  "parameters": { "data_channel": "rtm" }
}
```

Without both, events may arrive via RTC data channel instead, and RTM toolkit handlers will not fire.

Optional flags:

- `parameters.enable_metrics: true` for metrics events
- `parameters.enable_error_message: true` for error events

## Stop and Cleanup Sequence

Reverse initialization on session end:

1. Stop the agent from your server (`POST /leave` or SDK `stop()`)
2. Client leaves RTC channel
3. Client unsubscribes from RTM channel
4. Client logs out of RTM
5. Release RTC/RTM engines

Stopping the agent before the client leaves gives the platform time to exit the channel cleanly.

## Where Code Lives

| Layer                    | Responsibility                      | Typical source                                                  |
| ------------------------ | ----------------------------------- | --------------------------------------------------------------- |
| Server start/stop/update | Agent lifecycle, token minting      | Official quickstart backend or [server-sdks.md](server-sdks.md) |
| Client RTC join          | Audio in/out                        | Official quickstart frontend or RTC refs                        |
| Client RTM + toolkit     | Transcripts, state, sendText        | [agent-toolkit.md](agent-toolkit.md)                            |
| Join payload shape       | LLM/TTS/ASR config, channel, tokens | Official quickstart or OpenAPI spec                             |

When adapting into an existing app, use [integration-from-quickstart.md](integration-from-quickstart.md) to map quickstart source files to your app paths before editing.

## Common Mistakes

- Generating `/join` payloads from memory instead of copying from the official quickstart source.
- Treating `POST /join` response as proof the agent is already audible in RTC.
- Using one RTC token for both the client and the ConvoAI `Authorization` header.
- Mismatching RTM login identity and RTM token subject.
- Enabling RTM in the project but omitting both RTM join flags.
- Calling client toolkit init before the server has started an agent.
