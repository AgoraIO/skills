---
name: conversational-ai-quickstarts
description: |
  Locked quickstart flow for Agora Conversational AI when the user does not yet have a proven
  working baseline. Use for new projects and integrations where the ConvoAI path has not been
  proven end to end. Restricts the model to one decision group per turn: baseline path,
  project readiness, then backend path only if needed. Do not generate code or custom
  architecture before the quickstart gates are resolved.
license: MIT
metadata:
  author: agora
  version: '1.1.0'
---

# Conversational AI Quickstart

Use this file for `quickstart` and `integration` mode from [README.md](README.md).

## Working-Baseline Rule

A **working ConvoAI baseline** means the developer has already started an Agora ConvoAI agent successfully and the client can join the same RTC channel and interact with it.

The following do **not** count as a working baseline:

- only RTC code exists
- a sample repo is cloned but the agent has never started successfully
- environment variables are present but unverified
- the user only knows the desired backend language or framework

If the user already has a working baseline, exit this file and route back through [README.md](README.md).

## Sequence

Follow this exact user-visible order:

1. Product intro in plain language
2. Baseline-path confirmation
3. Project-readiness checkpoint
4. Vendor-path confirmation — **skip if the user has not mentioned BYOK, providers, or Studio Agent ID; reseller defaults apply automatically**
5. Vendor selection, only if the user asks for the current provider list or chooses a non-default path
6. Studio Agent ID confirmation, only if the user wants to reuse an agent configured in Agora Studio
7. Backend-path confirmation, only if a separate backend or existing-repo integration still needs it
8. Structured quickstart spec

## Interaction Rules

- One decision group per turn. Do not ask baseline, credentials, and backend path in the same reply.
- Skip anything the user already answered.
- **Auto-skip `vendor_defaults`**: if the user has not mentioned BYOK, vendor API keys, a specific provider, or a Studio Agent ID, skip the vendor gate entirely and use reseller defaults. Do not ask about providers when the user just wants the fastest path.
- Infer obvious context from the user's stack or repository description.
- Mirror the user's language.
- While quickstart is unresolved, do **not** generate `/join` payloads, SDK code, custom file structures, clone commands, or repo adaptation plans.
- While quickstart is unresolved, read only this file and [README.md](README.md).
- Existing-app requests stay in quickstart until the ConvoAI path is proven once.
- Unless the user explicitly asks for BYOK (bring your own key) or a different provider stack, anchor on the defaults first — no vendor API keys needed.
- If `baseline_path=full-stack-nextjs`, keep the official sample's env var names. Do **not** rename them to generic provider-reference placeholders during quickstart.
- For non-default provider selection, fetch the official current provider docs before confirming support or generating config details.
- If the user already has an **Agora Studio Agent ID** from `https://console.agora.io/studio/agents`, treat that as a separate quickstart branch. Do not re-ask STT/LLM/TTS provider choices unless the user explicitly wants to replace the Studio-managed config.

## First-Success Vendor Defaults

The official `agent-quickstart-nextjs` sample works out of the box with just Agora credentials.
Vendor API calls (STT, LLM, TTS) go through Agora by default — no vendor API keys needed.

Default pipeline:

- **STT:** Deepgram nova-3
- **LLM:** OpenAI gpt-4o-mini
- **TTS:** MiniMax speech_2_6_turbo

BYOK (Bring Your Own Key) is supported but optional. The sample includes commented-out
BYOK blocks for Deepgram, OpenAI, and ElevenLabs. Users who want to use their own vendor
API keys can uncomment those blocks and provide them.

BYOK provider families visible in the current sample and SDK docs:

- **STT:** Deepgram (BYOK)
- **LLM:** OpenAI (BYOK)
- **TTS:** ElevenLabs (BYOK), Microsoft
- **MLLM:** OpenAI Realtime, Google Gemini Live

Use this rule during quickstart:

- For the first end-to-end success path, prefer the **default pipeline** (no vendor keys).
- Only switch to BYOK during quickstart if the user explicitly asks for it or names a specific vendor key they want to use.
- Only switch away from the default cascading pipeline if the user explicitly asks for MLLM.
- For the current provider matrix or vendor-specific configs, fetch the official live docs before claiming support or listing parameters.

