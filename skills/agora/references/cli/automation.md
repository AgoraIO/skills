# Agora CLI Automation and Machine-Readable Use

Verified against Agora CLI `0.1.7`.

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

For project environment values, prefer:

```bash
agora project env --json
```

Do not tell agents to parse pretty output unless the user explicitly wants human-readable terminal text.

## Output Modes

Verified in `0.1.7`:

- default output mode: `pretty`
- one-shot override: `--json`
- persistent default: `agora config update --output json`
- stable JSON envelopes for most action commands include `ok`, `command`, `data`, and `meta`
- global `--quiet` suppresses success output; rely on exit code
- global `--verbose` echoes structured logs to stderr without changing JSON envelopes

`agora project env` is special:

- it prints the selected export format directly
- `--json` returns raw env JSON, not the normal CLI envelope
- `--shell` returns `export ...` lines for direct `eval`

Useful commands:

```bash
agora config path
agora config get
agora config update --output json
agora introspect --json
agora --help --all --json
agora project env --json
agora auth status --json
eval "$(agora project env --shell)"
```

## Persisted Defaults

The example config for `0.1.7` includes these persisted defaults:

- `output`
- `apiBaseUrl`
- `oauthBaseUrl`
- `oauthClientId`
- `oauthScope`
- `telemetryEnabled`
- `browserAutoOpen`
- `logLevel`
- `verbose`

## Local Isolation

For local testing, isolated automation, or CI-style runs, use:

```bash
AGORA_HOME=/custom/path
```

This moves the CLI's local state away from the default config directory.

Use an isolated `AGORA_HOME` for CI, test runs, and multi-agent worktrees so one agent does not mutate another agent's selected project or auth/session files.

## Suggested Agent Pattern

Use this order:

```bash
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
agora --upgrade-check
```

## Auth and Error Handling

In `0.1.7`, unauthenticated `agora auth status --json` is a recoverable state. It exits `3` and reports `AUTH_UNAUTHENTICATED` in the JSON error envelope.

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
