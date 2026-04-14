# Agora CLI Automation and Machine-Readable Use

Verified against Agora CLI `0.1.1`.

## Rule for Agents

If an agent or script needs to consume CLI output, prefer:

```bash
agora ... --json
```

Do not tell agents to parse pretty output unless the user explicitly wants human-readable terminal text.

## Output Modes

Verified in `0.1.1`:

- default output mode: `pretty`
- one-shot override: `--json`
- persistent default: `agora config update --output json`

Useful commands:

```bash
agora config path
agora config get
agora config update --output json
```

## Persisted Defaults

The example config for `0.1.1` includes these persisted defaults:

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

## Suggested Agent Pattern

Use this order:

```bash
agora login
agora project use <project>
agora project doctor --json
```

If the agent needs to inspect defaults first:

```bash
agora config get --json
```

## Things Not to Promise

- Do not claim pretty output is a stable API.
- Do not claim hidden env vars beyond the documented config directory override and public config commands unless you have verified them for the user's version.
