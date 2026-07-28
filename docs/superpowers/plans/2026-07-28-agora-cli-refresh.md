# Agora CLI Reference Correctness Refresh — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct three actively-wrong facts in the bundled Agora CLI references (install URL, npm install path, config schema) and raise the minimum supported CLI, without documenting the deferred `0.2.6`/`0.2.7` command surface.

**Architecture:** Pure Markdown editing across 14 files. There is no code and no test framework. The "test cycle" for each task is a set of `grep` assertions plus `bash scripts/validate-skills.sh`, which checks frontmatter, duplicate skill names, broken relative links, absolute local paths, and blocklisted terms. Each task asserts its target state *before* editing (assertions must fail), edits, then re-asserts (must pass), then commits.

**Tech Stack:** Markdown, bash, `grep`, `python3` (via `scripts/validate-skills.sh`).

**Spec:** `docs/superpowers/specs/2026-07-28-agora-cli-refresh-design.md`
**Glossary:** `CONTEXT.md` — the terms *Last verified*, *Minimum CLI*, *readiness gate*, *install path*, *Level 2 fetch*, and *detect-don't-ask* are used with those exact meanings throughout.

## Global Constraints

- **Minimum CLI is `0.2.1`.** Every floor reference in the repo uses this value. `0.1.7` must not survive as a live instruction anywhere under `skills/`.
- **Canonical installer URLs** are exactly `https://dl.agora.io/cli/install.sh` (POSIX) and `https://dl.agora.io/cli/install.ps1` (PowerShell). `raw.githubusercontent.com/AgoraIO/cli` must not appear outside `CHANGELOG.md`.
- **npm is not an `install path`.** `npm install -g agoraio-cli` and `npm update -g agoraio-cli` must not appear as instructions. Two exceptions are deliberate and required: the `npm uninstall -g` commands (removal, not installation) and the explanatory inline note in `install-auth.md`.
- **State no config schema number.** Not `v3`, not `v4`, not `"version": 2`. The supported range spans schema 3 (`0.2.1`–`0.2.4`) and 4 (`0.2.5`+).
- **Never instruct an agent to ask the user which region they want.** Region is resolved by *detect-don't-ask*.
- **Do not ADD documentation for the deferred surface:** `project webhook`, region profiles as a feature, `--rtm-data-center`, `AGORA_INSTALL_SOURCE=s3`. The region *hazard* in `install-auth.md` is the single approved exception. This constraint forbids writing *new* coverage of those features; it does **not** authorize deleting accurate documentation that already exists. `--rtm-data-center` in particular already appears in two correct examples (`cli/projects.md`, `cli/quickstarts.md`) — leave them.
- **The `<!-- applies-from: vX -->` marker is a repo-wide convention** (also in `SKILL.md`, `mcp-tools.md`). It means "Minimum CLI" and stays at `v0.2.1` in all seven `references/cli/` files. Do not rename it. *Last verified* is carried in prose.
- **Protected files** (per `CLAUDE.md`) must not be touched: `references/rtc/{web,react,ios,android}.md`, `references/rtm/web.md`.
- **Every commit must leave `bash scripts/validate-skills.sh` passing.**

## File Structure

| File | Responsibility in this change |
| --- | --- |
| `skills/agora/references/cli/install-auth.md` | Installer URLs, detection-gated npm block, region detect-don't-ask rule, version gate |
| `skills/agora/references/cli/README.md` | Quick Reference table, readiness gate, version-agnostic config guidance |
| `skills/agora/references/cli/{doctor,quickstarts,env,projects,automation}.md` | Version labels; removal of conditionals the new floor makes dead |
| `skills/agora/SKILL.md` | Floor in the CLI readiness gate rule |
| `skills/agora/references/conversational-ai/{README,quickstarts}.md` | Five floor / npm call sites |
| `README.md`, `CONTRIBUTING.md` | Installer URL; npm claim; maintenance procedure |
| `tests/eval-cases.md` | Four stale cases rewritten, two new cases added |
| `CHANGELOG.md` | Release note |

## Deviation from spec discovered during planning

The spec says three eval cases are stale. There is a fourth: **CLI-03** (`tests/eval-cases.md:598-602`) asserts *"verified against CLI `0.2.1` with minimum supported `>=0.1.7`"*. Both halves change. Task 6 rewrites four cases, not three.