## Env Name Policy

Use different rules depending on whether the user is staying sample-aligned or generating custom code.

### Sample-aligned path (`full-stack-nextjs`)

Keep the official sample's env names as the source of truth.

Default (no vendor keys needed):

```bash
NEXT_PUBLIC_AGORA_APP_ID=
NEXT_AGORA_APP_CERTIFICATE=
# Optional:
# NEXT_PUBLIC_AGENT_UID=123456
# NEXT_AGENT_GREETING=
```

BYOK mode (only if the user explicitly opts in):

```bash
NEXT_PUBLIC_AGORA_APP_ID=
NEXT_AGORA_APP_CERTIFICATE=
NEXT_DEEPGRAM_API_KEY=
NEXT_OPENAI_API_KEY=
NEXT_OPENAI_URL=
NEXT_ELEVENLABS_API_KEY=
NEXT_ELEVENLABS_VOICE_ID=
```

Do **not** prompt for vendor API keys unless the user explicitly asks for BYOK.
Do **not** rename these env vars to a different custom scheme during quickstart.

### Custom-code path

If the user is no longer sample-aligned and needs provider-specific config layout, fetch the current official ConvoAI provider docs and use those as the source of truth.

## Baseline Paths

| Path | Use when | After quickstart completes |
|---|---|---|
| `full-stack-nextjs` | Best default for a new project or prototype | Continue with Path A in this file, then use [agent-toolkit.md](agent-toolkit.md) or [server-sdks.md](server-sdks.md) for customization |
| `separate-backend-frontend` | The user explicitly wants a separate server and client | Use Path B if Python fits, or combine [agent-samples.md](agent-samples.md) with the backend file chosen later |
| `existing-app-integration` | The user already has an app or repo, but ConvoAI is not working yet | Keep the implementation sample-aligned; use [agent-samples.md](agent-samples.md) plus the backend file chosen later |

## State Machine

The quickstart is a blocking state machine. While a state is unresolved, the only allowed action is to send the next prompt for that state and wait for the user's reply.

| State | Allowed | Forbidden | Next prompt | Advance when |
|---|---|---|---|---|
| `intro` | Give a short plain-language intro to what ConvoAI is | Code, repo plans, framework recommendations | Product intro text | Intro delivered |
| `baseline_path` | Ask which baseline path to use | Code, clone steps, provider discussions | Baseline-path prompt | User picks A/B/C or gives equivalent clear context |
| `project_readiness` | Ask about App ID, App Certificate, and ConvoAI activation | Code, repo inspection, backend implementation | Readiness prompt | User confirms ready or asks where to find them |
| `vendor_defaults` | Ask whether to use the defaults (no vendor keys), BYOK, show the current official provider list, choose a non-default cascading / MLLM path, or reuse a Studio Agent ID. **Skip this gate entirely if the user has not mentioned BYOK, providers, or Studio Agent ID — defaults apply automatically.** | Code, implementation | Vendor-defaults prompt | User picks A/B/C/D/E, directly names a provider path / Studio Agent ID path, or gate is auto-skipped |
| `vendor_selection` | Collect only provider-mode and provider choices after checking the official current provider docs | Code, implementation, secret collection | Custom-provider prompt | Provider mode and provider names are resolved |
| `studio_agent_id` | Collect the Agora Studio Agent ID and confirm the user wants Studio to remain the source of truth for agent config | Code, re-asking provider setup from scratch | Studio-Agent-ID prompt | The Studio Agent ID path is resolved |
| `backend_path` | Ask for backend path only if still needed | Code, detailed implementation | Backend-path prompt | Backend path is clear or no longer needed |
| `complete` | Emit structured spec and continue to the mapped reference file | Re-open resolved gates | None | Spec emitted |

### Pre-Action Self-Check

Before every tool call or user-visible reply:

1. What is the current state?
2. Is the intended action allowed in that state?
3. If not, send the state prompt instead.

### Failure Branches

