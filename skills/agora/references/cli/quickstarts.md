# Agora CLI Init, Quickstarts, and Recipes

<!-- applies-from: v0.2.1 -->

Use this file when the user wants `agora init`, `agora recipes ...`, `agora quickstart ...`, or repo-local project binding for an official quickstart or recipe.

Last verified against Agora CLI `0.2.9`. Minimum CLI `0.2.1`.

> **Agents:** complete [CLI readiness](README.md#cli-readiness-agents) in [README.md](README.md) before any command here.

## Core Decision

Use:

```bash
agora init <name> --template <template>
```

when the user wants a new runnable demo with project binding and env writing handled by the CLI.

Use:

```bash
agora recipes list --type all|ai|rtc
agora recipes show <slug>
agora init <name> --recipe <slug>
```

to discover official recipes and initialize one whose API detail includes a supported `cli.env` contract. Discovery is read-only; only `init --recipe` clones or writes files.

Use:

```bash
agora quickstart create <name> --template <template> --project <project>
agora quickstart env write <path-or-repo> --project <project>
```

when the user wants to clone or re-bind an official quickstart separately from project creation.

Use low-level `agora project ...` commands when the workflow must be decomposed, resumed, or inspected step by step.

## Commands

```bash
agora init my-nextjs-demo --template nextjs
agora init my-python-demo --template python
agora init my-go-demo --template go
agora init my-demo --template python --project my-existing-project
agora init my-demo --template python --new-project
agora init my-rtm-demo --template nextjs --new-project --feature rtc --feature rtm --rtm-data-center AP
agora init my-app --template nextjs --add-agent-rules cursor
agora init my-tool-agent --recipe tool-calling --project my-existing-project
```

Agent-safe non-interactive example:

```bash
agora init my-python-demo --template python --new-project --json
```

`agora init` creates or binds an Agora project, clones the selected quickstart, writes its env file, persists repo-local project context, and prints next steps. Newly created projects default to `rtc`, `rtm`, and `convoai`; `convoai` also implies `rtm`.

In `--json`, `--yes`, CI, or non-TTY runs, pass exactly one of `--template` or `--recipe`. Without either source the CLI fails fast with `INIT_SOURCE_REQUIRED`; passing both returns `INIT_SOURCE_CONFLICT`. Do not run bare `agora init <name>` in agent terminals because interactive source prompts cannot be answered there.

Recipe detail comes from the versioned official API at `recipes.agora.io`. The API returns only official recipes. A recipe can be listed and shown without being CLI-initializable: when its detail omits `cli.env`, `init --recipe` stops before project creation or cloning with `RECIPE_INIT_UNSUPPORTED`. Do not guess env paths or credential keys; follow the recipe document manually or choose a supported recipe.

```bash
agora quickstart list
agora quickstart list --details
agora quickstart list --show-all
agora quickstart create my-python-demo --template python --project my-project
agora quickstart env write my-python-demo --project my-project
agora quickstart env write /abs/path/to/my-python-demo --json
```

For CI or source-only work without an Agora login session, request clone-only behavior explicitly:

```bash
agora quickstart create my-nextjs-demo --template nextjs --template-only
```

This clones the official template without resolving a remote project or writing credentials. Without a resolved project or `--template-only`, non-interactive runs fail before cloning with `QUICKSTART_PROJECT_REQUIRED`. Configure and verify the template's env file separately when CI credentials are available.

`quickstart create` shells out to `git clone`. Clone subprocesses disable git credential helpers so agent and CI runs do not hang on macOS keychain prompts.

Typed clone failures:

| Code | Recovery |
|------|----------|
| `QUICKSTART_GIT_MISSING` | Install `git` and retry |
| `QUICKSTART_REF_INVALID` | Pass a valid `--ref` (no leading `-`) |
| `QUICKSTART_REPO_OVERRIDE_INVALID` | Fix or unset `AGORA_QUICKSTART_<TEMPLATE>_REPO_URL` |

> ⚠️ Removed in v0.2.0: `agora quickstart list --verbose`. Use `agora quickstart list --details` instead.

## Project Binding

The CLI writes repo-local non-secret project metadata to:

```text
.agora/project.json
```

Resolution order:

1. explicit `--project` or positional project argument
2. repo-local `.agora/project.json` resolved from the target repo path
3. global context set by `agora project use`

`.agora/project.json` can include durable metadata such as project ID, project name, region, template, env path, and detected `projectType`. Do not put secrets in this file.

## Env Writing

`quickstart env write` is template-aware. It writes the variable names and env file path the selected official quickstart expects:

| Template | Target | Variables |
|---|---|---|
| Generic project env | selected dotenv file | `AGORA_APP_ID`, `AGORA_APP_CERTIFICATE` |
| Next.js quickstart | `.env.local` | `NEXT_PUBLIC_AGORA_APP_ID`, `NEXT_AGORA_APP_CERTIFICATE` |
| Python quickstart | `server/.env` | `AGORA_APP_ID`, `AGORA_APP_CERTIFICATE` |
| Go quickstart | `server/.env` | `AGORA_APP_ID`, `AGORA_APP_CERTIFICATE` |
| Android quickstart server | `server/.env.local` | `AGORA_APP_ID`, `AGORA_APP_CERTIFICATE` |

**Agent rule:** for official quickstarts, always use **`agora quickstart env write`**, not `agora project env write`. The template-aware writer selects the expected path and keys, preserves example values, and normalizes unsupported legacy `APP_ID` / `APP_CERTIFICATE` aliases for Python and Go.

Existing `.env` and `.env.local` files are preserved. The CLI updates existing credential keys, appends missing credentials, and comments duplicate or stale Agora credential aliases for the selected runtime.

Use [env.md](env.md) for generic `agora project env` and `agora project env write` behavior.

## Agent Guidance

- Complete [CLI readiness](README.md#cli-readiness-agents) before `init` or env writes.
- Prefer `agora init <name> --template <template> --json` for one-shot onboarding.
- Pass exactly one of `--template` or `--recipe` in agent, CI, and `--json` init runs.
- Prefer `agora quickstart env write ... --json` when seeding or re-syncing official quickstart repos.
- Do not substitute manual `git clone` until `init` / `quickstart create` fails with a documented error code and recovery is exhausted. `quickstart create --template-only` is the supported unauthenticated clone path.
- Use `agora project doctor --json` after binding to check control-plane readiness, but do not treat it as proof that the sample can run end to end.
- Use `agora doctor --json` when the failure looks local to the CLI install rather than to the project.
- Use `agora` in user-facing commands for an installed CLI. Use `./agora` only when running a local binary built from the CLI repository.