---

### Task 1: `install-auth.md` — installers, npm, region

**Files:**
- Modify: `skills/agora/references/cli/install-auth.md`

**Interfaces:**
- Produces: the canonical wording for the region detect-don't-ask rule and the npm inline note. Tasks 2, 4, 5, and 6 reference these facts but must not restate the full blocks.

- [ ] **Step 1: Assert the current (wrong) state**

```bash
grep -c "raw.githubusercontent.com/AgoraIO/cli" skills/agora/references/cli/install-auth.md
grep -c "npm install -g agoraio-cli" skills/agora/references/cli/install-auth.md
grep -c "0\.1\.7" skills/agora/references/cli/install-auth.md
```

Expected: `4`, `2`, `2`. These are the defects this task removes.

- [ ] **Step 2: Replace the version label**

Replace line 7 (`Verified against Agora CLI \`0.2.1\`.`) with:

```markdown
Last verified against Agora CLI `0.2.7`. Minimum CLI `0.2.1`.
```

Leave `<!-- applies-from: v0.2.1 -->` on line 3 unchanged.

- [ ] **Step 3: Rewrite the Version Gate bullets**

Replace the bullet list under `## Version Gate and Upgrade` (lines 19-25) with:

```markdown
- Read-only probe first: `agora version` and `which -a agora` / `where.exe agora`.
- If `agora` is missing or below Minimum CLI `0.2.1`, stop normal CLI workflow and upgrade.
- Preferred remediation after approval: `curl -fsSL https://dl.agora.io/cli/install.sh | sh`.
- If `agora version` still reports an old version after install, check PATH shadowing with `which -a agora` / `where.exe agora` and follow `agora doctor`'s shell-specific PATH fix. Do not uninstall automatically; remove an old binary only after user approval, using `install.sh --uninstall` / `install.ps1 -Uninstall` for installer-managed installs.
- If the CLI errors with `Config version N is newer than this CLI supports`, an old binary is reading config written by a newer CLI. Upgrade through the readiness flow; edit config only as a last resort after backing it up.
```

The `0.1.6` bullet and the archive-prefix bullet are deleted. Deleting the archive-prefix guidance is safe: that failure affects only `agora upgrade` self-update from `0.1.7`–`0.2.0`, and the upgrade order is curl-installer-first, which resolves the correct archive name on its own.

- [ ] **Step 4: Replace both installer blocks**

The POSIX block (line 30) becomes:

```bash
curl -fsSL https://dl.agora.io/cli/install.sh | sh
```

The PowerShell block (line 36) becomes:

```powershell
irm https://dl.agora.io/cli/install.ps1 | iex
```

- [ ] **Step 5: Replace the npm block with a detection-gated block**

Delete the `npm install path:` heading, its code fence, and the paragraph beginning "The npm package is expected to be a thin install wrapper" (lines 39-45). Insert in their place:

```markdown
### npm-managed installs

<!-- npm agoraio-cli is deliberately omitted as an install path. Latest published is
     0.1.6 (below Minimum CLI) and publishing is disabled upstream (commit aad8582).
     Upstream docs/install.md still lists npm as "Available" — do not restore it from
     there. Restore only if npm publishing resumes AND the published version clears
     the floor. -->

npm `agoraio-cli` is **not** a current install path. Never recommend it for install or upgrade.

Surface the migration below **only when detection shows an npm-managed install** — the readiness gate already runs `which -a agora`; if the resolved binary sits under `npm prefix -g`, it is npm-managed. Otherwise this section does not apply and should not be mentioned.

macOS / Linux:

```bash
curl -fsSL https://dl.agora.io/cli/install.sh | sh -s -- --replace-npm
```

Windows PowerShell (there is no `-ReplaceNpm` flag):

```powershell
npm uninstall -g agoraio-cli
irm https://dl.agora.io/cli/install.ps1 | iex
```

Two traps to avoid:

- `install.ps1` refuses to overwrite an npm-managed install and exits `7`, printing `npm update -g agoraio-cli` as the remedy. Do **not** follow it — that resolves to `0.1.6`, below Minimum CLI.
- Do **not** pass `-Force` to bypass the exit-`7` refusal. It creates a side-by-side install and the PATH shadowing the readiness gate then has to untangle.
```

- [ ] **Step 6: Update the preview-package snippet**

Replace the snippet at lines 59-62 with:

```bash
npm uninstall -g agora-cli-preview
curl -fsSL https://dl.agora.io/cli/install.sh | sh
```

`npm uninstall` stays: it removes an npm-managed install rather than creating one, so it is not an `install path`.

- [ ] **Step 7: Update the `--add-to-path` removal warning**

Replace line 66 with:

```markdown
> ⚠️ Removed in v0.2.0: the `--add-to-path` installer flag. Use `curl -fsSL https://dl.agora.io/cli/install.sh | sh` instead; PATH wiring is on by default.
```

- [ ] **Step 8: Add the region rule to Login Flow**

Immediately after the line `If browser auto-open fails, use \`agora login --no-browser\` ...` (line 90), insert:

```markdown
### Region — determine, do not ask

`agora login` without `--region` sets the active region to `global` and discards the previous project context. Resolve the region from state:

1. If `.agora/project.json` records a `region`, pass it: `agora login --region <region>`
2. Otherwise, if a prior session recorded `data.region` via `agora auth status --json`, preserve it
3. Otherwise run bare `agora login` — `global` is correct for the large majority

Never prompt the user to choose a region. If the CLI returns `PROJECT_REGION_MISMATCH`, its error names both regions and the exact command to run — follow that.
```

- [ ] **Step 9: Update the remaining `0.2.1` prose references**

Line 92: change ``In `0.2.1`, unauthenticated status`` to ``Unauthenticated status``.
Line 103: change ``Observed `0.2.1` exit codes:`` to ``Observed exit codes:``.
Line 115: delete the bullet about upgrade failing when crossing `0.2.1` (below Minimum CLI).
Line 119: change ``The verified `0.2.0` loopback login flow`` to ``The loopback login flow``.
Line 47: change ``In `0.2.1`, the shell installers`` to ``The shell installers``.

- [ ] **Step 10: Update "Things Not to Overstate"**

Add to that list:

```markdown
- Do not present npm `agoraio-cli` as an install or upgrade channel.
- Do not ask the user which region they want; resolve it from state.
```

- [ ] **Step 11: Re-run the assertions**

```bash
grep -c "raw.githubusercontent.com/AgoraIO/cli" skills/agora/references/cli/install-auth.md || echo "0 - PASS"
grep -n "npm install -g agoraio-cli\|npm update -g agoraio-cli" skills/agora/references/cli/install-auth.md
grep -n "0\.1\.7\|0\.1\.6" skills/agora/references/cli/install-auth.md
bash scripts/validate-skills.sh
```

Expected: no `raw.githubusercontent` hits. The only `npm update -g agoraio-cli` hit is inside the "do not follow it" trap warning. The only `0.1.6` hits are the inline HTML comment and the trap warning. No `0.1.7` hits. Validation passes.

- [ ] **Step 12: Commit**

```bash
git add skills/agora/references/cli/install-auth.md
git commit -m "docs(cli): move installer to dl.agora.io, drop npm install path, add region rule"
```

---

### Task 2: `cli/README.md` — quick reference, readiness gate, config guidance

**Files:**
- Modify: `skills/agora/references/cli/README.md`

**Interfaces:**
- Consumes: the region rule and npm detection block from Task 1 — this file *links* to them and must not duplicate their content.
- Produces: the canonical readiness gate that all other CLI files link to via `README.md#cli-readiness-agents`. The anchor `#cli-readiness-agents` must survive — five files link to it.

- [ ] **Step 1: Assert the current state**

```bash
grep -c "raw.githubusercontent.com/AgoraIO/cli" skills/agora/references/cli/README.md
grep -n "config v3\|\"version\": 2" skills/agora/references/cli/README.md
grep -c "0\.1\.7" skills/agora/references/cli/README.md
```

Expected: `3`; two config-number hits at lines 127-128; `5`.

- [ ] **Step 2: Replace the version label**

Line 7 becomes:

```markdown
Last verified against Agora CLI `0.2.7`. Minimum CLI `0.2.1`. Label older behavior as deprecated or removed when it no longer matches the installed CLI.
```

- [ ] **Step 3: Fix the Quick Reference table**