- If the user says they cloned a repo but never got an agent running, stay in quickstart.
- If the user asks for code before quickstart resolves, answer with the next gate instead of generating code.
- If a reply only partially resolves the current gate, ask a narrow follow-up for the missing field only.
- If the user names a provider that is not in the current official provider docs, say this clearly: it is **not currently documented as supported in the official Agora ConvoAI provider docs**, so do not proceed as if it is supported. Offer the documented default combo or a live-doc verification path.
- If the user asks to see the provider list, fetch the current official provider docs and stay in the vendor gate until they accept the default combo or choose a documented alternative.
- If the user says they already have an Agora Studio Agent ID, switch to the `studio_agent_id` state and stop re-asking provider-vendor questions unless they explicitly say they want to replace the Studio-managed config.
- If the user changes the baseline-path assumption later (for example, picks Path A first and later insists on a separate Python backend), return to `baseline_path` and re-confirm instead of silently drifting paths.
- If the user chooses Path B but does not have access to the private repo, keep the quickstart state intact and continue with the public `agent-samples` fallback only after stating that the private baseline is unavailable.

## Prompt Templates

### Product Intro

Keep it short. Explain that ConvoAI is a server-managed voice agent that joins an RTC channel, speaks through TTS, and usually pairs an RTC client with a backend that starts the agent.

Use a natural transition into quickstart. Preferred tone:

- Avoid saying "run the baseline flow" or "anchor on a proven baseline" to the user.
- Prefer "let's first use the official sample to get the whole link working once" language.

Suggested transition line:

```text
Before we jump into custom code, let's first use the official sample to get the whole flow working once. Once the agent can join the channel and finish one real conversation, we can turn that working version into your demo.
```

### Baseline Path

```text
Before we customize anything, let's first use an official sample to get the full ConvoAI flow working once:
A. Use the official full-stack Next.js quickstart
B. Use a separate backend + frontend baseline (private Python repo if you have access; otherwise we will fall back to the public decomposed sample)
C. Adapt an existing app/repo, but keep it sample-aligned until ConvoAI works end to end
```

### Project Readiness

```text
Before we continue, confirm these prerequisites:
- App ID: your Agora project identifier
- App Certificate: required for production-safe token generation
- ConvoAI activation: the project must have Conversational AI enabled

A. All ready
B. Not yet — tell me where to get them
```

### Backend Path

Use only if the baseline path still leaves the backend unclear.

```text
Which backend path should we optimize for after the baseline is chosen?
A. TypeScript / Node.js
B. Python
C. Go
D. Another backend language / direct REST
```

### Vendor Defaults

Use this only if the user has mentioned BYOK, vendor API keys, a specific provider, or a Studio Agent ID. If none of these were mentioned, skip this prompt entirely and use reseller defaults.

```text
The official quickstart works out of the box with just Agora credentials — no vendor API keys needed.

Default pipeline:
- STT: Deepgram nova-3
- LLM: OpenAI gpt-4o-mini
- TTS: MiniMax speech_2_6_turbo

A. Use the defaults (no vendor keys needed — fastest path)
B. I want to use my own vendor API keys (BYOK)
C. Show me the current official provider list first
D. I want to choose a non-default cascading or MLLM path
E. I already have an Agora Studio Agent ID and want to reuse that Studio-managed agent
```

### Custom Provider Prompt

Use only after the user picks `C` or directly asks for non-default providers.

```text
First check the current official ConvoAI provider docs, then choose from the documented provider modes:
- Cascading path: STT + LLM + TTS
- MLLM path: OpenAI Realtime or Google Gemini Live

Then choose the documented providers for that mode using the current official docs as the source of truth.

Reply in one line, for example:
- `TTS: Microsoft`
- `MLLM: OpenAI Realtime`
- `STT: Deepgram, LLM: OpenAI, TTS: Microsoft`
```

### Studio Agent ID Prompt

Use only when the user picks `D` or directly says they already have an Agora Studio Agent ID.

```text
If you already configured the agent in Agora Studio, we can treat Studio as the source of truth for the agent configuration instead of rebuilding the provider stack here.

Open `https://console.agora.io/studio/agents`, find the agent you want to reuse, and copy its **Agent ID**.

