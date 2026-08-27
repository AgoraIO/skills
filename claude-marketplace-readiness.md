# Claude Marketplace Readiness

Assessment of the Agora plugin for submission to
`anthropics/claude-plugins-community`.

## Verdict

**Ready after the current changes are reviewed and committed.** The plugin now
follows Claude Code's documented default layout, installs its skill and MCP
server from a clean marketplace configuration, avoids volatile cached model
defaults, and has CI coverage for manifest and runtime packaging failures.

## Agent Skills Standard Conformance

The public `skills/agora/` directory conforms to the official Agent Skills
specification:

- `SKILL.md` is at the skill root and its `name` matches the `agora` directory.
- Required `name` and `description` fields meet the naming and length rules.
- Optional `license` and `metadata` fields use supported schema types.
- The 114-line entrypoint is below the recommended 500-line ceiling.
- References use relative paths and load progressively by product and topic.
- The pinned official reference implementation reports
  `Valid skill: skills/agora`.

The standard recommends avoiding deeply nested reference chains. This skill
uses one intentional intermediate product router (`SKILL.md` → product
`README.md` → topic) because it spans several distinct Agora products. That
keeps unrelated implementation material out of context and does not violate the
format specification. Additional routing layers should not be added.

## Packaging Decisions

### Keep the repository root as the plugin root

This repository serves both generic skill installers and Claude Code. Keeping
the canonical `skills/agora/` content inside the actual plugin root provides:

- default `skills/` discovery
- a root `.mcp.json`, the documented MCP location
- working `--plugin-dir` development
- one source of truth for all hosts
- no generated or duplicated 470+ KB skill bundle

A dedicated subdirectory would require either duplicated generated content or a
symlink outside the plugin directory. Claude's marketplace installer can
dereference an in-marketplace symlink, but `--plugin-dir` and direct local-path
loading skip symlinks that resolve outside the plugin. That is a worse
development contract than the current benign validation warning.

Direct plugin validation therefore continues to report that root `CLAUDE.md`
is not loaded as plugin context. The warning is accurate and non-blocking:
`CLAUDE.md` contains contributor instructions, while runtime instructions live
under `skills/`.

### Keep testing guidance internal

Testing guidance is a conditional reference used after the main Agora product
route is known. It is now
`skills/agora/references/testing-guidance/README.md`, without skill frontmatter,
so different hosts cannot accidentally expose it as a second public skill.

This keeps the public plugin surface to one coherent `agora` skill while
preserving progressive disclosure for test-generation and review tasks.

## Resolved Findings

### MCP discovery

- Added the standard root `.mcp.json`.
- Removed the broken custom `mcpServers` path and obsolete
  `.claude-plugin/mcp-config.json`.
- Aligned Claude and Cursor on the `agora-docs-mcp` server key and HTTP
  transport.
- Verified with a fresh isolated marketplace install:

```text
Skills (1)  agora
MCP servers (1)  agora-docs-mcp
```

### Manifest and marketplace metadata

- Plugin, skill, and Cursor wrapper versions are aligned at `1.8.2`.
- `plugin.json` is the single version authority; the duplicate marketplace
  entry version was removed, as recommended by Claude's versioning reference.
- Added supported `displayName`, author contact, homepage, marketplace owner
  URL, category, and tags.

### Freeze-forever compliance

- Removed cached vendor model IDs from quickstart, sample, Go SDK, and eval
  guidance.
- Removed static Next.js-to-Node.js runtime matrices.
- Runtime versions now come from the cloned sample's package metadata or
  `.nvmrc`.
- Provider and model values now come from the cloned official sample and
  current official provider docs.

Stable mechanisms remain inline: env names, provider-stage roles, authentication
rules, lifecycle ordering, and safety gates.

### Progressive disclosure

- Reduced `conversational-ai/quickstarts.md` from more than 700 lines to fewer
  than 500.
- Moved user-facing prompt and output templates into
  `conversational-ai/quickstart-prompts.md`.
- Removed duplicated execution logic from the prompt layer.
- Restored copy-safe RTC Web client/join alternatives and moved detailed screen
  sharing and large-scale subscription workflows into focused topic files,
  leaving useful room for future maintenance in the protected core Web
  reference.

### CI coverage

The validation workflow now checks:

1. Repository skill structure and relative links.
2. The official Agent Skills schema with the pinned `skills-ref` validator.
3. The 500-line Layer 4 topic ceiling.
4. Marketplace schema with `--strict`.
5. The plugin manifest directly.
6. Public skill frontmatter with `--strict`.
7. A fresh local marketplace install.
8. Machine-readable discovery of the `agora` skill and `agora-docs-mcp` server.
9. Markdown lint.

Local verification passes with one documented non-blocking direct-manifest
warning about the contributor-only root `CLAUDE.md`. Markdown lint reports zero
issues, and the isolated install reports one `agora` skill and one
`agora-docs-mcp` server. The official Agent Skills reference implementation
reports `Valid skill: skills/agora`.

Claude Code is pinned in CI, and the packaging assertion reads
`plugin list --json` plus the installed filesystem instead of matching
human-readable output spacing.

The marketplace description remains at the current top-level `description`
field. Claude's schema documents `metadata.description` only for backward
compatibility, so duplicating it would create two values that could drift.

## Distribution Context

The repository also contains an export workflow for a possible contribution to
`anthropics/skills` under the name `voice-ai-integration`. That workflow syncs
an export to a branch in the Agora fork and prints a URL for opening an upstream
pull request manually.

It is not currently an active Anthropic distribution channel: the export branch
and upstream `skills/voice-ai-integration` directory were not present when this
assessment was performed.

## Submission Checklist

- [x] Marketplace and plugin manifests parse and validate.
- [x] Skill links and frontmatter validate.
- [x] The official Agent Skills reference validator reports a valid skill.
- [x] Plugin installs from a clean marketplace configuration.
- [x] Agora skill is discovered.
- [x] Agora Docs MCP server is discovered.
- [x] Versions have a single authority and are release-bumped.
- [x] Volatile provider and framework values route to live sources.
- [x] README, license, changelog, security policy, and contribution docs exist.
- [ ] Review and commit the current changes.
- [ ] Run the updated GitHub Actions workflow on the submitted commit.
- [ ] Submit through the Claude Console or organization form.
- [ ] After catalog publication, add
  `/plugin install agora@claude-community` to the README.

## Housekeeping

The two pre-existing untracked audit artifacts were discarded after their
findings were resolved:

- `.github/v1.8.1-pr-body.md`
- `skills_eval_report.md`

Local `docs-links`, local `main`, and `origin/main` currently identify the same
commit. `docs-links` has no configured upstream branch.

## References

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices)
- [Create plugins](https://code.claude.com/docs/en/plugins)
- [Plugin manifest and default locations](https://code.claude.com/docs/en/plugins-reference)
- [Plugin marketplaces and version management](https://code.claude.com/docs/en/plugin-marketplaces)
- [Agent Skills](https://code.claude.com/docs/en/skills)
