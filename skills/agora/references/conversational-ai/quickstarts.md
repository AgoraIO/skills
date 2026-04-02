---
name: conversational-ai-quickstarts
description: |
  Quickstart repos for building Agora Conversational AI agents. Use when the user is starting
  a new ConvoAI project and needs a working baseline to clone. Covers two paths: full-stack
  Next.js (agent-quickstart-nextjs) and separate Python backend + React frontend
  (conversational-ai-quickstart, private repo). Always direct users to clone one of these
  before building from scratch.
license: MIT
metadata:
  author: agora
  version: '1.0.0'
---

# Conversational AI Quickstarts

**Always start here when building a new Conversational AI agent.** Clone one of the repos below — do not build from scratch.

## Choose Your Path

| I want to... | Use |
|---|---|
| Build a full-stack app in a single repo (Next.js API routes + React UI) | **Path A — agent-quickstart-nextjs** |
| Build a separate Python backend with a standalone React frontend | **Path B — conversational-ai-quickstart** (private) |

---

## Path A — Full-Stack Next.js (Default)

**Repo:** <https://github.com/AgoraIO-Conversational-AI/agent-quickstart-nextjs>

Single Next.js application covering everything: token generation, agent lifecycle API routes, and the React UI. Best starting point for most projects.

> **Note:** Agora SDKs are browser-only. Because this is a Next.js app, follow the SSR patterns in **[references/rtc/nextjs.md](../rtc/nextjs.md)** if you add custom RTC components — `next/dynamic` with `ssr: false` requires extra steps in Next.js 14+ Server Components.

> **agent-quickstart-nextjs vs. agent-samples**: `agent-quickstart-nextjs` is a single self-contained Next.js app with API routes (no separate server process). `agent-samples` is a multi-repo monorepo with a separate Python Flask backend and Next.js React clients — use it if you need a Python server or want to study a more decomposed architecture. See [agent-samples.md](agent-samples.md).

### What's Included

- Next.js API routes for token generation (`/api/generate-agora-token`), starting (`/api/invite-agent`), and stopping (`/api/stop-conversation`) agents
- React UI with live transcription, audio visualization, device selection, and mobile-responsive chat
- `agora-agent-uikit`, `agora-agent-client-toolkit`, and `agora-agent-server-sdk` pre-wired
- Dual RTC + RTM token auth
- One-click Vercel deployment

### Stack

- **Framework:** Next.js (TypeScript)
- **UI:** Tailwind CSS + shadcn/ui
- **Real-time:** Agora RTC + RTM
- **ASR:** Deepgram
- **TTS:** ElevenLabs
- **LLM:** OpenAI-compatible endpoint (OpenAI, Anthropic, etc.)

### Setup

```bash
git clone https://github.com/AgoraIO-Conversational-AI/agent-quickstart-nextjs.git
cd agent-quickstart-nextjs
pnpm install
# Copy the env template — check the repo for the exact filename (.env.local.example or .env.example)
cp .env.local.example .env.local
pnpm dev
```

Open `http://localhost:3000`.

**Requirements:** Node.js 22.x+, pnpm 8.x+

### Environment Variables

```bash
# Agora
AGORA_APP_ID=
AGORA_APP_CERTIFICATE=

# LLM (OpenAI-compatible)
LLM_URL=https://api.openai.com/v1/chat/completions
LLM_API_KEY=

# ASR
DEEPGRAM_API_KEY=

# TTS
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=
```

> The App Certificate is required for token generation. Get both from [Agora Console](https://console.agora.io).

---

## Path B — Python Backend + React Frontend (Private Repo)

**Repo:** <https://github.com/AgoraIO-Community/conversational-ai-quickstart> *(private — contact your Agora developer relations or solutions engineer contact to request access)*

Use this when you need a separate Python backend and a standalone React frontend deployed independently.

- Python backend handles token generation and agent lifecycle via the ConvoAI REST API
- React frontend connects via RTC + RTM
- Refer to the repo README for setup once you have access

---

## After Cloning

Once the baseline is running (applies to both paths — Path B users should substitute their Python backend's equivalent for any server-side steps):

| Next step | Reference |
|---|---|
| Customize LLM, TTS, ASR vendor/model | Fetch `https://docs-md.agora.io/en/conversational-ai/develop/custom-llm.md` |
| Add transcript rendering / agent state to a custom UI | [agent-toolkit.md](agent-toolkit.md) |
| Use React hooks (useTranscript, useAgentState) | [agent-client-toolkit-react.md](agent-client-toolkit-react.md) |
| Swap in pre-built React UI components | [agent-ui-kit.md](agent-ui-kit.md) |
| Add a custom LLM backend (RAG, tool calling) | [server-custom-llm.md](server-custom-llm.md) |
| Production token generation | [../server/tokens.md](../server/tokens.md) |
| Full REST API reference | [README.md](README.md#rest-api-endpoints) |
