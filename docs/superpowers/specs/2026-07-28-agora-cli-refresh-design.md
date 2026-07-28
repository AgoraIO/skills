# Agora CLI Reference Correctness Refresh

**Date:** 2026-07-28
**Status:** Approved for implementation (revised after grilling session)
**Scope:** Correctness-only refresh of `skills/agora/references/cli/` against Agora CLI `0.2.7`

## Problem

The bundled CLI references are pinned to Agora CLI `0.2.1`. The current release is
`0.2.7`. Several of the drifted facts are not merely stale — they send agents down
paths that fail.

### Install path moved

Upstream made `https://dl.agora.io/cli/install.sh` the canonical installer
(commit `fe621d1`). It is a CloudFront CDN that reaches users behind a GitHub block.
The skill still directs agents to
`https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh` in five files.

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
(published 2026-04-30) — below even the old `>=0.1.7` floor, and `agora upgrade` does
not exist in that version. Upstream disabled npm publishing in CI (commit `aad8582`,
shipped in `0.2.7`).

An agent following the skill's own remediation step installs a binary that fails the
skill's own readiness gate.

Windows is worse. `install.ps1` detects an npm-managed `agora` and refuses to
overwrite it (exit `7`), printing `npm update -g agoraio-cli` as the remedy
(`install.ps1:434`) — which resolves to the stale `0.1.6`. There is no `-ReplaceNpm`
flag on Windows; `--replace-npm` is Unix-only.

### `agora login` silently switches region

Verified in `v0.2.7` `internal/cli/auth.go`: `login()` normalizes the region, so
omitting `--region` yields `global`, then calls `resetSessionRuntimeState()`, which
sets `CurrentRegion` and discards the previous project context.

The skill instructs bare `agora login`. For a user on the cn control plane that
command destroys a working session. This sits inside the auth path, which this change
claims as re-verified.

### Config schema claim spans two versions

`references/cli/README.md:127` states that `0.2.0+` supports config **v3**.
`currentAppConfigVersion` by release: `0.2.1`–`0.2.4` → **3**, `0.2.5`+ → **4**. With
the new floor at `0.2.1`, the supported range spans both, so no single number is
correct.

### Legacy branching

The `>=0.1.7` floor drags four dead conditionals through the files: the
"do not call `agora upgrade` on `0.1.6`" caveat, the archive-prefix-rename retry for
`0.1.7`–`0.2.0`, and two `0.2.0+`-conditional notes about `agora doctor` availability.

## Decisions

| Decision | Choice |
| --- | --- |
| Scope | Correctness only |
| npm | Remove as install path; migration shown only on detection |
| Version labelling | Split into per-file `Last verified` and uniform `Minimum CLI` |
| Minimum CLI | Raise `0.1.7` → `0.2.1` |
| Config schema | Version-agnostic guidance; state no schema number |
| Region | Document the hazard as a detect-don't-ask rule, not as a feature |
| Eval cases | Rewrite 3 stale cases, add 2 new |
| ADR | None |

### Verification method

Upstream's `CHANGELOG.md` proved unreliable three times during this investigation: it
files the region work under `[Unreleased]` even in the `v0.2.7` tag (the shipped
binary has it), attributes config schema 4 to that same entry (the code shows `0.2.5`),
and it documents `--rtm-data-center` under `0.2.0` while the `0.2.1` audit recorded no
prose for it. All claims in this refresh are verified against `agora introspect --json` from
the installed `0.2.7` binary and against upstream source at the relevant tag — not
against the changelog. Future audits should do the same.

### Domain vocabulary

`CONTEXT.md` (new, at repo root) defines the load-bearing terms this spec relies on:
**Last verified**, **Minimum CLI**, **readiness gate**, **install path**,
**Level 2 fetch**, and **detect-don't-ask**.

## Changes

### Version labelling, applied to every file in `references/cli/`

Replace the single `Verified against Agora CLI 0.2.1` line and the
`<!-- applies-from: v0.2.1 -->` marker with two distinct facts:

```markdown
<!-- last-verified: v0.2.7 -->

Last verified against Agora CLI `0.2.7`. Minimum CLI `0.2.1`.
```

`README.md` and `install-auth.md` carry `Last verified: 0.2.7` — those are the files
whose claims were actually re-checked. `doctor.md`, `quickstarts.md`, `env.md`,
`projects.md`, and `automation.md` carry `Last verified: 0.2.1` plus:

> Reviewed at `0.2.7` for install-path and minimum-version changes only. The command
> behavior below was last checked at `0.2.1`; use `agora introspect --json` for the
> live command tree.

A uniform `0.2.7` stamp would erase the signal that tells the next maintainer which
files still need auditing. Making staleness visible is the point.

