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
        ├── mcp-tools.md       ← MCP reference + freeze-forever decision table
        ├── rtc/
        ├── rtm/
        ├── conversational-ai/
        ├── server/
        └── cloud-recording/
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
- **No** → route to MCP or an external link (REST API schemas, SDK changelogs, vendor configs, model names)

See [`skills/agora/references/mcp-tools.md`](skills/agora/references/mcp-tools.md) for the full decision table.

## Naming Rule

Never use `shengwang-` prefixes. All paths, directory names, and skill names use Agora-branded identifiers. New product directories use the `agora-` prefix.

## Validation

Before suggesting any PR, run:

```bash
bash scripts/validate-skills.sh
```

Zero errors required. Fix any reported issues before opening the PR.