Replace the installer, npm, and version rows:

```markdown
| Preferred installer | `curl -fsSL https://dl.agora.io/cli/install.sh \| sh` |
| Windows PowerShell installer | `irm https://dl.agora.io/cli/install.ps1 \| iex` |
| Installed command | `agora` |
| Deprecated package | `agora-cli-preview` |
| Last verified | `0.2.7` |
| Minimum CLI | `0.2.1` |
```

The `| npm package | agoraio-cli ... |` row is deleted. The `Deprecated package` row stays.

- [ ] **Step 4: Make `agora doctor --json` unconditional in readiness step 1**

Replace line 95 with:

```markdown
Run `agora doctor --json` after the read-only probe. It is available in every supported release.
```

Minimum CLI `0.2.1` is above the `0.2.0` release that introduced `doctor`, so the availability conditional is dead.

- [ ] **Step 5: Rewrite readiness step 2 (version gate)**

Replace lines 99-108 with:

```markdown
- **Minimum CLI:** `0.2.1`.
- **Below minimum** or command not found → stop and upgrade.

**Upgrade order** (ask for user approval before running installers):

1. **Preferred:** `curl -fsSL https://dl.agora.io/cli/install.sh | sh`
   - Never use `--add-to-path` (removed in 0.2.0) or invent `--force` flags.
2. **Confirm:** `agora version` shows `>=0.2.1`, then run `agora doctor --json` before continuing.
```

The npm alternate step and the archive-prefix step are deleted.

- [ ] **Step 6: Make the config guidance version-agnostic**

Replace readiness step 4 (lines 122-128) with:

```markdown
### 4. Config schema mismatch

Error: `Config version N is newer than this CLI supports.`

- Usually an old binary is still on PATH while config was written by a newer CLI.
- Fix: complete the upgrade playbook above. Current releases auto-migrate config forward on first load.
- Last resort on a binary that cannot be upgraded: back up the config file (`agora config path`), then lower its `version` field to a value the running binary accepts.
```

State no schema number: the supported range spans schema 3 (`0.2.1`–`0.2.4`) and 4 (`0.2.5`+), and a bare integer is a `Level 2 fetch` concern under the freeze-forever rule.

- [ ] **Step 7: Update the Important Rules list**

Delete nothing else, but append:

```markdown
- Do not present npm `agoraio-cli` as an install or upgrade channel; it is stale below Minimum CLI and publishing is disabled upstream.
- Do not ask the user to choose a region; resolve it from `.agora/project.json`, then session state, then default to `global`. See [install-auth.md](install-auth.md).
```

- [ ] **Step 8: Re-run assertions**

```bash
grep -n "raw.githubusercontent.com/AgoraIO/cli" skills/agora/references/cli/README.md
grep -n "agoraio-cli" skills/agora/references/cli/README.md
grep -n "config v3\|config v4\|\"version\": 2" skills/agora/references/cli/README.md
grep -n "0\.1\.7\|0\.1\.6" skills/agora/references/cli/README.md
grep -c "cli-readiness-agents" skills/agora/references/cli/README.md
bash scripts/validate-skills.sh
```

Expected: no hits for the first four (the single `agoraio-cli` hit in the new Important Rules line is expected and correct). The readiness anchor heading still present. Validation passes.

- [ ] **Step 9: Commit**

```bash
git add skills/agora/references/cli/README.md
git commit -m "docs(cli): raise Minimum CLI to 0.2.1, CDN installer, version-agnostic config guidance"
```

---

### Task 3: Remaining five CLI reference files

**Files:**
- Modify: `skills/agora/references/cli/doctor.md`
- Modify: `skills/agora/references/cli/quickstarts.md`
- Modify: `skills/agora/references/cli/env.md`
- Modify: `skills/agora/references/cli/projects.md`
- Modify: `skills/agora/references/cli/automation.md`

**Interfaces:**
- Consumes: the readiness gate anchor `README.md#cli-readiness-agents` from Task 2. All five link to it; those links must keep resolving or `validate-skills.sh` fails on broken links.

- [ ] **Step 1: Assert the current state**

```bash
grep -n "Verified against Agora CLI" skills/agora/references/cli/{doctor,quickstarts,env,projects,automation}.md
grep -n "0\.1\.7\|0\.2\.0+" skills/agora/references/cli/{doctor,quickstarts,env,projects,automation}.md
```

