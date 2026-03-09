# Agora Conversational AI Engine

REST API-driven voice AI agents. Create agents that join RTC channels and converse with users via speech. Front-end clients connect via RTC+RTM.

## Architecture

```text
Your Server (REST API calls)
    ↓ POST /join with config
Agora ConvoAI Engine
    ↓ creates agent
Agent joins RTC channel ←→ Front-end client (RTC + RTM)
    ↓                           ↓
ASR → LLM → TTS             Receives audio + transcripts
```

1. Your server calls the REST API to create an agent with LLM/TTS/ASR config
2. The agent joins an Agora RTC channel and subscribes to the user's audio
3. ASR converts speech to text → LLM generates response → TTS converts to speech
4. The agent publishes audio back to the channel; transcripts arrive via RTC data channel or RTM

## MCP Integration

The ConvoAI REST API documentation is fast-moving. Use MCP to fetch current parameter
details rather than relying on inline content.

**When MCP is available:** Call `get-doc-content` with the Quick Start URI for your language:

- Python/curl: `docs://default/convoai/restful/get-started/quick-start`
- Go: `docs://default/convoai/restful/get-started/quick-start-go`
- Java: `docs://default/convoai/restful/get-started/quick-start-java`

**When MCP is unavailable:**

1. Fetch the live OpenAPI spec: `https://docs-md.agora.io/api/conversational-ai-api-v2.x.yaml`
2. Fall back to: <https://docs.agora.io/en/conversational-ai/develop/rest-api>
3. Notify the user: "MCP unavailable — using local fallback. Please verify against
   current docs before deploying."

The behavioral guidance and gotchas in this file (uid types, agent name uniqueness, MLLM location field, etc.) are always valid regardless of MCP status.

See [../mcp-tools.md](../mcp-tools.md) for full MCP tool reference.

## Authentication

Two methods are supported. **Token-based auth is preferred** — it avoids storing long-lived Customer Secret credentials on your server.

### Option A: Agora Token (recommended)

