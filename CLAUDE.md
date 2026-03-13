# CLAUDE.md

This repo contains AI agent skills for Agora (agora.io) platform integration — RTC, RTM, Conversational AI, server-side tokens, and Cloud Recording.

## File Structure

The skill content lives under a nested path: `skills/agora/`. When adding or editing files, always place them here — not at repo root or in a flat `skills/` directory.

```
skills/
└── agora/                     ← skill root (all edits go here)
    ├── SKILL.md               ← entry point; do not restructure this file
    ├── intake/SKILL.md        ← intake router; do not restructure this file
    └── references/
        ├── doc-fetching.md    ← two-tier lookup procedure (agent-facing)
        ├── mcp-tools.md       ← Agora MCP server install guide (user-facing)
        ├── rtc/
        ├── rtm/
        ├── conversational-ai/
        ├── server/
        ├── cloud-recording/
        ├── server-gateway/
        └── testing-guidance/
```

## Protected Files

Do not modify the following files without an explicit instruction from the user:

- `skills/agora/references/rtc/web.md`
- `skills/agora/references/rtc/react.md`
- `skills/agora/references/rtc/ios.md`
- `skills/agora/references/rtc/android.md`
- `skills/agora/references/rtm/web.md`
These files contain stable, high-value inline examples. Edits require a verified reason and an updated eval case.

## Freeze-Forever Rule

Before adding any inline content, ask: **will this still be correct in 6 months without any updates?**

- **Yes** → put it inline (stable APIs, initialization sequences, gotchas)
- **No** → route to Level 2 fetch or an external link (REST API schemas, SDK changelogs, vendor configs, model names)

| Content type | Where it lives |
|---|---|
| RTC initialization, track management, event registration | Inline — `references/rtc/` |
| RTM messaging and presence patterns | Inline — `references/rtm/` |
| Token generation (RTC, RTM, AccessToken2) | Inline — `references/server/` |
| ConvoAI gotchas, field-type rules, lifecycle | Inline — `references/conversational-ai/README.md` |
| ConvoAI quick-start code (Python, Go, Java) | Level 2 fetch |
| ConvoAI full request/response schemas | Level 2 fetch |
| TTS / ASR / LLM vendor configs and model names | Level 2 fetch |
| Cloud Recording REST API field details | Level 2 fetch |
| Error code listings | Level 2 fetch |
| Release notes and new parameters | Level 2 fetch |

## Naming Rule

Never use `shengwang-` prefixes. All paths, directory names, and skill names use Agora-branded identifiers. New product directories use the `agora-` prefix.

## Validation

Before suggesting any PR, run:

```bash
bash scripts/validate-skills.sh
```

Zero errors required. Fix any reported issues before opening the PR.
