# Agora CLI

Use this module when the user is asking how to use the installed `agora` command-line tool.

<!-- applies-from: v0.2.1 -->

Last verified against Agora CLI `0.2.9`. Minimum CLI `0.2.1`. Label older behavior as deprecated or removed when it no longer matches the installed CLI.

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
- Read-only discovery of official recipes and recipe-backed initialization
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
| `agora init`, `recipes list/show`, `quickstart create`, `quickstart env write`, `.agora/project.json`, repo binding | [quickstarts.md](quickstarts.md) |
| `project env`, `project env write`, `.env`, `.env.local`, shell exports, `--with-secrets` | [env.md](env.md) |
| `project create`, `project list`, `project use`, `project show`, `project feature ...` | [projects.md](projects.md) |
| `doctor`, `project doctor`, readiness, blocking issues, next remediation command | [doctor.md](doctor.md) |
| Scripted usage, machine-readable output, `introspect`, `env-help`, `skills`, `mcp serve`, error envelopes, telemetry, upgrade, `AGORA_HOME` | [automation.md](automation.md) |

## Quick Reference

| Item | Value |
|---|---|
| Canonical repo | `https://github.com/AgoraIO/cli` |
| Preferred installer | `curl -fsSL https://dl.agora.io/cli/install.sh \| sh` |
| Windows PowerShell installer | `irm https://dl.agora.io/cli/install.ps1 \| iex` |
| Installed command | `agora` |
| Deprecated package | `agora-cli-preview` |
| Last verified | `0.2.9` |
| Minimum CLI | `0.2.1` |
| Default output mode | `pretty` |
| Agent-safe output mode | `--json` |
| Agent-safe command tree | `agora introspect --json` |
| Preferred full onboarding command | `agora init <name> --template <template>` or `--recipe <slug>` |
| Preferred project env export command | `agora project env` |
| Preferred quickstart env command | `agora quickstart env write` |
| Install self-test | `agora doctor --json` |
| Environment override catalog | `agora env-help --json` |
| Official recipe catalog | `agora recipes list --json` |
| Built-in workflow catalog | `agora skills list --json` |

## Current Command Surface

Verified in CLI `0.2.9`:

- top level: `auth`, `completion`, `config`, `doctor`, `env-help`, `help`, `init`, `introspect`, `login`, `logout`, `mcp`, `open`, `project`, `quickstart`, `recipes`, `skills`, `telemetry`, `upgrade`, `version`, `whoami`
- auth group: `auth login`, `auth logout`, `auth status`
- config group: `config path`, `config get`, `config update`
- mcp group: `mcp serve`
- project group: `project create`, `project list`, `project use`, `project show`, `project env`, `project feature`, `project doctor`
- env group: `project env write`
- feature group: `project feature list`, `project feature status`, `project feature enable`
- webhook group: `project webhook events`, `project webhook list`, `project webhook show`, `project webhook create`, `project webhook update`, `project webhook delete`
- quickstart group: `quickstart list`, `quickstart create`, `quickstart env`, `quickstart env write`
- recipes group: `recipes list`, `recipes show`
- skills group: `skills list`, `skills search`, `skills show`
- telemetry group: `telemetry status`, `telemetry enable`, `telemetry disable`
- upgrade aliases: `agora update`, `agora self-update`

`agora introspect --json` is authoritative for the live command tree. Treat it as the source of truth before telling a user a command does not exist.

For agents, `agora introspect --json` is the preferred way to discover the current command tree programmatically. `agora --help --all` is the human-readable equivalent.

If the user asks for a command outside this surface, do not invent it. Route them to the closest real command or say it is not part of the verified CLI. For example, `agora convoai init` and `agora project doctor all` are still not verified commands; use `agora init`, `agora quickstart ...`, or `agora project doctor --feature convoai` instead.

## CLI Readiness (agents)

Run this checklist **before any mutating CLI command** — including ConvoAI quickstart setup that uses the CLI. Start with the read-only probe. If the CLI is missing, below the minimum, shadowed on PATH, or blocked by a config schema mismatch, installers are allowed only as readiness remediation after user approval.

### 1. Read-only probe

```bash
agora version
which -a agora          # macOS / Linux; use where.exe agora on Windows
```

Run `agora doctor --json` after the read-only probe. It is available in every supported release.

### 2. Version gate

- **Minimum CLI:** `0.2.1`.
- **Below minimum** or command not found → stop and upgrade.

**Upgrade order** (ask for user approval before running installers):

1. **Preferred (macOS / Linux):** `curl -fsSL https://dl.agora.io/cli/install.sh | sh`
   **Preferred (Windows PowerShell):** `irm https://dl.agora.io/cli/install.ps1 | iex`
   - `--add-to-path` was removed in 0.2.0 — do not use it. `--force` / `-Force` do exist, but they install alongside a managed install and create PATH shadowing; do not use them to bypass a refusal.