Use a combined RTC + RTM token generated with `RtcTokenBuilder.buildTokenWithRtm` from the [`agora-token`](https://www.npmjs.com/package/agora-token) npm package:

```javascript
import { RtcTokenBuilder, RtcRole } from 'agora-token';

const token = RtcTokenBuilder.buildTokenWithRtm(
  appId, appCertificate, channelName, account, RtcRole.PUBLISHER,
  tokenExpire, privilegeExpire
);

const response = await fetch(
  `${baseUrl}/${appId}/join`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `agora token=${token}`,
    },
    body: JSON.stringify(requestBody),
  }
);
```

> **Note:** Token-based auth for ConvoAI REST API calls is not yet in official docs (pending release). The behavior is stable — `Authorization: agora token=<RTC+RTM token>` is accepted by the ConvoAI endpoint. Verify against official docs once published.

See [../server/tokens.md](../server/tokens.md) for `buildTokenWithRtm` parameter reference.

### Option B: HTTP Basic Auth (Customer ID + Secret)

- Credentials: Customer ID + Customer Secret from [Agora Console](https://console.agora.io) → Developer Toolkit → RESTful API
- Header: `Authorization: Basic <base64(customerID:customerSecret)>`
- HTTPS required (TLS 1.0/1.1/1.2)

## Base URL

```text
https://api.agora.io/api/conversational-ai-agent/v2/projects/{appid}
```

## Agent Lifecycle

| Status     | Code | Description                |
| ---------- | ---- | -------------------------- |
| IDLE       | 0    | Ready, not active          |
| STARTING   | 1    | Initialization in progress |
| RUNNING    | 2    | Active, processing audio   |
| STOPPING   | 3    | Shutdown in progress       |
| STOPPED    | 4    | Exited channel             |
| RECOVERING | 5    | Error recovery             |
| FAILED     | 6    | Execution failure          |

## REST API Endpoints

| Method | Path                          | Description                      |
| ------ | ----------------------------- | -------------------------------- |
| POST   | `/join`                       | Start agent — joins channel      |
| POST   | `/agents/{agentId}/leave`     | Stop agent — leaves channel      |
| POST   | `/agents/{agentId}/update`    | Update agent config (token, LLM) |
| GET    | `/agents/{agentId}`           | Query agent status               |
| GET    | `/agents`                     | List agents (with filters)       |
| POST   | `/agents/{agentId}/speak`     | Broadcast TTS message            |
| POST   | `/agents/{agentId}/interrupt` | Interrupt agent speech           |
| GET    | `/agents/{agentId}/history`   | Get conversation history         |

## Reference Files

Each file maps to one repo in [AgoraIO-Conversational-AI](https://github.com/AgoraIO-Conversational-AI):

- **[agent-samples.md](agent-samples.md)** — Backend (simple-backend), React clients, profile system, MLLM/Gemini config, deployment
- **[agent-toolkit.md](agent-toolkit.md)** — `agora-agent-client-toolkit` + `agora-agent-client-toolkit-react`: AgoraVoiceAI, events, transcript, sendText, interrupt, React hooks
- **[agent-client-toolkit-react.md](agent-client-toolkit-react.md)** — React hooks detail: ConversationalAIProvider, useTranscript, useAgentState, useAgentError, useAgentMetrics, useConversationalAI
- **[agent-ui-kit.md](agent-ui-kit.md)** — `@agora/agent-ui-kit` React components: voice, chat, video, settings
- **[server-custom-llm.md](server-custom-llm.md)** — Custom LLM proxy: RAG, tool calling, conversation memory
- **[server-mcp.md](server-mcp.md)** — MCP memory server: persistent per-user memory via tool calling

## REST API Reference

Full request/response details for all endpoints:

- **[Start Agent (Join)](https://docs.agora.io/en/conversational-ai/rest-api/agent/join)** — POST /join: start agent with LLM/TTS/ASR config
- **[Stop Agent (Leave)](https://docs.agora.io/en/conversational-ai/rest-api/agent/leave)** — POST /leave: stop agent
- **[Update Agent](https://docs.agora.io/en/conversational-ai/rest-api/agent/update)** — POST /update: update token, LLM config
- **[Query Agent Status](https://docs.agora.io/en/conversational-ai/rest-api/agent/query)** — GET /agents/{id}: query status
- **[List Agents](https://docs.agora.io/en/conversational-ai/rest-api/agent/list)** — GET /agents: list with filters
- **[Broadcast Message (Speak)](https://docs.agora.io/en/conversational-ai/rest-api/agent/speak)** — POST /speak: broadcast TTS
- **[Interrupt Agent](https://docs.agora.io/en/conversational-ai/rest-api/agent/interrupt)** — POST /interrupt
- **[Conversation History](https://docs.agora.io/en/conversational-ai/rest-api/agent/history)** — GET /history

## Agent Configuration (join payload `properties` object)

- **[Custom LLM Guide](https://docs.agora.io/en/conversational-ai/develop/custom-llm)** — LLM vendor, model, url, api_key, system prompt, greeting, style; TTS vendor, model, voice settings; ASR vendor, language, model
- **[Gemini Live MLLM](https://docs.agora.io/en/conversational-ai/models/mllm/gemini)** — Multimodal: vendor, model, credentials, location
- **[Join Endpoint (full schema)](https://docs.agora.io/en/conversational-ai/rest-api/agent/join)** — Complete properties schema: channel, token, turn detection, VAD, tools, avatars, encryption, filler words
- **[Release Notes](https://docs.agora.io/en/conversational-ai/overview/release-notes)** — New parameters and features

## Gotchas & Quirks

Things the official docs don't emphasize that cause frequent mistakes:

- **Token auth is not in the official docs yet — use it anyway.** The ConvoAI REST API accepts `Authorization: agora token=<token>` using a combined RTC + RTM token from `RtcTokenBuilder.buildTokenWithRtm`. This is **safer than Basic Auth**: tokens are scoped to a single App ID + channel, while Customer ID/Secret grants access to every project on the account. Default to token auth unless the user explicitly requests Basic Auth. See [Authentication → Option A](#authentication) for the implementation.

- **`/update` overwrites `params` entirely** — sending `{ "llm": { "params": { "max_tokens": 2048 } } }` erases `model` and everything else in `params`. Always send the full object.
- **`/speak` priority enum** — `"INTERRUPT"` (immediate, default), `"APPEND"` (queued after current speech), `"IGNORE"` (skip if agent is busy). `interruptable: false` prevents users from cutting in.
- **20 PCU default limit** — max 20 concurrent agents per App ID. Exceeding returns error on `/join`. Contact Agora support to increase.
- **Event notifications require two flags** — `advanced_features.enable_rtm: true` AND `parameters.data_channel: "rtm"` in the join config. Without both, `onAgentStateChanged`/`onAgentMetrics`/`onAgentError` won't fire. Additionally: `parameters.enable_metrics: true` for metrics, `parameters.enable_error_message: true` for errors.
- **Custom LLM interruptable metadata** — the first SSE chunk can be `{"object": "chat.completion.custom_metadata", "metadata": {"interruptable": false}}` to prevent user speech from interrupting critical responses (e.g., compliance disclaimers). Subsequent chunks use standard `chat.completion.chunk` format.
- **Error response format** — non-200 responses return `{ "detail": "...", "reason": "..." }`.
- **MLLM `location` not `region`** — use `params.location: "us-central1"`, not `region`. The field name is `location` at every level (join payload and backend env vars).

For test setup and mocking patterns, see [references/testing-guidance/SKILL.md](../testing-guidance/SKILL.md).
