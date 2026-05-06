# Agora CLI Automation and Machine-Readable Use

<!-- applies-from: v0.2.0 -->

Use this file when the user needs script-safe CLI usage, machine-readable output, environment overrides, or agent-oriented command discovery.

Verified against Agora CLI `0.2.0`.

## Rule for Agents

If an agent or script needs to consume CLI output, prefer an explicitly machine-readable form:

```bash
agora ... --json
```

For command discovery, prefer:

```bash
agora introspect --json
```

This returns command metadata, global flags, enum values, pseudo-commands, and version metadata. Use `agora --help --all` for human-readable inspection.

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

Verified in `0.2.0`:

- default output mode: `pretty`
- one-shot override: `--json`
- persistent default: `agora config update --output json`
- stable JSON envelopes for most action commands include `ok`, `command`, `data`, and `meta`
- global `--quiet` suppresses success output; rely on exit code
- global `--debug` echoes structured logs to stderr without changing JSON envelopes
- global `--yes` / `-y` accepts defaults for confirmation prompts without starting new interactive OAuth flows in JSON, CI, or non-TTY contexts

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

## Persisted Defaults

The example config for `0.2.0` includes these persisted defaults:

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

This moves the CLI's local state away from the default config directory.

Use an isolated `AGORA_HOME` for CI, test runs, and multi-agent worktrees so one agent does not mutate another agent's selected project or auth/session files.

Other verified `0.2.0` environment overrides are discoverable through `agora env-help --json`, including `AGORA_NO_INPUT`, `AGORA_DEBUG`, `AGORA_PROJECT_CACHE_TTL_SECONDS`, `AGORA_DISABLE_CACHE`, and the `agora open` URL overrides.

## Suggested Agent Pattern

Use this order:

```bash
agora doctor --json
agora auth status --json
agora login
agora project use <project>
agora project env --json
agora project doctor --json
```

If the agent needs a full demo setup:

```bash
agora init my-python-demo --template python --json
```

If the agent needs to materialize generic project env into the repo:

```bash
agora project env write
```

If the agent is working in an official quickstart repo:

```bash
agora quickstart env write
```

If the agent needs to inspect defaults first:

```bash
agora config get --json
```

If the agent needs project metadata beyond the env contract:

```bash
agora project show --json
```

If the agent needs package-manager-specific update guidance:

```bash
agora upgrade --check
agora self-update --check
agora --upgrade-check
```

## Auth and Error Handling

In `0.2.0`, unauthenticated `agora auth status --json` is a recoverable state. It exits `3` and reports `AUTH_UNAUTHENTICATED` in the JSON error envelope.

`agora doctor --json` returns a stable JSON envelope and uses these verified exit codes:

- `0`: healthy install
- `1`: blocking install issues
- `2`: warnings
- `3`: auth or session issues

Agents should inspect documented error codes and run the matching recovery command. For example, auth errors route to `agora login`; missing project context routes to `agora project use <project>` or an explicit `--project`.

## Telemetry

Useful commands:

```bash
agora telemetry status
agora telemetry disable
agora telemetry enable
```

Runtime opt-out:

```bash
DO_NOT_TRACK=1 agora <command>
```

## Things Not to Promise

- Do not claim pretty output is a stable API.
- Do not recommend `agora project show --json` as the primary env-export workflow when `agora project env` is available.
- Do not claim hidden env vars beyond the documented config directory override and public config commands unless you have verified them for the user's version.
- Do not use `./agora` in user-facing examples unless you are explicitly running a locally built CLI repo binary.