Expected: five `Verified against` lines; hits at `doctor.md:21`, `doctor.md:48`, `quickstarts.md:116`, `automation.md:123`.

- [ ] **Step 2: Apply the stale-file version label to all five**

In each of the five files, replace the `Verified against Agora CLI \`0.2.1\`.` line with:

```markdown
Last verified against Agora CLI `0.2.1`. Minimum CLI `0.2.1`.

> Reviewed at `0.2.7` for install-path and minimum-version changes only. The command behavior below was last checked at `0.2.1`; use `agora introspect --json` for the live command tree.
```

These files keep `0.2.1` as *Last verified* deliberately. A uniform `0.2.7` stamp would claim verification that did not happen and erase the signal showing the next maintainer which files still need auditing.

Leave each file's `<!-- applies-from: v0.2.1 -->` marker unchanged.

- [ ] **Step 3: `doctor.md:21` — remove the availability conditional**

Replace with:

```markdown
Top-level `agora doctor` is available in every supported release.
```

- [ ] **Step 4: `doctor.md:48` — update the floor**

Replace with:

```markdown
- CLI below Minimum CLI `0.2.1` or config schema newer than the running binary: follow the curl-first upgrade path in [install-auth.md](install-auth.md#version-gate-and-upgrade)
```

- [ ] **Step 5: `quickstarts.md:116` — remove the availability conditional**

Replace with:

```markdown
- Use `agora doctor --json` when the failure looks local to the CLI install rather than to the project.
```

- [ ] **Step 6: `automation.md:123` — remove the version qualifier**

Replace with:

```markdown
After [CLI readiness](README.md#cli-readiness-agents) passes:
```

- [ ] **Step 7: Re-run assertions**

```bash
grep -n "0\.1\.7\|0\.1\.6" skills/agora/references/cli/{doctor,quickstarts,env,projects,automation}.md
grep -n "Last verified against" skills/agora/references/cli/{doctor,quickstarts,env,projects,automation}.md
bash scripts/validate-skills.sh
```

Expected: no `0.1.x` hits; five `Last verified` lines; validation passes with no broken-link errors.

- [ ] **Step 8: Commit**

```bash
git add skills/agora/references/cli/
git commit -m "docs(cli): label stale reference files, drop conditionals below the new floor"
```

---

### Task 4: `SKILL.md` and Conversational AI call sites

**Files:**
- Modify: `skills/agora/SKILL.md:83`
- Modify: `skills/agora/references/conversational-ai/README.md:49`
- Modify: `skills/agora/references/conversational-ai/quickstarts.md:318,320,491,500`

**Interfaces:**
- Consumes: Minimum CLI `0.2.1` from the Global Constraints; the readiness gate anchor from Task 2.

- [ ] **Step 1: Assert the current state**

```bash
grep -rn "0\.1\.7" skills/agora/SKILL.md skills/agora/references/conversational-ai/
```

Expected: five hits — `SKILL.md:83`, `conversational-ai/README.md:49`, `quickstarts.md:318`, `quickstarts.md:320`, `quickstarts.md:491`.

- [ ] **Step 2: `SKILL.md:83`**

Replace the sentence with:

```markdown
3. **CLI readiness gate.** Before any mutating Agora CLI command (`init`, `quickstart`, `project`, or `login`), run the read-only probe in **[references/cli/README.md](references/cli/README.md)**. Block normal CLI workflow when `agora version` is below Minimum CLI `0.2.1`, when PATH still resolves an older binary, or when config schema is newer than the running CLI. Installers are allowed only as readiness remediation after user approval. Use the documented curl-first upgrade path; do not invent installer flags such as `--add-to-path` or `--force`.
```

"or global npm installs" is removed.

- [ ] **Step 3: `conversational-ai/README.md:49`**

Replace with:

```markdown
0. run **[CLI readiness](../cli/README.md#cli-readiness-agents)** — version gate, upgrade if below Minimum CLI `0.2.1`, confirm PATH before any mutating CLI command
```

- [ ] **Step 4: `conversational-ai/quickstarts.md:318`**

Replace with:

```markdown
   2.1 Complete [CLI readiness](../cli/README.md#cli-readiness-agents) — block if below Minimum CLI `0.2.1` or PATH resolves an old binary
```

