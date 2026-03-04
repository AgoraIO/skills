# Agora Skills

Structured reference knowledge for [Agora](https://www.agora.io) (agora.io) real-time AI and Communication SDKs, designed for AI coding assistants. Covers Conversational AI (voice AI agents), RTC (video/voice), RTM (signaling/messaging), and server-side token generation.

## Installation

### Option A: Skills CLI (recommended)

```bash
npx skills add github:AgoraIO-Conversational-AI/skills
```

Skills activate automatically when your agent detects relevant tasks (e.g., "build a voice agent", "integrate Agora RTC", "generate a token").

### Option B: Git clone

Clone the repo once, then point your tool at `skills/agora/`:

```bash
git clone https://github.com/AgoraIO-Conversational-AI/skills.git ~/agora-skills
```

**Claude Code — symlink (user-level):**

```bash
mkdir -p ~/.claude/skills
ln -s ~/agora-skills/skills/agora ~/.claude/skills/agora
```

**Claude Code — copy (project-level, shared with team):**

```bash
mkdir -p .claude/skills
cp -r ~/agora-skills/skills/agora .claude/skills/agora
```

**Cursor:** Copy or symlink into `.cursor/rules/`.

**Windsurf:** Add `skills/agora/` to your Cascade context.

**GitHub Copilot:** Reference via `@workspace` or add to `.github/copilot-instructions.md`.

**Any other tool:** The skill files are plain markdown. Point your tool at `skills/agora/` or load individual files directly. Use `SKILL.md` as the entry point — it links to everything else.

---

## What This Is

This repo contains markdown skill files that give AI coding assistants deep knowledge of Agora's platform. When a developer asks for help with Agora, the assistant loads the relevant reference material — from high-level product overviews down to platform-specific code examples and API details.

**Products covered:**

- **RTC (Video/Voice SDK)** — Web, React, iOS (Swift), Android (Kotlin/Java)
- **RTM (Signaling)** — Web (JS/TS) messaging, presence, metadata, stream channels
- **Conversational AI** — REST API, agent config, 5 recipe repos (agent-samples, agent-toolkit, agent-ui-kit, server-custom-llm, server-mcp)
- **Server-Side** — Token generation for Node.js, Python, Go


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


ConvoAI files are aligned 1:1 with repos in [AgoraIO-Conversational-AI](https://github.com/AgoraIO-Conversational-AI). Each file maps to one repo and links to its README and AGENT.md as sources of truth. Gotchas and quirks that LLMs consistently get wrong stay inline in the ConvoAI README.

## File Structure

```
skills/
└── agora/                                                   Skill root
    ├── SKILL.md                            (72 lines)   Entry point, product index
    └── references/
        ├── mcp-tools.md                    (93 lines)   MCP tool reference and graceful degradation
        ├── convoai-restapi-summary.yaml   (197 lines)   Condensed ConvoAI schema (90% use case)
        ├── rtc/                                          RTC (Video/Voice SDK)
        │   ├── README.md                   (85 lines)   Critical rules, encoder profiles, cross-platform notes
        │   ├── web.md                     (498 lines)   agora-rtc-sdk-ng: client, tracks, events, screen share
        │   ├── react.md                   (295 lines)   agora-rtc-react: hooks, custom patterns
        │   ├── nextjs.md                               Next.js / SSR dynamic import patterns
        │   ├── ios.md                     (301 lines)   AgoraRtcEngineKit (Swift): setup, delegation
        │   └── android.md                 (340 lines)   RtcEngine (Kotlin/Java): setup, callbacks
        ├── rtm/                                          RTM (Signaling / Messaging)
        │   ├── README.md                   (25 lines)   Key concepts, platform links
        │   └── web.md                     (375 lines)   agora-rtm v2: messaging, presence, stream channels
        ├── conversational-ai/                            Conversational AI (Voice AI Agents)
        │   ├── README.md                  (100 lines)   Architecture, endpoints, auth, lifecycle, REST API + config links, gotchas
        │   ├── agent-samples.md            (80 lines)   Backend, React clients, profiles, MLLM, deployment
        │   ├── agent-toolkit.md            (57 lines)   @agora/conversational-ai SDK: API, helpers, hooks
        │   ├── agent-ui-kit.md             (52 lines)   @agora/agent-ui-kit React components
        │   ├── server-custom-llm.md        (36 lines)   Custom LLM proxy: RAG, tools, memory
        │   └── server-mcp.md               (38 lines)   MCP memory server: persistent per-user memory
        ├── server/                                       Server-Side (Tokens)
        │   ├── README.md                   (20 lines)   Token types, when tokens are needed
        │   └── tokens.md                   (34 lines)   Token generation TOC + links to official docs
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
