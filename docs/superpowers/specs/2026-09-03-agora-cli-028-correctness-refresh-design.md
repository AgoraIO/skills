# Agora CLI 0.2.8 Correctness Refresh Design

**Date:** 2026-09-03
**Status:** Implemented locally
**Scope:** Refresh the bundled Agora CLI references against release `0.2.8`
using the repository's existing maintenance methodology.

## Problem

The branch updates the CLI references from older verification points to `0.2.8`,
but initially introduced a patch-version compatibility matrix and claims of
behavioral parity from `0.2.2` through `0.2.8`. That is not how this repository
has handled earlier CLI refreshes.

The established model separates two facts:

- **Last verified** identifies the release against which a reference file was
  actually checked.
- **Minimum CLI** identifies the oldest release allowed through the readiness
  gate.

The installed CLI's `agora introspect --json` output is authoritative for its
live command tree when the bundled list is incomplete. It is an escape hatch,
not a mandatory per-command compatibility workflow.

## Decision

- Set Last verified to `0.2.8` for CLI files whose claims were checked against
  the `v0.2.8` tag.
- Set the uniform Minimum CLI to `0.2.2` because older releases contain stale
  Python quickstart repository mappings.
- Do not maintain a `0.2.2` through `0.2.8` compatibility matrix.
- Do not claim that every patch release was tested or shares one behavior
  contract.
- Keep readiness lightweight: version, PATH, config compatibility, and doctor.
- Use `agora introspect --json` before claiming that a command or flag does not
  exist.
- Keep exact-tag documentation, source, and tests in the maintenance audit; do
  not require users to clone the CLI repository before normal CLI operations.
- Keep schema recovery version-agnostic when the supported range spans multiple
  schema versions.

## Maintenance Evidence

The target source is Agora CLI tag `v0.2.8`, commit
`96c228b0036f59b79e2d2da3df97d027cb9c4859`.

Checked evidence includes:

- generated `docs/commands.md` for commands and flags
- `docs/automation.md` for JSON envelopes, output modes, progress, and result fields
- `docs/install.md` and `docs/troubleshooting.md` for installer and recovery behavior
- `internal/cli/config.go` and `runtime_support.go` for persisted config and schema behavior
- `internal/cli/auth.go` and `projects.go` for region and project context
- `internal/cli/quickstart.go` and `integration_quickstart_test.go` for current and legacy env layouts
- `internal/cli/install_doctor.go` and `doctor.go` for doctor checks, states, and exit behavior
- `internal/cli/commands.go` and `webhooks.go` for webhook command and secret behavior

An exact `0.2.8` binary was not executed: the tag requires Go `1.26.5`, and both
sandboxed and host-scoped toolchain downloads timed out. No runtime-binary claim
may be based on that failed build attempt.

## Runtime Guidance

```text
agora version
which -a agora              # where.exe on Windows

version < Minimum CLI
  -> stop normal workflow
  -> offer the approved installer after authorization

version >= Minimum CLI
  -> run doctor
  -> continue with bundled guidance

command or flag availability is uncertain
  -> use agora introspect --json
  -> do not invent a command that is absent
```

Runtime use does not require exact-tag source inspection. Exact-tag inspection
belongs to future reference maintenance, explicit old-version investigation, or
CLI bug diagnosis.

## Content Changes

- Remove the patch-version compatibility matrix and per-patch test claims.
- Use `Last verified against Agora CLI 0.2.8. Minimum CLI 0.2.2.` consistently.
- Update Python and Go fresh quickstarts to `server/.env.local` with
  `AGORA_APP_ID` and `AGORA_APP_CERTIFICATE`.
- Preserve detected legacy Python and Go layouts during env writes.
- Keep project creation region guidance aligned with the verified `0.2.8` command surface.
- Keep config mismatch recovery free of hard-coded schema numbers.
- Correct the persisted `0.2.8` config field list.
- Document webhook authorization and secret boundaries without copying the full generated command reference.
- Remove the stale Python env-name block from the ConvoAI quickstart reference.
- Update eval cases to assert Last verified, Minimum CLI, current env behavior, and the existing introspection escape hatch.

## Files

- `CHANGELOG.md`
- `skills/agora/SKILL.md`
- `skills/agora/references/cli/README.md`
- `skills/agora/references/cli/automation.md`
- `skills/agora/references/cli/doctor.md`
- `skills/agora/references/cli/env.md`
- `skills/agora/references/cli/install-auth.md`
- `skills/agora/references/cli/projects.md`
- `skills/agora/references/cli/quickstarts.md`
- `skills/agora/references/conversational-ai/README.md`
- `skills/agora/references/conversational-ai/quickstarts.md`
- `tests/eval-cases.md`

`CONTRIBUTING.md` and `references/doc-fetching.md` retain their established
maintenance and runtime lookup rules; no new compatibility framework is added.

## Validation

```bash
bash scripts/validate-skills.sh
skills-ref validate skills/agora
claude plugin validate . --strict
claude plugin validate ./.claude-plugin/plugin.json
claude plugin validate ./skills --strict
git diff --check
```

Also scan for compatibility-matrix terminology, per-patch test claims, stale env
layouts, and old verification labels. Tool absence or validator invocation
incompatibility must be reported rather than treated as a passing result.

## Acceptance Criteria

- CLI references use Last verified `0.2.8` and Minimum CLI `0.2.2`.
- No patch-version compatibility matrix or per-patch parity claim remains.
- Runtime readiness follows the established version/PATH/config/doctor flow.
- `introspect` remains an escape hatch for live command availability.
- Exact-tag source inspection remains a maintenance activity.
- Current and legacy quickstart env behavior matches `v0.2.8` evidence.
- Eval cases enforce the same model.
- Repository validation and `git diff --check` pass where tools are available.