- [ ] **Step 5: `conversational-ai/quickstarts.md:320`**

Replace with:

```markdown
   2.3 Verify CLI version with `agora version` (Minimum CLI `0.2.1`)
```

The old text read "minimum `0.2.1`, floor `0.1.7`" — two numbers for one concept. Collapse to the single `Minimum CLI` term defined in `CONTEXT.md`.

- [ ] **Step 6: `conversational-ai/quickstarts.md:491`**

Replace the table row with:

```markdown
| Agora CLI (all baselines)      | `agora version`                                  | Minimum CLI `0.2.1`                     | Follow [CLI readiness](../cli/README.md#cli-readiness-agents): curl installer from `dl.agora.io` |
```

- [ ] **Step 7: `conversational-ai/quickstarts.md:500`**

Replace with:

```markdown
- For Agora CLI below Minimum CLI, follow [CLI readiness](../cli/README.md#cli-readiness-agents) — run the `dl.agora.io` curl installer, then re-verify `agora version` and `which -a agora`. Do not use `--add-to-path` or invented `--force` flags. Do not install or upgrade via npm.
```

- [ ] **Step 8: Re-run assertions**

```bash
grep -rn "0\.1\.7" skills/agora/SKILL.md skills/agora/references/conversational-ai/
grep -rn "agoraio-cli" skills/agora/references/conversational-ai/
bash scripts/validate-skills.sh
```

Expected: zero hits for both greps; validation passes.

- [ ] **Step 9: Commit**

```bash
git add skills/agora/SKILL.md skills/agora/references/conversational-ai/
git commit -m "docs: raise Minimum CLI to 0.2.1 across SKILL.md and ConvoAI call sites"
```

---

### Task 5: Repository-level docs

**Files:**
- Modify: `README.md:51,54`
- Modify: `CONTRIBUTING.md:86-92`

**Interfaces:**
- Consumes: the canonical installer URL and the verification method from the spec.

- [ ] **Step 1: Assert the current state**

```bash
grep -n "raw.githubusercontent.com/AgoraIO/cli\|agoraio-cli" README.md CONTRIBUTING.md
```

Expected: `README.md:51` (URL), `README.md:54` (npm sentence), `CONTRIBUTING.md:88` (URL), `CONTRIBUTING.md:86` (npm wrapper mention).

- [ ] **Step 2: `README.md` — installer block and npm sentence**

Replace line 51 with:

```bash
curl -fsSL https://dl.agora.io/cli/install.sh | sh
```

Delete line 54 entirely (the sentence beginning "The npm path, `npm install -g agoraio-cli`, is also supported…") and replace it with:

```markdown
The installer is served from the Agora CDN, so it works in networks where GitHub is blocked. On Windows, use `irm https://dl.agora.io/cli/install.ps1 | iex`.
```

- [ ] **Step 3: `CONTRIBUTING.md` — maintenance procedure**

Replace steps 1 and 2 of "Updating Agora CLI References" (lines 86-92) with:

```markdown
1. Install or update the CLI from the canonical installer:
   ```bash
   curl -fsSL https://dl.agora.io/cli/install.sh | sh
   agora version
   which -a agora
   ```
