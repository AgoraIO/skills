# Agora CLI Reference Correctness Refresh

**Date:** 2026-07-28
**Status:** Approved for implementation
**Scope:** Correctness-only refresh of `skills/agora/references/cli/` against Agora CLI `0.2.7`

## Problem

The bundled CLI references are pinned to Agora CLI `0.2.1`. The current release is
`0.2.7`. Two of the drifted facts are not merely stale — they send agents down paths
that fail.

### Install URL moved

Upstream made `https://dl.agora.io/cli/install.sh` the canonical installer
(commit `fe621d1`, "docs,ci: make dl.agora.io the canonical install URL"). It is a
CloudFront CDN that reaches users behind a GitHub block. The skill still directs
agents to `https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh` in five
files.

Verified 2026-07-28:

| URL | Result |
| --- | --- |
| `https://dl.agora.io/cli/install.sh` | `HTTP 200`, 48319 bytes |
| `https://dl.agora.io/cli/install.ps1` | `HTTP 200`, 24204 bytes |
| `https://dl.agora.io/cli/latest.json` | `{"tag_name":"v0.2.7","version":"0.2.7"}` |

### npm path is a trap

`references/cli/install-auth.md:22` offers `npm install -g agoraio-cli` as the
alternate upgrade remediation, and `references/cli/README.md:106` lists it as step 2
of the upgrade order. The npm registry's latest published `agoraio-cli` is **`0.1.6`**
(published 2026-04-30) — below the skill's own `>=0.1.7` floor, and `agora upgrade`
does not exist in that version. Upstream disabled npm publishing in CI
(commit `aad8582`, shipped in `0.2.7`).

An agent that follows the skill's own remediation step therefore installs a binary
that fails the skill's own readiness gate, with no documented way forward.

### Config schema claim is wrong

`references/cli/README.md:127` states that `0.2.0+` supports config **v3**. Agora CLI
`0.2.7` migrates config to schema version **4**. Line 128 offers a last-resort
hand-edit that depends on this number being right.

### Legacy branching

The `>=0.1.7` floor drags four dead conditionals through the files: the
"do not call `agora upgrade` on `0.1.6`" caveat, the archive-prefix-rename retry for
`0.1.7`–`0.2.0`, and two `0.2.0+`-conditional notes about `agora doctor` availability.
With npm gone, the installer always delivers the latest release, so `0.1.x` is
reachable only from a long-stale install.

## Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Scope | Correctness only | Fix what is actively wrong; defer new command surface |
| npm | Remove as install path, keep migration | Agents never install via npm; existing npm users get `--replace-npm` |
| Version pin | `0.2.7` + scoped coverage note | Pin must not imply the webhook/region surface was audited |
| Minimum supported | Raise `0.1.7` → `0.2.1` | Deletes four dead branches; `0.1.x` is effectively unreachable |
| Eval cases | Rewrite 3, add npm-rejection case | Locks the fix against silent regression |

### Verification method

Upstream's `CHANGELOG.md` files the region work under `[Unreleased]` even in the
`v0.2.7` tag, while the shipped `0.2.7` binary contains it. The changelog is therefore
not authoritative for this release. All command-surface claims in this refresh are
verified against `agora introspect --json` from the installed `0.2.7` binary
(commit `aad8582`, built 2026-06-29) and against upstream `docs/`.

## Changes

### Applied to every file in `references/cli/`

Replace the `<!-- applies-from: v0.2.1 -->` marker and the "Verified against Agora CLI
`0.2.1`" line with:

```markdown
<!-- applies-from: v0.2.7 -->

Verified against Agora CLI `0.2.7`.

> Coverage note: install, upgrade, and auth paths re-verified at 0.2.7. The command
> surface below was last fully audited at 0.2.1 — `project webhook` (0.2.6) and region
> flags (0.2.7) are not yet documented here. Use `agora introspect --json` for the
> live command tree.
```

### `references/cli/README.md`

- Header: pin `0.2.7`; minimum supported `0.2.1`.
- Quick Reference table: both installer rows use `https://dl.agora.io/cli/...`; delete
  the `npm package` row. Keep the `agora-cli-preview` deprecated-package row.
- Quick Reference: `Verified against` → `0.2.7`; `Minimum supported` → `0.2.1`.
- CLI readiness step 1: `agora doctor --json` becomes unconditional — the new floor is
  above the `0.2.0` version that introduced it.
- CLI readiness step 2: floor `0.2.1`. Delete the `0.1.6` `agora upgrade` caveat and
  the archive-prefix-rename step. Upgrade order collapses to: (1) curl the CDN
  installer, (2) confirm with `agora version` and `agora doctor --json`.
- CLI readiness step 4: config schema v3 → v4.
- Important Rules: remove the npm install reference.

### `references/cli/install-auth.md`

- Both installer code blocks use `https://dl.agora.io/cli/install.sh` and
  `https://dl.agora.io/cli/install.ps1`.
- Replace the `npm install path:` block and its follow-up paragraph with a blockquote
  callout stating that npm `agoraio-cli` is **not** a current install path, that the
  latest published version is `0.1.6` (below the supported floor), and that npm
  publishing is disabled upstream — followed by the migration command for anyone
  already on an npm-managed install:

  `curl -fsSL https://dl.agora.io/cli/install.sh | sh -s -- --replace-npm`

