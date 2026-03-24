# Agora Skills

Structured reference knowledge for [Agora](https://www.agora.io) (agora.io) real-time AI and Communication SDKs, designed for AI coding assistants. Covers Conversational AI (voice AI agents), RTC (video/voice), RTM (signaling/messaging), and server-side token generation.

## Installation

### Skills CLI (recommended)

```bash
npx skills add github:AgoraIO/skills
```

Skills activate automatically when your agent detects relevant tasks (e.g., "build a voice agent", "integrate Agora RTC", "generate a token").

### Claude Code Plugin (recommended if using Claude)

Install Agora skills and the Agora Docs MCP server as a Claude Code plugin. Run these two slash commands inside Claude Code:

```
/plugin marketplace add AgoraIO/skills
/plugin install agora@agora-skills
```

The Agora MCP server (`mcp.agora.io`) is bundled automatically — no separate MCP configuration needed.

### Git clone

Clone the repo once, then point your tool at `skills/agora/`:

```bash
git clone https://github.com/AgoraIO/skills.git ~/agora-skills
```

### Configure with your Agent or IDE (optional)

**Claude Code — symlink (user-level):**

When installing the skill using the Skills CLI, you can symlink the skill to your home directory. This will make the skill available to all your agents.

```bash
ln -s ~/agora-skills/skills/agora ~/.claude/skills/agora
```

**Claude Code — copy (project-level, shared with team):**

When installing the skill using the Claude Code Plugin, you can copy the skill to your project directory. This will make the skill available to all your agents in the project.

```bash
mkdir -p .claude/skills
cp -r ~/agora-skills/skills/agora .claude/skills/agora
```

**Cursor:** Copy or symlink into `.cursor/rules/`. See [Cursor skills docs](https://cursor.com/docs/skills#skill-directories).

**Windsurf:** Add `skills/agora/` to your Cascade context. See [Windsurf skills docs](https://docs.windsurf.com/windsurf/cascade/skills).

**GitHub Copilot:** Reference via `@workspace` or add to `.github/copilot-instructions.md`. See [Copilot CLI skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-skills) and [Copilot Agents skills](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills).

**Any other tool:** The skill files are plain markdown. Point your tool at `skills/agora/` or load individual files directly. Use `SKILL.md` as the entry point — it links to everything else.

---

## What This Is

This repo contains markdown skill files that give AI coding assistants deep knowledge of Agora's platform. When a developer asks for help with Agora, the assistant loads the relevant reference material — from high-level product overviews down to platform-specific code examples and API details.

**Products covered:**

- **RTC (Video/Voice SDK)** — Web, React, Next.js, iOS (Swift), Android (Kotlin/Java), React Native, Flutter
- **RTM (Signaling)** — Web (JS/TS), iOS (Swift), Android (Kotlin) — all v2; messaging, presence, metadata, stream channels
- **Conversational AI** — REST API, agent config, Gemini Live + OpenAI Realtime MLLM, iOS/Android toolkits, 6 recipe repos (agent-samples, agent-toolkit, agent-client-toolkit-react, agent-ui-kit, server-custom-llm, server-mcp)
- **Cloud Recording** — REST API acquire/start/query/stop lifecycle
- **Server Gateway** — Linux SDK (C++) for server-side RTC
- **Server-Side** — Token generation for Node.js, Python, Go
- **Multi-Product Integration** — RTC + RTM + ConvoAI initialization order, UID strategy, codec selection, token matrix
- **Testing Guidance** — Mocking patterns for all platforms (Web, React, iOS, Android, React Native, Flutter, RTM)

## Design — 4-Layer Progressive Disclosure

LLM context windows are finite. Load the minimum needed, go deeper only when required.

| Layer                  | What                                                                | Size         | When Loaded          |
| ---------------------- | ------------------------------------------------------------------- | ------------ | -------------------- |
| **1 — Description**    | Trigger keywords in `SKILL.md` frontmatter                          | ~100 words   | Always (skill index) |
| **2 — SKILL.md body**  | Core concepts, product index, framework notes                       | ~72 lines    | On activation        |
| **3 — Product README** | Overview, critical rules, topic links                               | 20–100 lines | Per product          |
| **4 — Topic files**    | Implementation detail, code examples, API reference, or TOC + links | 34–500 lines | Per topic            |

Navigation: `SKILL.md` → product `README.md` → topic file (e.g., `web.md`, `agent-samples.md`).

### Link-First vs Inline

Not all content belongs inline. The skill uses two strategies depending on how fast upstream content moves and how well it's documented:

| Product               | Strategy                                 | Why                                           |
| --------------------- | ---------------------------------------- | --------------------------------------------- |
| **Conversational AI** | TOC + links to repo READMEs and AGENT.md | Fast-moving, 5 upstream repos with good docs  |
| **RTC / RTM**         | Inline code examples                     | Stable APIs, official docs lack good examples |
| **Server / Tokens**   | TOC + links to official docs             | Well-documented at docs.agora.io              |

ConvoAI files are aligned 1:1 with repos in [AgoraIO-Conversational-AI](https://github.com/orgs/AgoraIO-Conversational-AI/repositories). Each file maps to one repo and links to its README and AGENT.md as sources of truth. Gotchas and quirks that LLMs consistently get wrong stay inline in the ConvoAI README.

## File Structure

```
skills/
└── agora/                          Skill root
    ├── SKILL.md                    Entry point, product index (v1.2.0)
    ├── intake/
    │   └── SKILL.md                Multi-product needs analysis router
    └── references/
        ├── doc-fetching.md         Two-tier lookup procedure (agent-facing)
        ├── mcp-tools.md            MCP tool reference and graceful degradation
        ├── integration-patterns.md RTC+RTM+ConvoAI: init order, UID strategy, codec, tokens
        ├── rtc/                    RTC (Video/Voice SDK)
        │   ├── README.md           Critical rules, encoder profiles, cross-platform notes
        │   ├── web.md              agora-rtc-sdk-ng: client, tracks, events, screen share
        │   ├── react.md            agora-rtc-react: hooks, codec interop, custom patterns
        │   ├── nextjs.md           Next.js / SSR dynamic import patterns
        │   ├── ios.md              AgoraRtcEngineKit (Swift): setup, delegation
        │   ├── android.md          RtcEngine (Kotlin/Java): setup, callbacks
        │   ├── react-native.md     react-native-agora: engine init, events, video views
        │   ├── flutter.md          agora_rtc_engine (Dart): engine init, AgoraVideoView
        │   └── cross-platform-coordination.md  UID strategy, codec interop, screen share
        ├── rtm/                    RTM Signaling SDK v2
        │   ├── README.md           Key concepts, gotchas, platform links
        │   ├── web.md              agora-rtm v2: messaging, presence, stream channels
        │   ├── ios.md              AgoraRtmClientKit (Swift): init, login, subscribe, publish
        │   └── android.md          RtmClient (Kotlin): init, login, subscribe, publish
        ├── conversational-ai/      Conversational AI (Voice AI Agents)
        │   ├── README.md           Architecture, endpoints, auth, lifecycle, gotchas
        │   ├── agent-samples.md    Backend, React clients, profiles, MLLM, deployment
        │   ├── agent-toolkit.md    @agora/conversational-ai SDK: API, helpers, hooks
        │   ├── agent-client-toolkit-react.md   React hooks: provider, transcript, state
        │   ├── agent-ui-kit.md     @agora/agent-ui-kit React components
        │   ├── agent-toolkit-ios.md    iOS ConversationalAIAPIImpl Swift toolkit
        │   ├── agent-toolkit-android.md  Android ConversationalAIAPIImpl Kotlin toolkit
        │   ├── server-custom-llm.md  Custom LLM proxy: RAG, tools, memory
        │   ├── server-mcp.md       MCP memory server: persistent per-user memory
        │   ├── auth-flow.md        Three-token flow for direct REST API implementors
        │   ├── python-sdk.md       agora-agent Python SDK patterns
        │   ├── go-sdk.md           agora-agent-server-sdk-go patterns
        │   └── server-sdks.md      TypeScript/Node.js server SDK patterns
        ├── cloud-recording/        Cloud Recording (REST API)
        │   └── README.md           acquire/start/query/stop lifecycle, storage config
        ├── server-gateway/         Server Gateway (Linux SDK)
        │   ├── README.md           Overview, use cases, critical notes
        │   └── linux-cpp.md        C++ SDK: setup, callbacks, media pipeline
        ├── server/                 Server-Side (Tokens)
        │   ├── README.md           Token types, when tokens are needed
        │   └── tokens.md           Token generation TOC + links to official docs
        └── testing-guidance/       Testing Patterns
            └── SKILL.md            Mocking patterns: Web, React, iOS, Android, RN, Flutter, RTM
```

## Maintaining and Extending

### Adding a New Product

1. Create `references/{product}/README.md` (Layer 3)
2. Add an entry to the **Products** section of `SKILL.md`
3. Create topic files as needed (Layer 4)

### Adding a New Platform

1. Create `references/{product}/{platform}.md` (Layer 4)
2. Add a link in the product's `README.md`

### Updating Content

- Edit the specific Layer 4 file.
- **Inline files** (RTC, RTM, TEN): Keep code examples current, keep **Official Documentation** URLs at the bottom.
- **Link-first files** (ConvoAI, server): Update TOC links when upstream repos restructure. Keep gotchas/quirks inline only for things LLMs get wrong that aren't obvious in upstream docs.
- Don't duplicate content that lives in upstream repo READMEs or AGENT.md — link to it instead.

### Verifying URLs

```bash
grep -roh 'https://[^ )]*' skills/ | sort -u | while read url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 10 "$url")
  echo "$code $url"
done
```

### Agora Release Notes

- Conversational AI: https://docs.agora.io/en/conversational-ai/overview/release-notes
- Video SDK: https://docs.agora.io/en/video-calling/overview/release-notes
- Signaling (RTM): https://docs.agora.io/en/signaling/overview/release-notes
