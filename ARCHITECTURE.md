# Architecture

## 4-Layer Progressive Disclosure

LLM context windows are finite. Load the minimum needed, go deeper only when required.

| Layer | What | Size | When Loaded |
|-------|------|------|-------------|
| **1 — Description** | Trigger keywords in `SKILL.md` frontmatter | ~100 words | Always (skill index) |
| **2 — SKILL.md body** | Core concepts, product index, framework notes | ~72 lines | On activation |
| **3 — Product README** | Overview, critical rules, topic links | 20–100 lines | Per product |
| **4 — Topic files** | Implementation detail, code examples, API reference | 34–500 lines | Per topic |

Navigation: `SKILL.md` → product `README.md` → topic file (e.g., `web.md`, `agent-samples.md`).

## Link-First vs Inline Strategy

Not all content belongs inline. The skill uses two strategies depending on how fast upstream content moves and how well it's documented:

| Product | Strategy | Why |
|---------|----------|-----|
| **Conversational AI** | TOC + links to repo READMEs and AGENT.md | Fast-moving, 5 upstream repos with good docs |
| **RTC / RTM** | Inline code examples | Stable APIs, official docs lack good examples |
| **Server / Tokens** | TOC + links to official docs | Well-documented at docs.agora.io |

ConvoAI files are aligned 1:1 with repos in [AgoraIO-Conversational-AI](https://github.com/orgs/AgoraIO-Conversational-AI/repositories). Each file maps to one repo and links to its README and AGENT.md as sources of truth. Gotchas and quirks that LLMs consistently get wrong stay inline in the ConvoAI README.

## File Structure

```
skills/
└── agora/                          Skill root
    ├── SKILL.md                    Entry point, product index
    ├── intake/
    │   └── SKILL.md                Multi-product needs analysis router
    └── references/
        ├── doc-fetching.md         Two-tier lookup procedure (agent-facing)
        ├── mcp-tools.md            MCP tool reference and graceful degradation
        ├── integration-patterns.md RTC+RTM+ConvoAI: init order, UID strategy, codec, tokens
        ├── rtc/                    RTC (Video/Voice SDK)
        │   ├── README.md           Critical rules, encoder profiles, cross-platform notes
        │   ├── web.md              agora-rtc-sdk-ng
        │   ├── react.md            agora-rtc-react
        │   ├── nextjs.md           Next.js / SSR patterns
        │   ├── ios.md              AgoraRtcEngineKit (Swift)
        │   ├── android.md          RtcEngine (Kotlin/Java)
        │   ├── react-native.md     react-native-agora
        │   ├── flutter.md          agora_rtc_engine (Dart)
        │   └── cross-platform-coordination.md
        ├── rtm/                    RTM Signaling SDK v2
        │   ├── README.md           Key concepts, gotchas, platform links
        │   ├── web.md              agora-rtm v2
        │   ├── ios.md              AgoraRtmClientKit (Swift)
        │   └── android.md          RtmClient (Kotlin)
        ├── conversational-ai/      Conversational AI (Voice AI Agents)
        │   ├── README.md           Architecture, endpoints, auth, lifecycle, gotchas
        │   ├── quickstarts.md      Quickstart state machine and baseline paths
        │   ├── agent-samples.md    Backend, React clients, profiles, MLLM
        │   ├── agent-toolkit.md    @agora/conversational-ai SDK
        │   ├── agent-client-toolkit-react.md   React hooks
        │   ├── agent-ui-kit.md     React UI components
        │   ├── agent-toolkit-ios.md    iOS toolkit
        │   ├── agent-toolkit-android.md  Android toolkit
        │   ├── server-custom-llm.md  Custom LLM proxy
        │   ├── server-mcp.md       MCP memory server
        │   ├── auth-flow.md        Token flow for direct REST API
        │   ├── python-sdk.md       Python SDK patterns
        │   ├── go-sdk.md           Go SDK patterns
        │   └── server-sdks.md      TypeScript/Node.js SDK patterns
        ├── cli/                    Agora CLI
        │   ├── README.md           Command surface, routing
        │   ├── install-auth.md     Install, login, config
        │   ├── projects.md         Project CRUD, feature enablement
        │   ├── doctor.md           Readiness checks
        │   └── automation.md       Scripted usage, --json
        ├── cloud-recording/        Cloud Recording (REST API)
        │   └── README.md           acquire/start/query/stop lifecycle
        ├── server-gateway/         Server Gateway (Linux SDK)
        │   ├── README.md           Overview, use cases
        │   └── linux-cpp.md        C++ SDK
        ├── server/                 Server-Side (Tokens)
        │   ├── README.md           Token types
        │   └── tokens.md           Token generation
        └── testing-guidance/       Testing Patterns
            └── SKILL.md            Mocking patterns for all platforms
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

- Edit the specific Layer 4 file
- **Inline files** (RTC, RTM): Keep code examples current, keep official doc URLs at the bottom
- **Link-first files** (ConvoAI, server): Update TOC links when upstream repos restructure. Keep gotchas inline only for things LLMs get wrong
- Don't duplicate content that lives in upstream repo READMEs — link to it instead

### Verifying URLs

```bash
grep -roh 'https://[^ )]*' skills/ | sort -u | while read url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 10 "$url")
  echo "$code $url"
done
```