2. Record the release in the CLI reference files as `Last verified against Agora CLI <version>`, and update `Minimum CLI` only when deliberately raising the floor. Do not stamp a file as last-verified against a release whose behavior you did not actually check — leaving a file at an older version is how the next maintainer finds what still needs auditing.
```

Then append after the existing step 3:

```markdown
4. Verify claims against `agora introspect --json` and upstream source at the release tag — **not** against upstream `CHANGELOG.md`. That changelog has been wrong repeatedly: it filed region support under `[Unreleased]` in a tag that ships it, attributed a config-schema bump to the wrong release, and documented `--rtm-data-center` under a release that a later audit still missed.
```

- [ ] **Step 4: Re-run assertions**

```bash
grep -n "raw.githubusercontent.com/AgoraIO/cli\|agoraio-cli" README.md CONTRIBUTING.md
bash scripts/validate-skills.sh
```

Expected: zero hits; validation passes.

- [ ] **Step 5: Commit**

```bash
git add README.md CONTRIBUTING.md
git commit -m "docs: canonical dl.agora.io installer, drop npm claim, harden CLI update procedure"
```

---

### Task 6: Eval cases

**Files:**
- Modify: `tests/eval-cases.md` — CLI-01 (line ~589), CLI-02 (line ~596), CLI-03 (line ~601), CLI-26 (line ~764); two new cases appended to the CLI suite

**Interfaces:**
- Consumes: every behavioral decision from Tasks 1-5. These cases are the regression gate — the eval workflows (`gemini-eval.yml`, `hermes-eval.yml`, `openclaw-eval.yml`) trigger on any PR touching `skills/**/*.md`.

- [ ] **Step 1: Assert the current state**

```bash
grep -n "agoraio-cli\|raw.githubusercontent" tests/eval-cases.md
grep -n "0\.1\.7" tests/eval-cases.md
```

Expected: hits in CLI-01, CLI-02, CLI-26; `0.1.7` in CLI-03.

- [ ] **Step 2: Rewrite CLI-01 pass criteria**

```markdown
- Pass Criteria: Uses the CLI references, recommends `curl -fsSL https://dl.agora.io/cli/install.sh | sh`, names the installed `agora` command, and includes `agora login`; does not recommend npm
```

- [ ] **Step 3: Rewrite CLI-02 pass criteria**

```markdown
- Pass Criteria: Tells the user not to use `agora-cli-preview`; routes to the current `agora` install path via the `dl.agora.io` installer; does not present the preview package as current; does not recommend `npm install -g agoraio-cli` as the replacement
```

- [ ] **Step 4: Rewrite CLI-03 pass criteria**

```markdown
- Pass Criteria: States Minimum CLI `0.2.1`, and that install/auth guidance was last verified against `0.2.7`; does not hand-wave with "latest"
```

- [ ] **Step 5: Rewrite CLI-26**

The case title still says "Stuck on CLI 0.1.6", which remains a valid scenario — `0.1.6` is below the floor, which is exactly when this guidance fires. Only the expected behavior and pass criteria change:

```markdown
- Expected Behavior: Runs CLI readiness: `dl.agora.io` curl installer, then PATH re-check; does not use `--add-to-path`, invented `--force`, or npm
- Pass Criteria: Recommends `curl -fsSL https://dl.agora.io/cli/install.sh | sh`; re-verifies with `agora version` and `which -a agora`; does not offer `npm install -g agoraio-cli` as an alternate
```

- [ ] **Step 6: Append two new cases to the CLI suite**

```markdown
### CLI-28: npm install path is declined

- User Input: "Should I install the Agora CLI with npm?"
- Expected Behavior: Declines npm and routes to the standalone installer
- Pass Criteria: Does not recommend `npm install -g agoraio-cli`; states that the published npm package is stale at `0.1.6` and below Minimum CLI `0.2.1`; recommends `curl -fsSL https://dl.agora.io/cli/install.sh | sh`; if the user already has an npm-managed install, offers `--replace-npm` on macOS/Linux or `npm uninstall -g agoraio-cli` followed by the PowerShell installer on Windows
- Result: ___

### CLI-29: Region is detected, never asked

