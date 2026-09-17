---
name: agora-rtc-first-success
description: >-
  Official Quickstart workflow for a new Agora RTC one-to-one video
  call. Use for build, try, run, onboarding, or First Success requests when no
  working RTC baseline exists. Requires a current app run; claims about call
  quality or bidirectional media require user-provided evidence.
license: MIT
metadata:
  author: agora
  version: '1.0.0'
---

# Agora RTC First Success

Use this workflow when [README.md](README.md) classifies an RTC request as
`quickstart`. The goal is a current, real-device one-to-one media result, not
only source generation or control-plane readiness.

## Official Baseline

Use the official Next.js RTC video-call Quickstart selected by:

```text
template: nextjs
scenario: video-call
required feature: rtc
```

Use [../cli/README.md](../cli/README.md) and
[../cli/quickstarts.md](../cli/quickstarts.md) for current CLI syntax and
readiness rules. Do not duplicate or infer CLI behavior here.

Do not scaffold a replacement app, reconstruct RTC lifecycle code from memory,
or switch to an SDK-first implementation while this workflow is unresolved. A
minimal source fix is allowed only when an observed defect in the official
Quickstart blocks the documented path.

## Routing Rule

Enter this workflow when the user asks to create, build, run, try, demo,
onboard, or reach First Success for an RTC call and has not stated that a real
RTC call already worked.

Skip this workflow for an explicit SDK/API concept, code review, or focused
implementation question. If the user reports a prior working RTC baseline and
asks for a new feature, use that report for routing but do not describe it as a
current Agent-observed verification.

If the user asks to verify RTC now, historical runs never satisfy the current
run. Start the Quickstart and collect fresh evidence.

## Evidence Contract

Track current-run evidence in the conversation:

```yaml
rtc_first_success:
  project_ready:
    status: pending
    source: agent_observed
  quickstart_ready:
    status: pending
    source: agent_observed
  app_running:
    status: pending
    source: agent_observed
  user_experience_verified:
    status: pending
    source: user_confirmed
```

Allowed `status` values are `pending`, `passed`, and `blocked`. Do not change a
field to `passed` without evidence from its declared source in the current run.

### Agent-observed evidence

- `project_ready`: a directly usable project is selected, RTC is available,
  required credentials are present, and project Doctor has no blocking issue.
- `quickstart_ready`: the CLI successfully selected `nextjs + video-call`,
  created or opened the official Quickstart at a known path, wrote its expected
  env file, validated the matching manifest, and completed dependency setup.
- `app_running`: the start command returned by the CLI was run as returned, the
  process remains active, and a real request to its local URL returns a
  non-empty successful page.

### User-confirmed evidence

- `user_experience_verified`: the user provides evidence of a successful
  bidirectional remote audio and video call in the same channel.

After `app_running` passes, give the user the exact local URL. Do not enter the
call or request camera or microphone permission on the user's behalf unless
explicitly asked. Report that the Quickstart is running. Do not claim a
successful RTC call based on startup or page availability alone; describe call
quality or bidirectional media only when the user provides that evidence.

## What Does Not Prove First Success

None of these, alone or together, prove complete RTC First Success:

- the repository was cloned or generated
- credentials or `.env.local` exist
- `agora doctor`, `agora project doctor`, or Quickstart Doctor passes
- tests, lint, typecheck, or build passes
- the server process starts
- the local URL returns HTTP 200
- a token request returns HTTP 200
- one page joins and renders only its local preview
- automated fake-media or headless-browser results
- a successful run from an earlier task

These observations can advance only the matching project, Quickstart, or app
gate. Claims of a successful call still require the user's current-run evidence.

## Execution State Machine

Stay in the current unresolved state. Do not jump to custom RTC implementation
or declare completion.