2. **npm-managed installs:** if `which -a agora` (or `where.exe agora`) resolves the binary under `npm prefix -g`, the standalone installer refuses with exit `7` and suggests `npm update -g agoraio-cli` — do not follow that suggestion, it resolves to the stale `0.1.6`, below Minimum CLI. Do not pass `--force`/`-Force` to override the refusal either. See [install-auth.md](install-auth.md#npm-managed-installs) for the platform-specific migration commands.
3. **Confirm:** `agora version` shows `>=0.2.1`, then run `agora doctor --json` before continuing.

### 3. PATH shadowing

If install succeeded but `agora version` is still old:

```bash
which -a agora
```

Run the shell-specific PATH fix printed by `agora doctor`, or reorder PATH so the new install directory wins. Do not continue agent workflows until the probed version matches.

Do not uninstall binaries automatically. If an old `agora` binary still shadows the new install after PATH recovery, ask for user approval before removing it. For installer-managed installs, use the upstream uninstall path (`install.sh --uninstall` / `install.ps1 -Uninstall`). For npm-managed installs, remove with `npm uninstall -g agoraio-cli`, or migrate in place with `--replace-npm` (see [install-auth.md](install-auth.md#npm-managed-installs)) — do not delete an npm-managed binary by hand. Otherwise remove or rename only the specific stale binary the user approves.

### 4. Config schema mismatch

Error: `Config version N is newer than this CLI supports.`

- Usually an old binary is still on PATH while config was written by a newer CLI.
- Fix: complete the upgrade playbook above. Current releases auto-migrate config forward on first load.
- Last resort on a binary that cannot be upgraded: back up the config file (`agora config path`), then lower its `version` field to a value the running binary accepts.

### 5. Agent-safe command shapes

After readiness passes:

| Task | Command shape |
|------|---------------|
| New demo in agent terminal | `agora init <name> --template python\|nextjs\|go\|android --json` or `agora init <name> --recipe <slug> --json` — pass exactly one source (`INIT_SOURCE_REQUIRED` when omitted; `INIT_SOURCE_CONFLICT` when both are present) |
| Discover official recipes | `agora recipes list --type all\|ai\|rtc --json`, then `agora recipes show <slug> --json` |
| Clone-only quickstart | `agora quickstart create <name> --template <id> --template-only --json` |
| Official quickstart env | `agora quickstart env write <repo> --json` — Python and Go use `AGORA_APP_ID` / `AGORA_APP_CERTIFICATE`; Next.js uses its `NEXT_*` keys |
| Generic project dotenv | `agora project env write` — only when the repo is **not** an official quickstart expecting template keys |
| CI upgrade check | `agora upgrade --check --json` — do not mutate the binary in CI unless `AGORA_ALLOW_UPGRADE_IN_CI=1` |

Topic files link here instead of duplicating this playbook: [install-auth.md](install-auth.md), [quickstarts.md](quickstarts.md), [env.md](env.md), [doctor.md](doctor.md), [automation.md](automation.md).

## Important Rules

- **CLI readiness first:** complete the checklist above before mutating commands.
- For agents and scripts, prefer `--json` instead of parsing pretty output.
- Use `agora` in examples for an installed CLI. Use `./agora` only when running a locally built binary from the CLI repository.
- Use `agora init` for a new end-to-end demo when the user wants the CLI to create or bind a project, clone a quickstart, write env, and print next steps.
- Use `agora recipes list/show` for read-only discovery. Use `agora init <name> --recipe <slug>` to clone a supported official recipe and write credentials from its API-provided `cli.env` contract.
- Use `agora quickstart ...` when the user wants to clone or re-bind an official starter repo without necessarily creating a new project.
- Treat `project env` as the primary way to export project development config.
- Treat `agora doctor` as the install and local-environment self-test.
- Treat `project env write` as the generic file-writing companion for project App ID/App Certificate values.
- Treat `quickstart env write` as the template-aware env writer for official quickstarts.
- Do not expose secrets unless the user explicitly asks for `--with-secrets`.
- Treat `project doctor` as a readiness checker, not a full Conversational AI onboarding flow.
- In non-interactive runs (`--json`, `--yes`, CI, or non-TTY), pass exactly one of `--template` or `--recipe` to `agora init`.
- In CI/non-TTY, `agora open` defaults to URL-only behavior unless `--browser` is explicitly passed.
- Prefer `--debug` and `AGORA_DEBUG`; `--verbose` and `AGORA_VERBOSE` were removed in `0.2.0`.
- Prefer the installer defaults; `--add-to-path` was removed in `0.2.0` because PATH wiring is now on by default.
- Do not present `agora-cli-preview` as current.
- Do not call undocumented commands such as `agora convoai init`.
- Do not present npm `agoraio-cli` as an install or upgrade channel; it is stale below Minimum CLI and publishing is disabled upstream.
- Do not ask the user to choose a region; resolve it from `.agora/project.json`, then session state, then default to `global`. See [install-auth.md](install-auth.md).
