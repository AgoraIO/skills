# AGENTS.md

This repository contains AI agent skills for building with [Agora](https://www.agora.io) — covering RTC, RTM, Conversational AI, Agora CLI workflows, server-side tokens, and Cloud Recording.

## Repository Structure

```text
scripts/
└── validate-skills.sh              # Static validation
skills/
└── agora/                          # Skill root
    ├── SKILL.md                    # Entry point, product index
    └── references/
        ├── doc-fetching.md         # Two-tier lookup procedure
        ├── mcp-tools.md            # MCP tool reference + graceful degradation
        ├── integration-patterns.md # RTC + RTM + ConvoAI coordination
        ├── cli/                    # Agora CLI: install, auth, init, quickstarts, env, doctor, automation
        ├── rtc/                    # RTC: Web, React, Next.js, iOS, Android, RN, Flutter
        ├── rtm/                    # RTM v2: Web, iOS, Android
        ├── conversational-ai/      # ConvoAI: REST, SDKs, toolkits, auth flow
        ├── server/                 # Token generation
        ├── cloud-recording/        # Cloud Recording REST API
        ├── server-gateway/         # Linux Server Gateway
        └── testing-guidance/       # Mocking patterns and test guidance
```

## 4-Layer Progressive Disclosure

| Layer | What | Size | When Loaded |
|-------|------|------|-------------|
| **1 — Description** | Trigger keywords in `SKILL.md` frontmatter | ~100 words | Always (skill index) |
| **2 — SKILL.md body** | Product routing, guardrails, ambiguity rules | ~90 lines | On activation |
| **3 — Product README** | Overview, critical rules, topic links | 20–100 lines | Per product |
| **4 — Topic files** | Implementation detail, code examples, API reference | 34–500 lines | Per topic |

## Freeze-Forever Rule

Ask: **will this still be correct in 6 months without any updates?** If yes, put it inline. If no, route to Level 2 docs lookup or an external link. MCP is preferred only when installed and supported in the current tool/runtime.

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
skills-ref validate skills/agora
claude plugin validate . --strict
claude plugin validate ./.claude-plugin/plugin.json
claude plugin validate ./skills --strict
```

Validation covers:

- frontmatter checks for all frontmatter-bearing markdown files under `skills/agora/`
- the official Agent Skills schema and naming rules through `skills-ref`
- duplicate skill names
- broken relative links
- Layer 4 topic files over 500 lines
- absolute local path leakage (`/Users/...`)
- blocklisted internal terms

Claude validation additionally covers the marketplace schema, plugin manifest,
and public skill frontmatter. Direct manifest validation may emit the expected
non-blocking warning that the repository-root `CLAUDE.md` is not plugin context.
