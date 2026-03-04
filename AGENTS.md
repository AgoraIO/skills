# AGENTS.md

This repository contains AI agent skills for building with [Agora](https://www.agora.io) — covering RTC, RTM, Conversational AI, server-side tokens, and Cloud Recording.

## Repository Structure

```
skills/
├── scripts/validate-skills.sh
└── skills/
    └── agora/                       # Skill root
        ├── SKILL.md                 # Entry point, product index
        ├── intake/SKILL.md          # Intake router for vague requests
        └── references/
            ├── mcp-tools.md         # MCP tool reference + freeze-forever table
            ├── rtc/  rtm/  conversational-ai/  server/  cloud-recording/
```

## 4-Layer Progressive Disclosure

| Layer | What | Size | When Loaded |
|-------|------|------|-------------|
| **1 — Description** | Trigger keywords in `SKILL.md` frontmatter | ~100 words | Always (skill index) |
| **2 — SKILL.md body** | Core concepts, product index, framework notes | ~72 lines | On activation |
| **3 — Product README** | Overview, critical rules, topic links | 20–100 lines | Per product |
| **4 — Topic files** | Implementation detail, code examples, API reference | 34–500 lines | Per topic |

## Freeze-Forever Rule

Ask: **will this still be correct in 6 months without any updates?** If yes, put it inline. If no, route to MCP or an external link. See [`skills/agora/references/mcp-tools.md`](skills/agora/references/mcp-tools.md) for the full decision table.

## Naming Conventions

- Directory names: lowercase `kebab-case`
- Use `agora-` prefix for new product skill directories
- **Never** use `shengwang-` prefixes

## Adding a New Product

1. Create `skills/agora/references/{product}/README.md` (Layer 3 — 20–100 lines)
2. Add an entry to the **Products** section of `skills/agora/SKILL.md`
3. Create topic files: `skills/agora/references/{product}/{topic}.md` (Layer 4 — 34–500 lines)
4. Apply the freeze-forever test to all inline content
5. Add at least one eval case to `tests/eval-cases.md`

## Validation

```bash
bash scripts/validate-skills.sh
```