- Version-gate bullets: floor `0.2.1`. Delete the `0.1.6` bullet and the
  archive-prefix-rename bullet.
- The `--add-to-path` removal warning keeps its point but updates the URL inside it.
- Preview-package snippet becomes `npm uninstall -g agora-cli-preview` followed by the
  curl installer. The `npm uninstall` command stays because it removes an npm-managed
  install rather than creating one.

### `references/cli/doctor.md`, `quickstarts.md`, `automation.md`, `env.md`, `projects.md`

Pin and coverage note. Remove the conditionals the new floor makes dead:

- `doctor.md:21` — the `0.1.7–0.1.x` fallback to version/PATH checks.
- `doctor.md:48` — "CLI below `0.1.7`" becomes "below `0.2.1`".
- `quickstarts.md:116` — `agora doctor --json` is no longer conditional on `0.2.0+`.
- `automation.md:123` — drop the `0.2.0+` qualifier.

### `skills/agora/SKILL.md`

Line 83: floor `0.1.7` → `0.2.1`; drop "or global npm installs" from the remediation
sentence.

### `references/conversational-ai/`

Five call sites reference the floor or the npm alternate:

- `README.md:49` — floor `0.2.1`.
- `quickstarts.md:318` — floor `0.2.1`.
- `quickstarts.md:320` — collapse "minimum `0.2.1`, floor `0.1.7`" to a single floor of
  `0.2.1`.
- `quickstarts.md:491` — table cell: floor `0.2.1`, remove "npm alternate".
- `quickstarts.md:500` — remove the npm alternate from the remediation sentence.

### Repository docs

- `README.md:51` — installer URL → CDN.
- `README.md:54` — delete the sentence describing npm as a supported install wrapper.
- `CONTRIBUTING.md:88` — installer URL → CDN.

### `tests/eval-cases.md`

Rewrite three cases whose pass criteria assert the old behavior:

- **Line 589** (install and log in): assert the `https://dl.agora.io/cli/install.sh`
  installer, the `agora` command, and `agora login`. Remove the npm-wrapper clause.
- **Line 596** (`agora-cli-preview` still installed): route to the CDN installer.
  Remove "or npm `agoraio-cli` wrapper".
- **Line 764** (upgrade path): assert the CDN installer, re-verification with
  `agora version` and `which -a agora`. Remove the npm-alternate clause and the
  `0.1.6` clause.

Add one case:

- **User input:** "Should I install the Agora CLI with npm?"
- **Pass criteria:** Declines the npm path; states that published `agoraio-cli` is
  stale at `0.1.6` and below the supported floor; recommends
  `curl -fsSL https://dl.agora.io/cli/install.sh | sh`; offers
  `install.sh --replace-npm` for an existing npm-managed install.

### `CHANGELOG.md`

Add an entry recording the `0.2.7` re-pin, the canonical installer change, npm
removal, and the raised floor.

## Validation

1. `bash scripts/validate-skills.sh` — zero errors required.
2. `grep -rn "raw.githubusercontent.com/AgoraIO/cli" --include="*.md" .` — zero hits
   outside `CHANGELOG.md`.
3. `grep -rn "npm install -g agoraio-cli" --include="*.md" .` — zero hits outside
   `CHANGELOG.md`.
4. `grep -rn "0\.1\.[0-9]" --include="*.md" skills/` — review every remaining hit.
   Expect zero: the new floor removes all `0.1.x` conditionals. Any surviving hit must
   be a deliberate historical note, not a live instruction.

## Out of scope

Recorded here so the gap is visible to the next maintainer. None of the following is
documented by this change; `agora introspect --json` remains the escape hatch.

| Gap | Version | Note |
| --- | --- | --- |
| Region-aware profiles | `0.2.7` | Highest priority. `agora login --region global\|cn`; **breaking** — login without `--region` resets the active region to `global` and clears project context; `--region` removed from `init` and `project create`; `auth status --json` gains `data.region`; new `PROJECT_REGION_MISMATCH` error. Affects `agora login`, which the skill does document. |
| `agora project webhook` | `0.2.6` | Seven subcommands (`create`, `list`, `show`, `update`, `delete`, `events`), twelve `WEBHOOK_*` error codes. |
| `--rtm-data-center` | `0.2.0` | Flag on `init` and `project create` (`CN`, `NA`, `EU`, `AP`; defaults `NA`). Predates the current `0.2.1` pin — missed at the last audit rather than new drift, which suggests the deferred-surface list should be re-derived from `agora introspect --json` rather than from the changelog. |
| `AGORA_INSTALL_SOURCE=s3` | `0.2.7` | Restricted-network install for fully GitHub-blocked regions, plus the automatic mirror fallback. |
| Quickstart env layout change | post-`0.2.7` | On `main`, Python and Go quickstarts move to `server/.env.local` with `AGORA_APP_ID` / `AGORA_APP_CERTIFICATE`. Unreleased; the `0.2.7` behavior documented in the skill (`APP_ID` in `server/.env`) is still correct. |
