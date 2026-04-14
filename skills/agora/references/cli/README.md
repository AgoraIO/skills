# Agora CLI

Use this module when the user is asking how to use the installed `agora` command-line tool.

Verified against Agora CLI `0.1.1` on 2026-04-14. Write guidance for `>=0.1.1`, but label version-sensitive behavior explicitly when it was only verified in `0.1.1`.

## What the CLI Covers

- OAuth login and local session management
- Local CLI defaults and config inspection
- Agora project creation, selection, and inspection
- Feature enablement for `rtc`, `rtm`, and `convoai`
- ConvoAI readiness checks through `agora project doctor`

## Routing

| User's request | Read this file next |
|---|---|
| Install, login, config directory, `whoami`, `auth status` | [install-auth.md](install-auth.md) |
| `project create`, `project list`, `project use`, `project show`, `project feature ...` | [projects.md](projects.md) |
| `project doctor`, readiness, blocking issues, next remediation command | [doctor.md](doctor.md) |
| Scripted usage, machine-readable output, config persistence, `AGORA_HOME` | [automation.md](automation.md) |

## Quick Reference

| Item | Value |
|---|---|
| npm package | `agoraio-cli` |
| Installed command | `agora` |
| Deprecated package | `agora-cli-preview` |
| Minimum skill-supported version | `0.1.1` |
| Default output mode | `pretty` |
| Agent-safe output mode | `--json` |

## Current Command Surface

Verified in CLI `0.1.1`:

- top level: `login`, `logout`, `whoami`, `auth`, `config`, `project`
- auth group: `auth login`, `auth logout`, `auth status`
- config group: `config path`, `config get`, `config update`
- project group: `project create`, `project list`, `project use`, `project show`, `project feature`, `project doctor`
- feature group: `project feature list`, `project feature status`, `project feature enable`

If the user asks for a command outside this surface, do not invent it. Route them to the closest real command or say it is not part of the verified CLI.

## Important Rules

- For agents and scripts, prefer `--json` instead of parsing pretty output.
- Treat `project doctor` as a readiness checker, not a full Conversational AI onboarding flow.
- Do not present `agora-cli-preview` as current.
- Do not call undocumented commands such as `agora convoai init`.
