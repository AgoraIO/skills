# Agora CLI Doctor

<!-- applies-from: v0.2.1 -->

Use this file when the user needs either local CLI install diagnostics (`agora doctor`) or project readiness diagnostics (`agora project doctor`).

Verified against Agora CLI `0.2.1`.

> **Agents:** run [CLI readiness](README.md#cli-readiness-agents) before doctor-driven recovery loops.

## Purpose

`agora doctor` checks the local CLI install.

`agora project doctor` checks whether a project is control-plane ready for feature development from the CLI's point of view.

Use `agora doctor` first when the failure looks local to the workstation or shell. Use `agora project doctor` when auth works and the problem is project configuration or feature readiness.

## Install Doctor

Top-level `agora doctor` is available in `0.2.0+`. For `0.1.7–0.1.x`, use the read-only version and PATH checks in [CLI readiness](README.md#cli-readiness-agents), then prefer upgrading to the verified `0.2.1` baseline before deeper diagnostics.

```bash
agora doctor
agora doctor --json
agora doctor --quiet
```

Verified `0.2.1` install-doctor checks include:

- binary path and PATH resolution
- installed version
- `AGORA_HOME` writability
- API and OAuth DNS/network reachability
- auth/session state
- known MCP host detection

Verified `0.2.1` install-doctor exit codes:

- `0`: healthy
- `1`: blocking install issues
- `2`: warnings
- `3`: auth or session issues

Common recovery paths:

- PATH issue: run the shell-specific command printed by `agora doctor`, or use `which -a agora` to find a shadowing old binary. Do not uninstall automatically; ask before removing a stale binary — see [README.md](README.md#cli-readiness-agents)
- CLI below `0.1.7` or config schema newer than the running binary: follow the curl-first upgrade path in [install-auth.md](install-auth.md#version-gate-and-upgrade)
- network or DNS issue: fix connectivity or proxy settings before retrying auth
- auth issue: run `agora login`

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

Verified result states in `0.2.1`:

- `healthy`: project is ready from the CLI's current checks
- `warning`: partially ready, but not fully clean
- `not_ready`: blocking issues were found
- `auth_error`: not logged in or project context cannot be resolved

Exit behavior verified in `0.2.1`:

- healthy doctor run exits `0`
- blocking readiness issues exit `1`
- warning-only readiness issues exit `2`
- auth or session issues exit `3`

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

`--deep` is part of the verified CLI surface. It runs deeper repo-local checks for `.agora` metadata and quickstart env consistency where applicable.

Do not claim `--deep` proves RTC or RTM runtime connectivity. It remains a CLI readiness check.

## First-Success Boundary

Treat doctor results as **control-plane readiness only**:

- `healthy` / `warning` can mean the project is configured correctly at the CLI layer
- they do **not** prove RTM is already usable
- they do **not** prove the official sample can start, open, survive `Try it now`, and complete a conversation

## Fix Mode

`--fix` is not in the verified command surface. Do not claim broad automatic remediation behavior unless a future CLI version documents it.

For safe guidance, prefer explicit remediation commands over "the CLI will fix this automatically."