Important:
- This **Studio Agent ID** is different from the runtime `agent_id` returned by `/join`.
- The Studio Agent ID identifies the Studio-managed agent configuration and maps to the request field `pipeline_id`.
- The runtime `agent_id` identifies a live started session.

Reply with one of these:
A. I have the Studio Agent ID — here it is: `<agent-id>`
B. I need to look it up in Studio first
C. Go back — I want to use the default/provider path instead
```

### Unsupported Provider Prompt

Use this when the user names a provider that is not in the current official provider docs.

```text
That provider is not in the current official Agora ConvoAI provider docs, so I should not proceed as if it is supported.

You can choose one of these paths:
A. Use the documented default combo to get the first demo working
B. Show the current official provider list first
C. Re-check the latest official docs to verify whether that provider is supported now
```

## Output: Structured Quickstart Spec

After all gates are resolved, normalize the result into a short spec and continue automatically.

```yaml
use_case: [text]
mode: [quickstart | integration]
proven_working_baseline: no
baseline_path: [full-stack-nextjs | separate-backend-frontend | existing-app-integration]
frontend: [nextjs-react | standalone-react | existing-app | unknown]
backend: [typescript-node | python | go | direct-rest | unknown]
project_readiness:
  app_id: [ready | missing | unknown]
  app_certificate: [ready | missing | unknown]
  convoai_activation: [ready | missing | unknown]
key_mode: [default | byok | unknown]
providers:
  pipeline: [cascading | mllm | unknown]
  stt: [deepgram | user-specified-supported | unknown]
  llm: [openai | user-specified-supported | unknown]
  tts: [minimax | elevenlabs | microsoft | user-specified-supported | unknown]
  mode: [default | byok-default | user-specified-cascading | mllm | unknown]
studio_agent:
  use_existing_agent_id: [yes | no | unknown]
  agent_id: [text | missing | unknown]
config_style: [sample-aligned | custom-path | unknown]
```

Notes:

- `stt` is the SDK-facing name in this quickstart spec. Platform docs may call the same stage `ASR`.
- `studio_agent.agent_id` means the **Agora Studio Agent ID** from `https://console.agora.io/studio/agents`, not the runtime `agent_id` returned by `/join`.
- When this Studio path is used, that Studio Agent ID maps to the request field `pipeline_id`.
- `AGORA_STUDIO_AGENT_ID` is the preferred config placeholder name for this path; the request field remains `pipeline_id`.
- `config_style` is derived from the chosen baseline path unless the user explicitly overrides it later:
  `full-stack-nextjs` and `existing-app-integration` usually imply `sample-aligned`;
  fully custom provider configuration usually implies `custom-path`.

## After Collection

Route according to the completed spec:

- `full-stack-nextjs` → stay in Path A below. Use [server-sdks.md](server-sdks.md) only if the user later customizes the server-side API routes.
- `separate-backend-frontend` + `python` → use Path B below, then [python-sdk.md](python-sdk.md) for backend details.
- `separate-backend-frontend` + `typescript-node` → use [agent-samples.md](agent-samples.md) for the decomposed app shape, then [server-sdks.md](server-sdks.md).
- `separate-backend-frontend` + `go` → use [agent-samples.md](agent-samples.md) for client structure, then [go-sdk.md](go-sdk.md).
- existing Agora Studio Agent ID → use [conversational-ai-studio.md](conversational-ai-studio.md).
- provider selection or parameter confirmation → fetch the current official ConvoAI provider docs.
- `direct-rest` → use [auth-flow.md](auth-flow.md).
- `existing-app-integration` → keep changes sample-aligned with [agent-samples.md](agent-samples.md) until the first successful end-to-end ConvoAI session.

## Path A — Full-Stack Next.js (Default)

**Repo:** <https://github.com/AgoraIO-Conversational-AI/agent-quickstart-nextjs>

Single Next.js application covering token generation, agent lifecycle API routes, and the React UI. This is the best starting point for most new projects.

> **Note:** Agora SDKs are browser-only. If you add custom RTC components, follow the SSR patterns in [../rtc/nextjs.md](../rtc/nextjs.md).

> **agent-quickstart-nextjs vs. agent-samples**: `agent-quickstart-nextjs` is a single self-contained Next.js app with API routes. `agent-samples` is a decomposed baseline with a separate backend and client apps. Use [agent-samples.md](agent-samples.md) only when the quickstart spec requires that structure.

