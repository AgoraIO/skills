# Agora CLI

Use this module when the user is asking how to use the installed `agora` command-line tool.

<!-- applies-from: v0.2.1 -->

Verified against Agora CLI `0.2.1`. Minimum supported CLI is `>=0.1.7`. Label older behavior as deprecated or removed when it no longer matches the installed CLI.

The canonical CLI repository is <https://github.com/AgoraIO/cli>. Use that repository's `README.md`, `docs/commands.md`, `docs/automation.md`, `docs/error-codes.md`, `docs/telemetry.md`, `CHANGELOG.md`, and releases for Level 2 CLI lookup when these bundled references are not enough.

The Agora Docs MCP server (`agora-docs-mcp`) and the Agora CLI solve different problems: MCP traverses documentation only; the local `agora` binary logs in, creates or binds projects, clones quickstarts, writes env files, and checks readiness.

## What the CLI Covers

- OAuth login and local session management
- Local CLI defaults and config inspection
- Agora project creation, selection, and inspection
- Project environment export and dotenv file writing
- Feature enablement for `rtc`, `rtm`, and `convoai`
- One-command onboarding with `agora init`
- Official quickstart cloning, binding, and env writing
- Repo-local project binding through `.agora/project.json`
- Install self-diagnostics through `agora doctor`
- Environment-variable discovery through `agora env-help`
- Built-in workflow discovery through `agora skills`
- Local MCP tool serving through `agora mcp serve`
- ConvoAI readiness checks through `agora project doctor`
- Telemetry preferences and upgrade guidance
- Machine-readable command-tree discovery through `agora introspect --json`

## Routing

| User's request | Read this file next |
|---|---|
| Install, login, config directory, `whoami`, `auth status`, `login --no-browser` | [install-auth.md](install-auth.md) |
| `agora init`, `quickstart create`, `quickstart env write`, `.agora/project.json`, repo binding | [quickstarts.md](quickstarts.md) |
| `project env`, `project env write`, `.env`, `.env.local`, shell exports, `--with-secrets` | [env.md](env.md) |
| `project create`, `project list`, `project use`, `project show`, `project feature ...` | [projects.md](projects.md) |
| `doctor`, `project doctor`, readiness, blocking issues, next remediation command | [doctor.md](doctor.md) |
| Scripted usage, machine-readable output, `introspect`, `env-help`, `skills`, `mcp serve`, error envelopes, telemetry, upgrade, `AGORA_HOME` | [automation.md](automation.md) |

## Quick Reference

| Item | Value |
|---|---|
| Canonical repo | `https://github.com/AgoraIO/cli` |
| Preferred installer | `curl -fsSL https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh \| sh` |
| Windows PowerShell installer | `irm https://raw.githubusercontent.com/AgoraIO/cli/main/install.ps1 \| iex` |
| npm package | `agoraio-cli` (Node 18+; thin install wrapper for the same Go binary) |
| Installed command | `agora` |
| Deprecated package | `agora-cli-preview` |
| Verified against | `0.2.1` |
| Minimum supported | `0.1.7` |
| Default output mode | `pretty` |
| Agent-safe output mode | `--json` |
| Agent-safe command tree | `agora introspect --json` |
| Preferred full onboarding command | `agora init <name> --template <template>` |
| Preferred project env export command | `agora project env` |
| Preferred quickstart env command | `agora quickstart env write` |
| Install self-test | `agora doctor --json` |
| Environment override catalog | `agora env-help --json` |
| Built-in recipe catalog | `agora skills list --json` |

## Current Command Surface

Verified in CLI `0.2.1`:

- top level: `auth`, `completion`, `config`, `doctor`, `env-help`, `help`, `init`, `introspect`, `login`, `logout`, `mcp`, `open`, `project`, `quickstart`, `skills`, `telemetry`, `upgrade`, `version`, `whoami`
- auth group: `auth login`, `auth logout`, `auth status`
- config group: `config path`, `config get`, `config update`
- mcp group: `mcp serve`
- project group: `project create`, `project list`, `project use`, `project show`, `project env`, `project feature`, `project doctor`
- env group: `project env write`
- feature group: `project feature list`, `project feature status`, `project feature enable`
- quickstart group: `quickstart list`, `quickstart create`, `quickstart env`, `quickstart env write`
- skills group: `skills list`, `skills search`, `skills show`
- telemetry group: `telemetry status`, `telemetry enable`, `telemetry disable`
- upgrade aliases: `agora update`, `agora self-update`

For agents, `agora introspect --json` is the preferred way to discover the current command tree programmatically. `agora --help --all` is the human-readable equivalent.

If the user asks for a command outside this surface, do not invent it. Route them to the closest real command or say it is not part of the verified CLI. For example, `agora convoai init` and `agora project doctor all` are still not verified commands; use `agora init`, `agora quickstart ...`, or `agora project doctor --feature convoai` instead.

## CLI Readiness (agents)

