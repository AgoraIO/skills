# Agora CLI

Use this module when the user is asking how to use the installed `agora` command-line tool.

Verified against Agora CLI `0.1.7` on 2026-04-30. Write guidance for `>=0.1.7`, but label version-sensitive behavior explicitly when it was only verified in `0.1.7`.

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
| `project doctor`, readiness, blocking issues, next remediation command | [doctor.md](doctor.md) |
| Scripted usage, machine-readable output, `introspect`, error envelopes, telemetry, upgrade, `AGORA_HOME` | [automation.md](automation.md) |

## Quick Reference

| Item | Value |
|---|---|
| Canonical repo | `https://github.com/AgoraIO/cli` |
| Preferred installer | `curl -fsSL https://raw.githubusercontent.com/AgoraIO/cli/main/install.sh \| sh -s -- --add-to-path` |
| Windows PowerShell installer | `irm https://raw.githubusercontent.com/AgoraIO/cli/main/install.ps1 \| iex` |
| npm package | `agoraio-cli` (Node 18+; thin install wrapper for the same Go binary) |
| Installed command | `agora` |
| Deprecated package | `agora-cli-preview` |
| Minimum skill-supported version | `0.1.7` |
| Default output mode | `pretty` |
| Agent-safe output mode | `--json` |
| Agent-safe command tree | `agora introspect --json` |
| Preferred full onboarding command | `agora init <name> --template <template>` |
| Preferred project env export command | `agora project env` |
| Preferred quickstart env command | `agora quickstart env write` |

## Current Command Surface

Verified in CLI `0.1.7`:

- top level: `login`, `logout`, `whoami`, `auth`, `config`, `init`, `introspect`, `open`, `project`, `quickstart`, `telemetry`, `upgrade`, `version`
- auth group: `auth login`, `auth logout`, `auth status`
- config group: `config path`, `config get`, `config update`
- project group: `project create`, `project list`, `project use`, `project show`, `project env`, `project feature`, `project doctor`
- env group: `project env write`
- feature group: `project feature list`, `project feature status`, `project feature enable`
- quickstart group: `quickstart list`, `quickstart create`, `quickstart env`, `quickstart env write`
- telemetry group: `telemetry status`, `telemetry enable`, `telemetry disable`

For agents, `agora introspect --json` is the preferred way to discover the current command tree programmatically. `agora --help --all` is the human-readable equivalent.

If the user asks for a command outside this surface, do not invent it. Route them to the closest real command or say it is not part of the verified CLI. For example, `agora convoai init` and `agora project doctor all` are still not verified commands; use `agora init`, `agora quickstart ...`, or `agora project doctor --feature convoai` instead.

## Important Rules

- For agents and scripts, prefer `--json` instead of parsing pretty output.
- Use `agora` in examples for an installed CLI. Use `./agora` only when running a locally built binary from the CLI repository.
- Use `agora init` for a new end-to-end demo when the user wants the CLI to create or bind a project, clone a quickstart, write env, and print next steps.
- Use `agora quickstart ...` when the user wants to clone or re-bind an official starter repo without necessarily creating a new project.
- Treat `project env` as the primary way to export project development config.
- Treat `project env write` as the generic file-writing companion for project App ID/App Certificate values.
- Treat `quickstart env write` as the template-aware env writer for official quickstarts.
- Do not expose secrets unless the user explicitly asks for `--with-secrets`.
- Treat `project doctor` as a readiness checker, not a full Conversational AI onboarding flow.
- Do not present `agora-cli-preview` as current.
- Do not call undocumented commands such as `agora convoai init`.