### What's Included

- Next.js API routes for token generation (`/api/generate-agora-token`), agent start (`/api/invite-agent`), and agent stop (`/api/stop-conversation`)
- React UI with live transcription, audio visualization, device selection, and mobile-responsive chat
- `agora-agent-uikit`, `agora-agent-client-toolkit`, and `agora-agent-server-sdk` pre-wired
- Dual RTC + RTM token auth
- One-click Vercel deployment

### Stack

- **Framework:** Next.js (TypeScript)
- **UI:** Tailwind CSS + shadcn/ui
- **Real-time:** Agora RTC + RTM
- **Default pipeline (reseller):** Deepgram nova-3 (STT), OpenAI gpt-4o-mini (LLM), MiniMax speech_2_6_turbo (TTS)
- **BYOK option:** Deepgram (STT), OpenAI (LLM), ElevenLabs (TTS) — uncomment in `invite-agent/route.ts`

### Setup

```bash
git clone https://github.com/AgoraIO-Conversational-AI/agent-quickstart-nextjs.git
cd agent-quickstart-nextjs
pnpm install
cp env.local.example .env.local
# Edit .env.local — only NEXT_PUBLIC_AGORA_APP_ID and NEXT_AGORA_APP_CERTIFICATE are required
pnpm dev
```

Open `http://localhost:3000`.

**Requirements:** Node.js 22.x+, pnpm 8.x+

### Environment Variables

Default (only Agora credentials needed):

```bash
# Required
NEXT_PUBLIC_AGORA_APP_ID=
NEXT_AGORA_APP_CERTIFICATE=

# Optional
NEXT_PUBLIC_AGENT_UID=123456
NEXT_AGENT_GREETING=
```

BYOK mode (uncomment the BYOK blocks in `app/api/invite-agent/route.ts` first):

```bash
# Required (same as above)
NEXT_PUBLIC_AGORA_APP_ID=
NEXT_AGORA_APP_CERTIFICATE=

# Vendor keys (required for BYOK)
NEXT_DEEPGRAM_API_KEY=
NEXT_OPENAI_API_KEY=
NEXT_OPENAI_URL=https://api.openai.com/v1/chat/completions
NEXT_ELEVENLABS_API_KEY=
NEXT_ELEVENLABS_VOICE_ID=
```

> The App Certificate is required for token generation. Get both from [Agora Console](https://console.agora.io).
> When staying on this sample-aligned path, do not rename these env vars to a different custom provider env scheme during quickstart.

## Path B — Python Backend + React Frontend (Private Repo)

**Repo:** <https://github.com/AgoraIO-Community/conversational-ai-quickstart> *(private — contact your Agora developer relations or solutions engineer contact to request access)*

Use this when you specifically need a separate Python backend and a standalone React frontend deployed independently.

- Python backend handles token generation and agent lifecycle via the ConvoAI REST API
- React frontend connects via RTC + RTM
- Refer to the repo README for setup once you have access

If access to the private repo is unavailable, keep the quickstart spec and fall back to [agent-samples.md](agent-samples.md) for the public decomposed baseline, then use [python-sdk.md](python-sdk.md) for backend behavior.

## After the Baseline Works

Once the first end-to-end ConvoAI session works, route by task:

| Next step | Reference |
|---|---|
| Customize LLM, TTS, ASR vendor or model | Fetch `https://docs-md.agora.io/en/conversational-ai/develop/custom-llm.md` |
| Add transcript rendering or agent state to a custom UI | [agent-toolkit.md](agent-toolkit.md) |
| Use React hooks (`useTranscript`, `useAgentState`) | [agent-client-toolkit-react.md](agent-client-toolkit-react.md) |
| Swap in pre-built React UI components | [agent-ui-kit.md](agent-ui-kit.md) |
| Add a custom LLM backend (RAG, tool calling) | [server-custom-llm.md](server-custom-llm.md) |
| Production token generation | [../server/tokens.md](../server/tokens.md) |
| Full REST API reference | [README.md](README.md#rest-api-endpoints) |