- User Input: "Set up the Agora CLI for my project"
- Expected Behavior: Completes login without interrogating the user about regions
- Pass Criteria: Runs bare `agora login` when the repo has no `.agora/project.json` and no prior session region; does **not** ask the user to choose between `global` and `cn`; raises `--region` only when a repo binding, a prior session region, or a `PROJECT_REGION_MISMATCH` error indicates it. Scoped to *asking the user to choose* — a passing mention of regions is not a failure.
- Result: ___
```

- [ ] **Step 7: Re-run assertions**

```bash
grep -n "raw.githubusercontent" tests/eval-cases.md
grep -n "0\.1\.7" tests/eval-cases.md
grep -c "CLI-28\|CLI-29" tests/eval-cases.md
bash scripts/validate-skills.sh
```

Expected: zero hits for the first two; `2` for the new case IDs; validation passes. Remaining `agoraio-cli` hits are inside negative assertions ("does not recommend…"), which is correct.

- [ ] **Step 8: Commit**

```bash
git add tests/eval-cases.md
git commit -m "test(eval): assert CDN installer, npm refusal, and region non-interrogation"
```

---

### Task 7: Changelog and full-repo verification sweep

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: all prior tasks. This is the gate that proves the Global Constraints hold repo-wide, not just per-file.

- [ ] **Step 1: Add the changelog entry**

Add under the top-most unreleased/current heading, matching the surrounding entry style:

```markdown
- `skills/agora/references/cli/*`: moved the canonical installer to `https://dl.agora.io/cli/install.sh`, removed npm `agoraio-cli` as an install path (published `0.1.6` is below the floor; upstream disabled npm publishing), raised Minimum CLI to `0.2.1`, made config-schema guidance version-agnostic, and split version labelling into per-file `Last verified` plus uniform `Minimum CLI`
- `skills/agora/references/cli/install-auth.md`: added a region detect-don't-ask rule — `agora login` without `--region` resets the active region to `global` and discards project context, so agents resolve region from `.agora/project.json` or session state instead of prompting
- `CONTEXT.md`: new glossary defining `Last verified`, `Minimum CLI`, `readiness gate`, `install path`, `Level 2 fetch`, and `detect-don't-ask`
- `tests/eval-cases.md`: rewrote CLI-01, CLI-02, CLI-03, CLI-26; added CLI-28 (npm refusal) and CLI-29 (region non-interrogation)
```

- [ ] **Step 2: Run the full Global Constraints sweep**

```bash
echo "--- 1. installer URL ---"
grep -rn "raw.githubusercontent.com/AgoraIO/cli" --include="*.md" . | grep -v "^./CHANGELOG.md"
echo "--- 2. npm as instruction ---"
grep -rn "npm install -g agoraio-cli\|npm update -g agoraio-cli" --include="*.md" . | grep -v "^./CHANGELOG.md"
echo "--- 3. old floor ---"
grep -rn "0\.1\.7" --include="*.md" skills/ tests/
echo "--- 4. config schema numbers ---"
grep -rn "config v[0-9]\|\"version\": 2" --include="*.md" skills/
echo "--- 5. validation ---"
bash scripts/validate-skills.sh
```

Expected results:

1. Zero lines.
2. Only lines that are negative assertions or the trap warning in `install-auth.md` — read each hit and confirm none is an instruction to run npm.
3. Zero lines.
4. Zero lines.
5. `Validation passed`.

If check 2 returns a hit that is *not* a negative assertion or the documented trap warning, that is a real failure — fix it before committing.

- [ ] **Step 3: Confirm protected files were untouched**

```bash
git diff --name-only main -- skills/agora/references/rtc/ skills/agora/references/rtm/web.md
```

Expected: no output. `CLAUDE.md` forbids modifying these without explicit instruction.

- [ ] **Step 4: Review the complete diff**

```bash
git diff main --stat
```

Expected: 14 files changed — 7 under `references/cli/`, `SKILL.md`, 2 ConvoAI files, `README.md`, `CONTRIBUTING.md`, `tests/eval-cases.md`, `CHANGELOG.md`.

- [ ] **Step 5: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: changelog for Agora CLI 0.2.7 correctness refresh"
```

---

## Self-Review

**Spec coverage.** Every spec section maps to a task: version labelling → Tasks 1-3; `cli/README.md` → Task 2; config guidance → Task 2 Step 6; `install-auth.md` installers/npm/region/version-gate/preview → Task 1; the five remaining CLI files → Task 3; `SKILL.md` → Task 4; ConvoAI → Task 4; repo docs → Task 5; eval cases → Task 6; `CHANGELOG.md` → Task 7; validation → Task 7 Step 2. The spec's out-of-scope table is enforced negatively by the Global Constraints.

**Placeholder scan.** No TBD/TODO. Every edit step carries literal replacement text. No step says "similar to Task N" — the region rule and npm block are written out once in Task 1 and referenced by file, not paraphrased.

**Consistency.** `Minimum CLI` and `Last verified` are used with their `CONTEXT.md` meanings throughout, never as "minimum supported" or "verified against". The readiness anchor is `README.md#cli-readiness-agents` in all five linking files, and Task 2's Interfaces block flags that the anchor must survive or link validation fails.

**One correction folded in:** the spec undercounted stale eval cases at three. CLI-03 asserts both the old floor and the old pin, making four. Task 6 covers all four and the deviation is recorded above.
