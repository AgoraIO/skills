# Agora CLI Doctor

Verified against Agora CLI `0.1.1`.

## Purpose

`agora project doctor` checks whether a project is ready for Conversational AI development from the CLI's point of view.

It verifies:

- logged-in session
- project resolution or current-project context
- feature readiness
- basic project configuration such as App ID presence

It does not replace the full Conversational AI quickstart or end-to-end runtime validation.

## Commands

```bash
agora project doctor [project]
agora project doctor --json
agora project doctor --deep
```

## Interpreting Results

Verified result states in `0.1.1`:

- `healthy`: project is ready from the CLI's current checks
- `warning`: partially ready, but not fully clean
- `not_ready`: blocking issues were found
- `auth_error`: not logged in or project context cannot be resolved

Exit behavior verified in `0.1.1`:

- healthy doctor run exits `0`
- blocking readiness issues exit nonzero
- unauthenticated deep-mode doctor exits `3`

## Common Recovery Commands

If doctor reports an auth problem:

```bash
agora login
```

If doctor cannot resolve the target project:

```bash
agora project use <project>
```

If doctor reports ConvoAI feature readiness issues:

```bash
agora project feature enable convoai
```

## Deep Mode

`--deep` is part of the verified CLI surface in `0.1.1`, but runtime preflight is not currently available there.

Verified `0.1.1` behavior:

- doctor still runs
- the runtime-preflight item is reported as skipped
- the message is effectively "Deep runtime preflight is not available in CLI 0.1.1"

Do not promise deeper runtime checks unless you have verified a newer CLI version.

## Fix Mode

`--fix` exists in the command help for `0.1.1`, but do not claim broad automatic remediation behavior unless you have verified it for the user's version.

For safe guidance, prefer explicit remediation commands over "the CLI will fix this automatically."