Run this checklist **before any mutating CLI command** — including ConvoAI quickstart setup that uses the CLI. Start with the read-only probe. If the CLI is missing, below the minimum, shadowed on PATH, or blocked by a config schema mismatch, installers or global npm are allowed only as readiness remediation after user approval.

### 1. Read-only probe

```bash
agora version
which -a agora          # macOS / Linux; use where.exe agora on Windows
```

Run `agora doctor --json` only after the resolved CLI supports it (`0.2.0+`) or after upgrading. For `0.1.7–0.1.x`, use `agora version` plus PATH inspection, then prefer upgrading to the verified `0.2.1` baseline before deeper diagnostics.

### 2. Version gate

- **Minimum supported:** `0.1.7` (`agora upgrade`, `introspect`, npm channel, and stable automation errors require this floor).
- **Below minimum** (for example `0.1.6`) or command not found → stop and upgrade. Do **not** rely on `agora upgrade` on `0.1.6`; that subcommand does not exist there.

**Upgrade order** (ask for user approval before installers or global npm):

1. **Preferred:** `curl -fsSL https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh | sh`
   - Never use `--add-to-path` (removed in 0.2.0) or invent `--force` flags.
2. **Alternate:** `npm install -g agoraio-cli` (Node 18+), then repeat step 1 probes.
3. **If version is 0.1.7–0.2.0 and self-update fails crossing 0.2.1:** re-run the curl installer once (archive prefix rename).
4. **Confirm:** `agora version` shows `>=0.1.7`, then run `agora doctor --json` when available before continuing.

### 3. PATH shadowing

If install succeeded but `agora version` is still old:

```bash
which -a agora
```

Run the shell-specific PATH fix printed by `agora doctor`, or reorder PATH so the new install directory wins. Do not continue agent workflows until the probed version matches.

Do not uninstall binaries automatically. If an old `agora` binary still shadows the new install after PATH recovery, ask for user approval before removing it. For installer-managed installs, use the upstream uninstall path (`install.sh --uninstall` / `install.ps1 -Uninstall`); otherwise remove or rename only the specific stale binary the user approves.

### 4. Config schema mismatch

Error: `Config version N is newer than this CLI supports.`

- Usually an old binary is still on PATH while config was written by a newer CLI.
- Fix: complete the upgrade playbook above (0.2.0+ supports config v3 and auto-migrates).
- Last resort on a stuck old binary: back up config (`agora config path`), set `"version": 2`, then upgrade.

### 5. Agent-safe command shapes

After readiness passes:

| Task | Command shape |
|------|---------------|
| New demo in agent terminal | `agora init <name> --template python\|nextjs\|go --json` — **`--template` required** in `--json`, `--yes`, CI, or non-TTY runs (`QUICKSTART_TEMPLATE_REQUIRED` otherwise) |
| Official quickstart env | `agora quickstart env write <repo> --json` — writes template keys (`APP_ID` for Python, not generic `AGORA_APP_ID`) |
| Generic project dotenv | `agora project env write` — only when the repo is **not** an official quickstart expecting template keys |
| CI upgrade check | `agora upgrade --check --json` — do not mutate the binary in CI unless `AGORA_ALLOW_UPGRADE_IN_CI=1` |

Topic files link here instead of duplicating this playbook: [install-auth.md](install-auth.md), [quickstarts.md](quickstarts.md), [env.md](env.md), [doctor.md](doctor.md), [automation.md](automation.md).

## Important Rules

- **CLI readiness first:** complete the checklist above before mutating commands.
- For agents and scripts, prefer `--json` instead of parsing pretty output.
- Use `agora` in examples for an installed CLI. Use `./agora` only when running a locally built binary from the CLI repository.
- Use `agora init` for a new end-to-end demo when the user wants the CLI to create or bind a project, clone a quickstart, write env, and print next steps.
- Use `agora quickstart ...` when the user wants to clone or re-bind an official starter repo without necessarily creating a new project.
- Treat `project env` as the primary way to export project development config.
- Treat `agora doctor` as the install and local-environment self-test.
- Treat `project env write` as the generic file-writing companion for project App ID/App Certificate values.
- Treat `quickstart env write` as the template-aware env writer for official quickstarts.
- Do not expose secrets unless the user explicitly asks for `--with-secrets`.
- Treat `project doctor` as a readiness checker, not a full Conversational AI onboarding flow.
- In non-interactive runs (`--json`, `--yes`, CI, or non-TTY), always pass `--template` to `agora init`.
- In CI/non-TTY, `agora open` defaults to URL-only behavior unless `--browser` is explicitly passed.
- Prefer `--debug` and `AGORA_DEBUG`; `--verbose` and `AGORA_VERBOSE` were removed in `0.2.0`.
- Prefer the installer defaults; `--add-to-path` was removed in `0.2.0` because PATH wiring is now on by default.
- Do not present `agora-cli-preview` as current.
- Do not call undocumented commands such as `agora convoai init`.
