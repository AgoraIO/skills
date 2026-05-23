# Agora CLI Automation and Machine-Readable Use

<!-- applies-from: v0.2.1 -->

Use this file when the user needs script-safe CLI usage, machine-readable output, environment overrides, or agent-oriented command discovery.

Verified against Agora CLI `0.2.1`.

> **Agents:** start with [CLI readiness](README.md#cli-readiness-agents) in [README.md](README.md) before any mutating command.

## Rule for Agents

If an agent or script needs to consume CLI output, prefer an explicitly machine-readable form:

```bash
agora ... --json
```

For command discovery, prefer:

```bash
agora introspect --json
```

Each `commands[]` record includes `headlessSafe` and `interactivity`. Prefer commands where `headlessSafe` is true; skip flows marked `interactive-browser` or similar in agent terminals.

For environment-variable discovery, prefer:

```bash
agora env-help --json
```

For curated workflow discovery, prefer:

```bash
agora skills list --json
```

For project environment values, prefer:

```bash
agora project env --json
```

Do not tell agents to parse pretty output unless the user explicitly wants human-readable terminal text.

## Output Modes

Verified in `0.2.1`:

- default output mode: `pretty`
- one-shot override: `--json`
- persistent default: `agora config update --output json`
- stable JSON envelopes for most action commands include `ok`, `command`, `data`, and `meta`
- global `--quiet` suppresses success output; rely on exit code
- global `--debug` echoes structured logs to stderr without changing JSON envelopes
- global `--yes` / `-y` accepts defaults for confirmation prompts without starting new interactive OAuth flows in JSON, CI, or non-TTY contexts
- in non-interactive runs, `agora init` requires `--template` or fails with `QUICKSTART_TEMPLATE_REQUIRED`

> ⚠️ Deprecated in v0.2.0: `--verbose` and `AGORA_VERBOSE`. Use `--debug` and `AGORA_DEBUG` instead.

`agora project env` is special:

- it prints the selected export format directly
- `--json` or `--format envelope` returns the unified JSON envelope
- `--format shell` returns shell export lines for direct `source <(...)>`

Useful commands:

```bash
agora config path
agora config get
agora config update --output json
agora config update --debug=true
agora introspect --json
agora --help --all --json
agora env-help --json
agora skills list --json
agora mcp serve
agora project env --json
agora auth status --json
source <(agora project env --format shell)
```

## Init JSON Fields

Successful `agora init --json` responses include `projectSelectionReason` (`explicit_project`, `new_project`, `most_recent`, etc.) for deterministic agent branching.

## Progress and MCP

Long-running commands emit NDJSON `progress` events on stdout before the terminal envelope. Stages include `clone:start`, `clone:complete`, and `clone:override` when `AGORA_QUICKSTART_<TEMPLATE>_REPO_URL` overrides the clone URL.

MCP clients may pass `_meta.progressToken` to receive `notifications/progress` for long-running tools.

## Persisted Defaults

The example config for `0.2.1` includes these persisted defaults:

- `output`
- `apiBaseUrl`
- `oauthBaseUrl`
- `oauthClientId`
- `oauthScope`
- `telemetryEnabled`
- `browserAutoOpen`
- `logLevel`
- `debug`

## Local Isolation

For local testing, isolated automation, or CI-style runs, use:

```bash
AGORA_HOME=/custom/path
```

Use an isolated `AGORA_HOME` for CI, test runs, and multi-agent worktrees so one agent does not mutate another agent's selected project or auth/session files.

Other verified environment overrides are discoverable through `agora env-help --json`, including `AGORA_NO_INPUT`, `AGORA_DEBUG`, `AGORA_PROJECT_CACHE_TTL_SECONDS`, `AGORA_DISABLE_CACHE`, `AGORA_QUICKSTART_<TEMPLATE>_REPO_URL`, and the `agora open` URL overrides.

## Suggested Agent Pattern

After [CLI readiness](README.md#cli-readiness-agents) passes on a `0.2.0+` CLI:

```bash
agora doctor --json
agora auth status --json
agora login
agora project use <project>
agora project env --json
agora project doctor --json
```

Full demo setup:

```bash
agora init my-python-demo --template python --new-project --json
```

Official quickstart repo (template-aware env keys):

```bash
agora quickstart env write
```

Generic project dotenv only when the repo is not an official quickstart:

```bash
agora project env write
```

Upgrade guidance:

```bash
agora upgrade --check --json
```

In CI, installer-managed `agora upgrade` is blocked by default (`ciBlocked: true` in JSON). Use `--check` only unless `AGORA_ALLOW_UPGRADE_IN_CI=1` is intentionally set.

`agora open --target docs` defaults to URL-only output in CI/non-TTY unless `--browser` is passed.

## Auth and Error Handling

Unauthenticated `agora auth status --json` is recoverable. It exits `3` with `AUTH_UNAUTHENTICATED`.

`agora doctor --json` exit codes:

- `0`: healthy install
- `1`: blocking install issues
- `2`: warnings
- `3`: auth or session issues

Branch on documented `error.code` values first. Level 2 catalog: `https://agoraio.github.io/cli/md/error-codes.md`

## Telemetry

```bash
agora telemetry status
agora telemetry disable
agora telemetry enable
DO_NOT_TRACK=1 agora <command>
```

## Things Not to Promise

- Do not claim pretty output is a stable API.
- Do not recommend `agora project show --json` as the primary env-export workflow when `agora project env` is available.
- Do not use `project env write` for official quickstart credential seeding when `quickstart env write` is required.
- Do not use `./agora` in user-facing examples unless running a locally built CLI repo binary.