| State | Action | Advance when |
|---|---|---|
| `cli_readiness` | Run the read-only CLI version, PATH, config, and auth checks required by the CLI reference | The installed CLI exposes the `nextjs + video-call` scenario and is ready for the selected non-interactive command |
| `project_readiness` | Inspect the selected or current project and verify RTC, App ID, App Certificate, and Doctor results | `project_ready` passes |
| `quickstart_setup` | Run `agora init <name> --template nextjs --scenario video-call --project <project> --json` or the equivalent decomposed Quickstart flow, then complete the returned dependency setup without starting a replacement command | `quickstart_ready` passes |
| `app_start` | Run the start step returned by the CLI exactly from the generated directory and keep the process active | `app_running` passes |
| `user_experience` | Hand off the local URL; leave media verification pending without prescribing a test setup | The user provides evidence of a bidirectional call and `user_experience_verified` passes |
| `complete` | Report RTC First Success with evidence ownership | All four gates are `passed` in the current run |

Use an existing directly usable project when the user selected one or when the
current project is already valid. Project creation, feature enablement, or any
other remote mutation requires its own explicit authorization. Local
Quickstart setup does not authorize those remote writes.

## CLI and Command Integrity

Run CLI readiness before `init`, Quickstart writes, project mutation, or login.
Use JSON output for agent branching.

The CLI resolves package-manager availability after cloning and returns
environment-specific `nextSteps`. Run those commands as returned before
adapting them. Do not replace them with a remembered pnpm, npm, npx, framework,
port, or wrapper command.

For the standard RTC Next.js Quickstart, setup flows directly from the returned
dependency-install step to the returned dev-server start step. Do not add
`test`, `lint`, `typecheck`, or a production `build` between them unless that
command appears in `nextSteps` or the user explicitly requested it. A failed
start may justify narrowly scoped diagnostics for the observed error; it does
not retroactively authorize a full test suite.

If the returned setup strategy is unavailable, report the CLI diagnostic and
leave the state blocked. Installing or upgrading a system runtime requires user
approval. Keep the generated credential file secret and never print its values.

## Execution Environment Boundary

Keep dependency installation in the sandbox. Treat a long-running start step
that depends on file watching, a browser session, or media devices as
host-sensitive and run the exact CLI-returned command with the minimum required
host access. Run no separate pre-start verification unless permitted by the
command-integrity rule above.

If the exact start command was first run in a sandbox and fails because a host
capability is unavailable, preserve that failure and rerun the same command on
the host. Change the command or use a production fallback only after the same
command also fails in host execution. For `EMFILE: too many open files, watch`,
use a single `fs.watch()` control and compare sandbox and host behavior before
attributing the error to descriptor exhaustion or a leak.

## Real-Device Verification

Give the user the local URL without prescribing how to test the call. If the
user reports audio-only, video-only, one-way media, local preview, or a waiting
state, do not claim a successful bidirectional video call.

Ask for only unresolved observations. Do not ask the user to repeat setup facts
already observed by the Agent.

## Failure and Resume Rules

- Attribute failures to the layer directly observed: CLI, project readiness,
  Quickstart setup, app start, page join, remote audio, or remote video.
- Preserve passed current-run gates when retrying a later stage, unless the app
  process, channel, project, or generated Quickstart changes.
- If the app process restarts, re-check `app_running` and repeat the user
  experience verification.
- If the user changes channels before completion, repeat the user experience
  verification.
- If host camera, microphone, browser-session, Keychain, VPN, or GUI state is
  unavailable from a sandbox, classify host state as unknown and request the
  minimum host-scoped action. Do not infer host failure from sandbox evidence.
- Never claim complete First Success while any gate is pending or blocked.

## Status Output

When `project_ready`, `quickstart_ready`, and `app_running` pass while
`user_experience_verified` remains pending, say: `The RTC Quickstart is prepared
and the app is running; user experience verification is pending.` Do not say
that RTC First Success is complete.

Keep routine replies natural. Show the full gate block on the first RTC
First Success reply, when blocked, or when the user asks for status. When one
field advances, a short update is enough:

```text
rtc_first_success: 2/4 -> 3/4; next: hand off the local URL
```

At completion, state which fields were Agent-observed and which were
user-confirmed. Do not collapse them into a claim that the Agent independently
verified real-device media.
