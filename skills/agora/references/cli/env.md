# Agora CLI Project Environment Export

<!-- applies-from: v0.2.1 -->

Use this file when the user needs to export project credentials, write dotenv files, or explain the difference between generic project env and quickstart env commands.

Verified against Agora CLI `0.2.1`.

> **Agents:** complete [CLI readiness](README.md#cli-readiness-agents) first. For official quickstarts, **`quickstart env write` is mandatory** — see warning below.

`agora project env` is the CLI's primary generic project-environment export command. Official quickstart repos have a separate template-aware writer: `agora quickstart env write`.

## Critical Agent Rule

Using `agora project env write` on an official Python or Go quickstart writes **`AGORA_APP_ID`** to a generic dotenv path. Those samples read **`APP_ID`** from `server/.env` or `server-go/.env`. The backend starts with empty credentials.

For official quickstarts, always use:

```bash
agora quickstart env write [repo-path]
```

Use:

```bash
agora project env
```

when the user wants project env vars.

Use:

```bash
agora project env write [path]
```

when they explicitly want generic Agora App ID / App Certificate values materialized into a dotenv file.

Use:

```bash
agora quickstart env write [repo-path]
```

when working inside an official quickstart or writing template-specific env names such as `NEXT_PUBLIC_AGORA_APP_ID` or `APP_ID`.

## Export Commands

Default behavior:

```bash
agora project env
```

This prints non-sensitive dotenv lines to `stdout`. It does not write a file.

Other supported forms:

```bash
agora project env --shell
agora project env --json
agora project env --format dotenv
agora project env --format shell
agora project env --format envelope
agora project env --format json
agora project env --project <project>
agora project env --with-secrets
```

Use cases:

- default dotenv output: paste into `.env`, redirect to a file, or inspect values
- `--shell`: `source <(agora project env --format shell)`
- `--json` or `--format envelope`: agents, CI, or scripts using the unified JSON envelope
- `--project <project>`: export a non-current project without changing local context
- `--with-secrets`: include sensitive values such as the app certificate

Option rules:

- `--format shell` and `--shell` are equivalent output choices; use one or the other
- `--format` and `--shell` cannot be combined
- `--json` and `--shell` cannot be combined
- invalid `--format` values fail with: `` `--format` must be one of: dotenv, shell, envelope, json ``

## Project Env Variables

The verified `0.2.1` project env export contract focuses on:

- `AGORA_APP_ID`
- `AGORA_APP_CERTIFICATE` only when `--with-secrets` is provided

Do not invent alternate names for the CLI env contract. If an agent needs project metadata beyond credentials, use `agora project show --json`.

## Secrets Rule

Secrets are opt-in.

- By default, `agora project env` exports only non-sensitive development config.
- `AGORA_APP_CERTIFICATE` is emitted only with `--with-secrets`.
- If the target project does not have an app certificate, `--with-secrets` fails instead of silently emitting an empty value.

## Generic Project Env Writing

`agora project env write [path]` writes generic `AGORA_APP_ID` and `AGORA_APP_CERTIFICATE` values to a dotenv file. If the selected project has no App Certificate, env writing cannot seed a token-ready app.

Supported flags:

```bash
agora project env write
agora project env write apps/web/.env.local
agora project env write --append
agora project env write --overwrite
agora project env write .env.local --template nextjs
```

Write rules:

- explicit `path`: write exactly that target path
- no `path`: choose the best default `.env*` target based on the current project directory
- `--append`: append App ID and App Certificate values when no existing values are present
- `--overwrite`: replace the target file with only Agora App ID and App Certificate values
- `--template nextjs|standard`: override the workspace detector when the credential key layout must be forced
- do not combine `--append` and `--overwrite`

Ask for explicit approval before running `--overwrite`, and state the target path before writing. Prefer append/update behavior for existing env files.

Do not use template files such as `.env.example`, `.env.sample`, or `.env.template` as write targets for real values or secrets.

In `0.2.1`, `project env write` updates or creates repo-local `.agora/project.json` metadata and records detected `projectType` / `envPath` when missing.

## Quickstart Env Writing

Official quickstarts use template-specific env names and file paths. Use [quickstarts.md](quickstarts.md) for the full flow.

Verified `0.2.1` examples:

```bash
agora quickstart env write my-python-demo --project my-project
agora quickstart env write /abs/path/to/my-go-demo --json
```

Template-specific behavior:

| Template | Target | Variables |
|---|---|---|
| Next.js quickstart | `.env.local` | `NEXT_PUBLIC_AGORA_APP_ID`, `NEXT_AGORA_APP_CERTIFICATE` |
| Python quickstart | `server/.env` | `APP_ID`, `APP_CERTIFICATE` |
| Go quickstart | `server-go/.env` | `APP_ID`, `APP_CERTIFICATE` |

Existing env files are preserved. The CLI updates existing credential keys, appends missing values, and comments duplicate or stale Agora credential aliases for the selected runtime.

## Agent Guidance

- For raw env consumption, prefer `agora project env --json` over `agora project show --json`.
- For shell sessions, prefer `agora project env --format shell`.
- For generic repo setup, use `agora project env write`.
- For official quickstart repos, use `agora quickstart env write` so the correct file path and variable names are used.
- `project env` prints the selected format directly; `project env write` and `quickstart env write` are action commands and can be consumed with `--json`.
