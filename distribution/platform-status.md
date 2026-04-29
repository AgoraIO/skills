# Platform Rollout Status

Last updated: 2026-04-29

Legend:

- `done` — required repo assets already exist
- `in_progress` — some assets exist, but rollout is not yet submission-ready
- `not_started` — no platform-specific packaging exists yet

| Platform | Priority | Status | Repo State | Action |
|---|---|---|---|---|
| Claude/plugin | P0 | done | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.claude-plugin/mcp-config.json` exist, versions are aligned to `1.5.1`, and submission metadata now lives in `distribution/platforms/claude.md`. | Capture fresh screenshots, then complete the external submit action in Claude. |
| agentskills.io | P0 | done | Registry-compatible metadata and reviewer notes are now prepared in `distribution/platforms/agentskills.md`, reusing `.claude-plugin/marketplace.json`. | Complete the external submit action on agentskills.io. |
| anthropics/skills | P1 | in_progress | Anthropic-specific PR copy exists, and sync automation now exports `skills/agora/` as `skills/voice-ai-integration/` to the fork via `.github/workflows/sync-anthropics-fork.yml`. | Add the `ANTHROPICS_SKILLS_SYNC_TOKEN` secret, run the workflow once, and verify the upstream PR. |
| Cursor Directory / Marketplace | P0 | done | README mentions Cursor usage, packaging guidance is in `distribution/platforms/cursor.md`, and reusable listing copy now lives in `distribution/platforms/cursor-listing.md`. | Capture screenshots and complete the external listing submission. |
| GitHub Copilot / awesome-copilot | P0 | done | README mentions Copilot usage, `.github/copilot-instructions.md` exists, packaging guidance is in `distribution/platforms/github-copilot.md`, and submission copy now lives in `distribution/platforms/github-copilot-submission.md`. | Open the external contribution PR to `github/awesome-copilot`. |
| Codex | P1 | in_progress | Codex evaluation workflow exists, but there is no Codex distribution wrapper yet. | Decide whether to distribute as skill-only or plugin-plus-skill, then add Codex-specific install notes. |
| Kimi | P1 | in_progress | Markdown skill layout is reusable, but no Kimi-specific packaging note exists. | Add a compatibility note and install path once Kimi submission expectations are finalized. |
| awesome-openclaw-skills | P1 | in_progress | OpenClaw eval workflow exists, but no community-listing note exists. | Add an OpenClaw install snippet and map repo assets to the community PR checklist. |
| VS Code extension marketplace | P2 | not_started | No extension manifest or VS Code packaging assets exist. | Do not prioritize; prefer GitHub Copilot skill distribution instead of extension work. |
| MiniMax SkillHub | P2 | not_started | No MiniMax-specific docs or packaging assets exist. | Wait for a stable submission format, then create a dedicated adapter package if needed. |
| TRAE / SOLO | P2 | not_started | No TRAE-specific docs or packaging assets exist. | Wait for a confirmed public submission path before investing in packaging. |