### `references/cli/README.md`

- Version labels per the scheme above; Quick Reference `Minimum CLI` → `0.2.1`.
- Quick Reference: both installer rows use `https://dl.agora.io/cli/...`; delete the
  `npm package` row; keep the `agora-cli-preview` deprecated-package row.
- Readiness step 1: `agora doctor --json` becomes unconditional — the new floor is
  above the `0.2.0` release that introduced it.
- Readiness step 2: floor `0.2.1`. Delete the `0.1.6` `agora upgrade` caveat and the
  archive-prefix-rename step. Upgrade order collapses to: (1) curl the CDN installer,
  (2) confirm with `agora version` and `agora doctor --json`.
- Readiness step 4: version-agnostic config guidance (below).
- Important Rules: remove the npm install reference.

### Config-schema guidance (version-agnostic)

Replace both the "0.2.0+ supports config v3" claim and the "set `"version": 2`"
last-resort line. Neither states a schema number, because the supported range spans
two of them and the integer will not survive six months unattended — a `Level 2 fetch`
concern under the repo's freeze-forever rule. The CLI's own error already reports the
actual version:

> If the CLI reports `Config version N is newer than this CLI supports`, an old binary
> is reading config written by a newer CLI. Upgrade through the readiness flow. As a
> last resort on a binary that cannot be upgraded, back up the config file
> (`agora config path`) and lower its `version` field to a value the running binary
> accepts.

### `references/cli/install-auth.md`

**Installers.** Both code blocks use the `dl.agora.io` URLs. The `--add-to-path`
removal warning keeps its point but updates the URL inside it.

**npm — shown only on detection.** The readiness gate already runs `which -a agora`.
The migration block is surfaced only when the resolved binary sits under
`npm prefix -g`; for everyone else it never appears. Content when it does:

- Unix: `curl -fsSL https://dl.agora.io/cli/install.sh | sh -s -- --replace-npm`
- Windows: `npm uninstall -g agoraio-cli`, then
  `irm https://dl.agora.io/cli/install.ps1 | iex`
- Do **not** run `npm update -g agoraio-cli` even though `install.ps1` prints it on
  exit `7` — it resolves to `0.1.6`, below the floor.
- Do **not** pass `-Force` to get past the exit-`7` refusal; it creates the PATH
  shadowing the readiness gate then has to untangle.

**Why npm is absent — inline note.** Upstream `docs/install.md` still lists npm as
"Available", so a maintainer syncing against upstream will read our omission as a bug
and restore it. A one-line comment in this file records the evidence and the reversal
condition, because that maintainer reads the reference file, not `docs/`:

> npm `agoraio-cli` is deliberately omitted. Latest published is `0.1.6` (below
> Minimum CLI) and publishing is disabled upstream (`aad8582`). Restore only if npm
> publishing resumes *and* the published version clears the floor.

**Region — determine, do not ask.** Added to the Login Flow section:

> `agora login` without `--region` sets the active region to `global` and discards the
> previous project context. Resolve the region from state:
>
> 1. If `.agora/project.json` records a `region`, pass it: `agora login --region <region>`
> 2. Otherwise, if a prior session recorded `data.region` via `agora auth status --json`, preserve it
> 3. Otherwise run bare `agora login` — `global` is correct for the large majority
>
> Never prompt the user to choose a region. If `PROJECT_REGION_MISMATCH` appears, the
> error names both regions and the exact command to run — follow it.

This documents the hazard without documenting the feature. The default path for global
users is unchanged: bare `agora login`, no extra turn. Supporting facts verified at
`v0.2.7`: `.agora/project.json` carries a `region` field (`local_project.go:19`),
`auth status --json` reports `data.region` (`auth.go:146`), a binding with an empty
region is explicitly "no opinion" and never conflicts, and the mismatch error is
self-remediating (`projects.go:148`).

**Version gate.** Floor `0.2.1`; delete the `0.1.6` and archive-prefix bullets.
Deleting the archive-prefix guidance is safe: that failure affects only `agora upgrade`
self-update from `0.1.7`–`0.2.0`, and the upgrade order is curl-installer-first, which
resolves the correct archive name on its own.

**Preview package.** Snippet becomes `npm uninstall -g agora-cli-preview` followed by
the curl installer. The `npm uninstall` command stays: it removes an npm-managed
install rather than creating one, so it is not an `install path`.

### `references/cli/doctor.md`, `quickstarts.md`, `automation.md`, `env.md`, `projects.md`

Version labels per the scheme above. Remove the conditionals the new floor makes dead:

