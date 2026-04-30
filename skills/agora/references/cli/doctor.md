# Agora CLI Doctor

Verified against Agora CLI `0.1.7`.

## Purpose

`agora project doctor` checks whether a project is control-plane ready for Conversational AI development from the CLI's point of view.

It verifies:

- logged-in session
- project resolution or current-project context
- feature readiness
- basic project configuration such as App ID presence
- in `--deep` mode, repo-local `.agora` metadata and quickstart env consistency checks where applicable

It does not replace the full Conversational AI quickstart, RTM runtime validation, or end-to-end sample validation.

## Commands

```bash
agora project doctor [project]
agora project doctor --json
agora project doctor --feature convoai
agora project doctor --feature rtc
agora project doctor --feature rtm
agora project doctor --deep
```

## Interpreting Results

Verified result states in `0.1.7`:

- `healthy`: project is ready from the CLI's current checks
- `warning`: partially ready, but not fully clean
- `not_ready`: blocking issues were found
- `auth_error`: not logged in or project context cannot be resolved

Exit behavior verified in `0.1.7`:

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

If RTM or a related capability was just enabled and the first run still fails, allow bounded wait/retry before concluding the project is still broken. Control-plane enablement may surface before the runtime service is actually usable.

## Deep Mode

`--deep` is part of the verified CLI surface in `0.1.7`. It runs deeper repo-local checks for `.agora` metadata and quickstart env consistency where applicable.

Do not claim `--deep` proves RTC or RTM runtime connectivity. It remains a CLI readiness check.

## First-Success Boundary

Treat doctor results as **control-plane readiness only**:

- `healthy` / `warning` can mean the project is configured correctly at the CLI layer
- they do **not** prove RTM is already usable
- they do **not** prove the official sample can start, open, survive `Try it now`, and complete a conversation

## Fix Mode

`--fix` is not in the verified `0.1.7` command surface. Do not claim broad automatic remediation behavior unless a future CLI version documents it.

For safe guidance, prefer explicit remediation commands over "the CLI will fix this automatically."
