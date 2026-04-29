# Distribution Assets

This directory tracks marketplace rollout work for the Agora skills repository.

## What Lives Here

- `platform-status.md` — current rollout status by platform
- `platforms/claude.md` — Claude submission metadata and screenshot checklist
- `platforms/agentskills.md` — agentskills.io submission metadata and notes
- `platforms/anthropics-skills.md` — Anthropic public skills repo contribution pack
- `platforms/anthropics-pr-body.md` — PR body used by the Anthropic fork sync workflow
- `platforms/cursor.md` — Cursor-specific packaging and listing checklist
- `platforms/cursor-listing.md` — reusable Cursor listing copy
- `platforms/github-copilot.md` — GitHub Copilot-specific packaging and listing checklist
- `platforms/github-copilot-submission.md` — reusable Copilot / awesome-copilot submission copy

## Release Workflow

1. Update skill content and eval coverage.
2. Sync versions across:
   - `skills/agora/SKILL.md`
   - `.claude-plugin/plugin.json`
   - `.claude-plugin/marketplace.json`
3. Update `platform-status.md` to reflect what changed.
4. Refresh any platform-specific docs under `platforms/`.
5. Run `bash scripts/validate-skills.sh`.

## Current Focus

- Keep Claude/plugin assets shippable.
- Keep agentskills.io, Cursor, and Copilot submission packs ready in-repo.
- Use `platform-status.md` as the single visible tracker for rollout progress.