- `doctor.md:21` — the `0.1.7–0.1.x` fallback to version/PATH checks.
- `doctor.md:48` — "CLI below `0.1.7`" → "below `0.2.1`".
- `quickstarts.md:116` — `agora doctor --json` is no longer conditional on `0.2.0+`.
- `automation.md:123` — drop the `0.2.0+` qualifier.

### `skills/agora/SKILL.md`

Line 83: floor `0.1.7` → `0.2.1`; drop "or global npm installs" from the remediation
sentence.

### `references/conversational-ai/`

Five call sites: `README.md:49` (floor), `quickstarts.md:318` (floor),
`quickstarts.md:320` (collapse "minimum `0.2.1`, floor `0.1.7`" to a single floor),
`quickstarts.md:491` (table cell: floor, remove "npm alternate"), `quickstarts.md:500`
(remove npm alternate).

### Repository docs

- `README.md:51` — installer URL → CDN.
- `README.md:54` — delete the sentence describing npm as a supported install wrapper.
- `CONTRIBUTING.md:88` — installer URL → CDN.

### `tests/eval-cases.md`

The eval workflows run on any PR touching `skills/**/*.md`, so these are enforced.

Rewrite three cases whose pass criteria assert the old behavior:

- **Line 589** (install and log in): assert the `dl.agora.io` installer, the `agora`
  command, and `agora login`. Remove the npm-wrapper clause.
- **Line 596** (`agora-cli-preview` installed): route to the CDN installer. Remove
  "or npm `agoraio-cli` wrapper".
- **Line 764** (upgrade path): assert the CDN installer and re-verification with
  `agora version` / `which -a agora`. Remove the npm-alternate and `0.1.6` clauses.

Add two cases:

1. **Input:** "Should I install the Agora CLI with npm?"
   **Pass:** Declines the npm path; states that published `agoraio-cli` is stale at
   `0.1.6` and below Minimum CLI; recommends
   `curl -fsSL https://dl.agora.io/cli/install.sh | sh`; offers the platform-correct
   migration for an existing npm-managed install.

2. **Input:** "Set up the Agora CLI for my project" (repo with no `.agora/project.json`)
   **Pass:** Runs bare `agora login`; does **not** ask the user to choose a region;
   does not raise `--region` absent a binding, prior session region, or
   `PROJECT_REGION_MISMATCH`. Scoped to *asking the user to choose* — a passing
   mention of regions is not a failure.

### `CHANGELOG.md`

Record the `0.2.7` re-verification, the canonical installer change, npm removal, the
raised floor, and the region detect-don't-ask rule.

## Validation

1. `bash scripts/validate-skills.sh` — zero errors required.
2. `grep -rn "raw.githubusercontent.com/AgoraIO/cli" --include="*.md" .` — zero hits
   outside `CHANGELOG.md`.
3. `grep -rn "npm install -g agoraio-cli" --include="*.md" .` — zero hits outside
   `CHANGELOG.md` and the deliberate inline note in `install-auth.md`.
4. `grep -rn "0\.1\.[0-9]" --include="*.md" skills/` — review every remaining hit.
   Expect zero live instructions; any survivor must be a deliberate historical note.
5. `grep -rn "config v[0-9]\|version.: 2" --include="*.md" skills/` — zero hits; the
   config guidance must state no schema number.

## Out of scope

Recorded so the gap is visible to the next maintainer. `agora introspect --json`
remains the escape hatch.

| Gap | Version | Note |
| --- | --- | --- |
| Region profiles (feature) | `0.2.7` | The *hazard* is now documented; the feature is not. Endpoint overrides (`AGORA_API_BASE_URL` etc.), `PROJECT_REGION_MISMATCH` reference, `data.region` in JSON shapes, and cn-vs-global endpoint selection remain undocumented. |
| `agora project webhook` | `0.2.6` | Seven subcommands, twelve `WEBHOOK_*` error codes. |
| `--rtm-data-center` | `0.2.0` | Flag on `init` and `project create` (`CN`, `NA`, `EU`, `AP`; default `NA`). **Correction:** an earlier draft of this table called this undocumented. It is not — `cli/projects.md` and `cli/quickstarts.md` each already carry a correct example using it. What is actually missing is only prose stating the accepted values and the `NA` default. These examples must not be deleted on the strength of this row. |
| `AGORA_INSTALL_SOURCE=s3` | `0.2.7` | Restricted-network install for fully GitHub-blocked regions, plus automatic mirror fallback. |
| Quickstart env layout | post-`0.2.7` | On `main`, Python and Go quickstarts move to `server/.env.local` with `AGORA_APP_ID` / `AGORA_APP_CERTIFICATE`. Unreleased; the `0.2.7` behavior in the skill (`APP_ID` in `server/.env`) is still correct. |
