# Contributing to Agora Agent Skills

Thanks for your interest in contributing! This repository provides reusable skills that help AI coding agents build applications on the Agora platform.

## Scope

This repository stores AI agent skills for Agora (agora.io) platform integration,
following the [Agent Skills](https://agentskills.io) open standard.
Changes should improve routing accuracy, code generation quality, and maintainability.

## Adding a New Product Skill

Examples of existing products added this way: Cloud Recording (`references/cloud-recording/`),
Server Gateway (`references/server-gateway/`), Testing Guidance (`references/testing-guidance/`).

1. Create `skills/agora/references/{product}/README.md` (Layer 3 — overview,
   critical rules, topic links, 20–100 lines)
2. Add an entry to the **Products** section of `skills/agora/SKILL.md`
3. Create topic files as needed: `skills/agora/references/{product}/{topic}.md`
   (Layer 4 — 34–500 lines)
4. Apply the freeze-forever test to all inline content (see below)
5. Add at least one eval case to `tests/eval-cases.md` for the new product
6. Update `skills/agora/intake/SKILL.md`:
   - Add the product to the Product Landscape table
   - Update the Product Relationships diagram
   - Add relevant rows to Common Product Combinations
   - Add a routing entry to the Step 4 table
   - Add a Decision Shortcuts row if the product has a clear keyword trigger
7. Bump the version in all three version files (see [Version Bumping](#version-bumping))

## Adding a New Platform

1. Create `skills/agora/references/{product}/{platform}.md` (Layer 4)
2. Add a link in the product's `README.md`

## Size Constraint

Individual skill files must not exceed **500 lines**. This is a hard limit —
context windows are finite, and oversized files crowd out the user's actual
project context. If a Layer 4 topic file approaches 500 lines, split it into
multiple topic files and link from the product README.

Current largest files as reference: `rtc/web.md` (498 lines), `rtm/web.md`
(375 lines). These are at or near the limit; do not expand them further.

## The Freeze-Forever Test

Before adding any factual content inline, ask: **will this still be correct in 6 months
without any updates?**

- **Yes** (stable API patterns, initialization sequences, token generation, RTC track
  management): put it **inline**.
- **No** (REST API parameter lists, SDK changelogs, vendor configurations, model names,
  ConvoAI request/response schemas): put it **behind an MCP call** or an **external link**.
  Never hardcode fast-moving content.

The link-first vs inline decision table in `README.md` already encodes this
principle. Follow it. When in doubt, add a new row to that table and document your
reasoning in the PR description.

The freeze-forever test applies to new content only. Do not remove existing inline
examples from RTC, RTM, or token generation files — these are stable APIs where
inline examples are the primary competitive value.

## Updating a Gotcha or Critical Rule

The 30+ documented gotchas in `references/rtc/README.md` and
`references/conversational-ai/README.md` are the most valuable content in this repo.
They represent debugging knowledge that LLMs consistently get wrong. Before updating:

1. Verify the behavior against the latest SDK version. Check the release notes linked
   at the bottom of `README.md`.
2. If the behavior changed in a specific SDK version, include that version in the
   gotcha description (e.g., "Fixed in agora-rtc-sdk-ng v4.21").
3. Do not remove a gotcha because it "seems obvious" — these were written because
   LLMs consistently generated the wrong code. The test cases in `tests/eval-cases.md`
   provide the evidence.
4. If a gotcha no longer applies to any supported SDK version, move it to a
   `## Historical Notes` section at the bottom of the file rather than deleting it.

## Required Frontmatter

Every `SKILL.md` must include:

    ---
    name: kebab-case-name          # max 64 chars, unique across repo
    description: >-
      Trigger phrases and description that help agents recognize when to use
      this skill. Include concrete product names and action verbs.
    license: MIT
    metadata:
      author: agora
      version: "X.Y.Z"
    ---

Rules:
- Do NOT use `triggers` as a top-level frontmatter field — fold trigger phrases
  into `description`. (Consistent with agentskills.io standard.)
- Use relative links for all local references.
- Put detailed docs under `references/`; keep `SKILL.md` focused on workflow.

## Naming

- Directory names: lowercase kebab-case
- Skill names (frontmatter `name`): unique across repository, lowercase kebab-case
- Use `agora-` prefix for new product skill directories
- Never use `shengwang-` prefixes — this repo uses Agora-branded paths throughout

## Pull Request Checklist

- [ ] Freeze-forever test applied to all new inline content (see above)
- [ ] Routing still correct from `skills/agora/SKILL.md`
- [ ] New or changed local links are valid (no broken relative paths)
- [ ] No duplicate skill names
- [ ] No absolute local paths (`/Users/...` or any machine-specific path)
- [ ] No hardcoded credentials, API keys, or App Certificates
- [ ] At least one eval case added or updated in `tests/eval-cases.md`
  (required for new product or platform additions)
- [ ] If adding a code generation skill: testing guidance updated in
  `references/testing-guidance/SKILL.md`
- [ ] `scripts/validate-skills.sh` passes locally

## Local Validation

    bash scripts/validate-skills.sh

## Running Evals

Eval cases live in `tests/eval-cases.md`. To run them:

1. Load the skill in your AI coding assistant (see [README — Installation](README.md#installation))
2. For each case, send the "User Input" to the assistant with the skill active
3. Compare the response against "Expected Behavior" and "Pass Criteria"
4. Record `PASS` or `FAIL` in the Result field
5. Add the run to the **Evaluation Log** table at the bottom of `tests/eval-cases.md`
   (date, skill version, pass/fail counts, failed case IDs, fix actions taken)

Run the full suite after every non-trivial skill change. Failed cases drive targeted
skill edits — don't ship a fix without verifying the case now passes.

## Version Bumping

Versions must stay in sync across three files. Bump all three together:

| File | Field |
|------|-------|
| `skills/agora/SKILL.md` | `metadata.version` in frontmatter |
| `.claude-plugin/plugin.json` | `"version"` |
| `.claude-plugin/marketplace.json` | `plugins[0].version` |

Version rules:
- **Patch** (`x.y.Z`): gotcha fixes, broken link repairs, content corrections
- **Minor** (`x.Y.0`): new product or platform added, new eval cases, new topic files
- **Major** (`X.0.0`): breaking restructure of skill entry points or routing logic

Document the change in `CHANGELOG.md` under a new `[x.y.z]` heading.

## Plugin & Marketplace Registration

This skill is published to:

- **[agentskills.io](https://agentskills.io)** — open skill registry (`.claude-plugin/marketplace.json`)
- **Claude Code plugin marketplace** — hosted at `AgoraIO/skills` on GitHub (`.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`)

Users install via two slash commands inside Claude Code:

```
/plugin marketplace add AgoraIO/skills
/plugin install agora@agora-skills
```

(`agora-skills` is the marketplace `name` in `marketplace.json`; `agora` is the plugin `name`.)

To update a registration after a version bump:
1. Submit a PR with the bumped version in both JSON files
2. Once merged, users get the update automatically when Claude Code refreshes (`/plugin marketplace update`)
3. For agentskills.io manual updates, follow the [agentskills.io submission guide](https://agentskills.io)

The Agora MCP server config is bundled in `.claude-plugin/mcp-config.json` and
referenced from `plugin.json` via `"mcpServers": "./mcp-config.json"`.

## Verifying URLs

Before opening a PR, check that all `https://` links in skill files are reachable:

```bash
grep -roh 'https://[^ )]*' skills/ | sort -u | while read url; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 10 "$url")
  echo "$code $url"
done
```

Any non-200 response (except intentional 301 redirects) should be investigated and fixed.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
