# Agora CLI 0.2.8 Correctness Refresh Implementation Plan

> **For agentic workers:** Follow the repository's established CLI refresh process. Do not introduce a new runtime compatibility framework.

**Goal:** Align verified CLI reference content with release `0.2.8` while keeping Minimum CLI `0.2.2` and the existing introspection escape hatch.

**Architecture:** Static reference files describe behavior checked against `v0.2.8`. The readiness gate blocks only below Minimum CLI, PATH shadowing, and config incompatibility. Exact-tag source inspection is used during maintenance, not normal user command execution.

---

### Task 1: Audit the target release

- [x] Pin `v0.2.8` to commit `96c228b0036f59b79e2d2da3df97d027cb9c4859`.
- [x] Inspect generated command and automation docs.
- [x] Inspect install, auth, config, project, quickstart, doctor, and webhook source/tests.
- [x] Record that exact-binary execution was unavailable because Go `1.26.5` download timed out.

### Task 2: Apply the established version model

- [x] Set Last verified `0.2.8` only where tag evidence was inspected.
- [x] Set uniform Minimum CLI `0.2.2`.
- [x] Remove the patch-version compatibility matrix and parity claims.
- [x] Keep `agora introspect --json` as the live command-tree authority.
- [x] Remove mandatory non-baseline and exact-tag runtime workflows.

### Task 3: Refresh verified behavior

- [x] Align current and legacy quickstart env layouts.
- [x] Align region and project-create guidance.
- [x] Align doctor checks and result behavior.
- [x] Correct persisted config fields.
- [x] Add stable webhook authorization and secret boundaries.
- [x] Remove conflicting ConvoAI env guidance.

### Task 4: Align evals and release notes

- [x] Update version, command discovery, env, init, doctor, and region evals.
- [x] Remove invented non-baseline runtime eval cases.
- [x] Update the changelog to describe the `0.2.8` refresh and introspection escape hatch.
- [x] Preserve the existing CONTRIBUTING maintenance method.

### Task 5: Validate

- [x] Run repository static validation: passed.
- [x] Run available root and manifest plugin validators: passed with the documented root `CLAUDE.md` warning.
- [x] Attempt `skills-ref`: unavailable in the current environment.
- [x] Record that `claude plugin validate ./skills --strict` treats `./skills` as a plugin root and fails because it has no manifest.
- [x] Run semantic residue scans.
- [x] Run `git diff --check` and inspect final worktree status.
