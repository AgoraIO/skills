---
name: conversational-ai-quickstarts
description: |
  Locked quickstart flow for Agora Conversational AI. Use when no working baseline exists.
  BLOCKING: Do not generate ConvoAI code from memory, scaffold replacement projects, or propose custom architecture before inspecting the official quickstart source. Runtime proof validates the user's environment: quickstart_repo_cloned, official_start_command_run, agent_join_verified, rtc_client_connected.
  SAMPLE INTEGRITY: Run official sample commands verbatim. Do not substitute startup commands or replace the sample. Internally check baseline_gate before every actionable reply; show status only on first reply, gate flips, blocked actions, or user status requests.
license: MIT
metadata:
  author: agora
  version: '1.5.0'
---

# Conversational AI Quickstart

Use this file for `quickstart` and `integration` mode from [README.md](README.md).

## Working-Baseline Rule

A **working ConvoAI baseline** means the developer has already started an Agora ConvoAI agent successfully and the client can join the same RTC channel and interact with it.

The following do **not** count as a working baseline:

- only RTC code exists
- a sample repo is cloned but the agent has never started successfully
- environment variables are present but unverified
- the user only knows the desired backend language or framework

If the user already has a working baseline, exit this file and route back through [README.md](README.md).

## Quickstart Source and Runtime Proof

### Official repo (Path A)

For this flow, pick the correct official template by stack:

- Python baseline (`agent-quickstart-python`) with Bun, using
  `https://github.com/AgoraIO-Conversational-AI/agent-quickstart-python`
- Next.js baseline (`agent-quickstart-nextjs`) with pnpm, using
  `https://github.com/AgoraIO-Conversational-AI/agent-quickstart-nextjs`
- Go baseline (`agent-quickstart-go`) with Makefile-based startup, using the official Go quickstart template for the `go` template family in Agora CLI.

Use this official sample as-is and only adapt documented fields once clone + runtime checks pass.

### Required env mapping by template

Use template-specific env files/keys for the selected official template:

- Next.js quickstart (`agent-quickstart-nextjs`):
  - write `.env.local`
  - `AGORA_APP_ID` -> `NEXT_PUBLIC_AGORA_APP_ID`
  - `AGORA_APP_CERTIFICATE` -> `NEXT_AGORA_APP_CERTIFICATE`
- Python quickstart (`agent-quickstart-python`):
  - write `server/.env`
  - `AGORA_APP_ID` -> `APP_ID`
  - `AGORA_APP_CERTIFICATE` -> `APP_CERTIFICATE`
- Go quickstart (`agent-quickstart-go`):
  - write `server-go/.env`
  - `AGORA_APP_ID` -> `APP_ID`
  - `AGORA_APP_CERTIFICATE` -> `APP_CERTIFICATE`

The quickstart is the source of truth for code shape. The agent does not need to prove Agora's official quickstart works in the abstract before reading or adapting it. It does need runtime proof before claiming the user's environment, Agora project, and customized flow work end to end.

Track runtime proof with this artifact:

```yaml
baseline_gate:
  quickstart_repo_cloned: false # official sample cloned at a known path
  official_start_command_run: false # documented start command run verbatim
  agent_join_verified: false # agent reached RUNNING in the RTC channel
  rtc_client_connected: false # client joined the same channel and heard agent audio
```

If `quickstart_repo_cloned` is false, the following are blocked:

- `/join` payload generation from memory
- SDK implementation files in the user's repo
- custom file structures or new app scaffolds
- existing-app edits that are not backed by a copy map sourced from the official quickstart

After the official quickstart source is cloned and inspected, the agent may:

- update the cloned quickstart's agent prompt, greeting, persona, scenario details, or documented join/config fields to match the user's requested agent
- produce a copy map for an existing app from the inspected quickstart files
- adapt only the mapped quickstart-derived pieces into the user's app after copy-map approval

Do not change the sample's architecture, token flow, env names, lifecycle, or documented commands unless the official quickstart source itself requires a minimal upstream-shaped fix.

The baseline gate is complete only when the sample-ready gate succeeds: app opens, conversation starts, the agent joins the RTC channel, and the user can speak and hear TTS back.

## Response Status Rules

Before every actionable reply, reconcile the current `baseline_gate` state with the action you are about to take. This internal check is mandatory but is not user-visible by default.

Show status only in these cases:

| Trigger                               | Format      | Fields                                                          |
| ------------------------------------- | ----------- | --------------------------------------------------------------- |
| First ConvoAI reply                   | Full block  | `official_template`, `next_command`, `baseline_gate`, `blocked` |
| Gate flips from false to true         | One line    | `baseline_gate: 2/4 -> 3/4; next: <command>`                    |
| Blocked action                        | Short block | False gate field plus the command that unblocks it              |
| User asks "where are we?" or "status" | Full block  | Same as first-reply format                                      |
| Routine command, Q&A, explanation     | No footer   | None                                                            |

Use checkmark glyphs in user-visible baseline status:

```text
baseline_gate:
  ✓ quickstart_repo_cloned
  ✗ official_start_command_run
  ✗ agent_join_verified
  ✗ rtc_client_connected
```

Tone rules:

- Do not use the phrase "policy violation" in user-visible replies. Say what is blocked and what command unblocks it.
- Do not use "Track A" or "Track B" in user-visible replies. Say "baseline" and "integration."
- Keep the footer silent on routine progress; show it only when it changes something for the user.

## Recovery Rule

If the agent has already deviated, stop the custom path and pivot back to the official sample.

Deviation triggers:

- generated a `/join` payload from memory before inspecting quickstart source
- created SDK implementation files in the user's repo before inspecting quickstart source and producing a copy map
- created a new `package.json`, `routes/`, or scaffold for a ConvoAI app instead of adapting the official quickstart source
- changed documented sample command semantics, such as replacing the README start command with a custom wrapper
- attempted to fix `[ERR_PNPM_IGNORED_BUILDS]` or configure pnpm build approvals instead of proceeding to the documented start command
- wrote `.env` / `.env.local` with literal `$AGORA_APP_ID` or `$AGORA_APP_CERTIFICATE` strings instead of expanded credential values

Recovery response:

1. Acknowledge the deviation in plain language.
2. Show the current `baseline_gate` with incomplete fields.
3. Give the exact next official sample command.
4. Do not continue custom edits until source alignment is restored. Runtime proof is still required before claiming the flow works.

## Sequence

Follow this exact user-visible order:

1. Product intro in plain language
2. Intake — confirm preferred stack (`python` or `node/ts`) and confirm whether the agent is allowed to install/upgrade missing tools
3. Environment check — verify runtime dependencies are installed
4. Project-readiness checkpoint — use the CLI directly to verify and fix
5. Vendor-path confirmation — **skip if the user has not mentioned BYOK, providers, or Studio Agent ID; defaults apply automatically**
6. Vendor selection, only if the user asks for the current provider list or chooses a non-default path
7. Studio Agent ID confirmation, only if the user wants to reuse an agent configured in Agora Studio
8. Structured quickstart spec

## Interaction Rules

- One decision group per turn. Do not ask credentials and vendor path in the same reply.
- Skip anything the user already answered.
- Resolve required values in this order: session memory, read-only workspace detection, then one focused question. Explicit user statements win over detected values, and the latest user statement wins on conflict. Do not re-ask for values the user already provided.
- **Auto-skip `vendor_defaults`**: if the user has not mentioned BYOK, vendor API keys, a specific provider, or a Studio Agent ID, skip the vendor gate entirely and use the defaults. Do not ask about providers when the user just wants the fastest path.
- Infer obvious context from the user's stack or repository description.
- Mirror the user's language.
- While quickstart source is unresolved, do **not** generate `/join` payloads, SDK code, custom file structures, clone commands, or repo adaptation plans from memory.
- While quickstart is unresolved, read only this file and [README.md](README.md).
- If the user asks to use the CLI to speed up onboarding, keep the request inside this quickstart flow. The CLI is already the default readiness path, so continue normally.
- Unless the user explicitly asks for BYOK (bring your own key) or a different provider stack, anchor on the defaults first — no vendor API keys needed.
- For non-default provider selection, fetch the official current provider docs before confirming support or generating config details.
- If the user already has an **Agora Studio Agent ID** from `https://console.agora.io/studio/agents`, treat that as a separate quickstart branch. Do not re-ask STT/LLM/TTS provider choices unless the user explicitly wants to replace the Studio-managed config.
- If stack preference is unknown, ask one short intake question before selecting the baseline sample.
- If stack preference is still unspecified after intake, default to `agent-quickstart-python`.
- When starting from scratch, customize the cloned quickstart's agent prompt, greeting, persona, scenario details, or documented join/config fields to match the user's requested agent. Keep architecture, env names, token flow, lifecycle, and documented commands intact.

## Industry-Standard Execution Policy

Apply this policy for quickstart setup actions:

1. Detect first: run read-only checks and report what is installed.
2. Recommend second: propose the best baseline path from user preference + detected tools.
3. Confirm scope before mutate: ask once for bounded quickstart setup approval.
4. Execute exactly: once confirmed, run the documented command without substituting variants.
5. Report clearly: summarize what changed and what remains blocked.

Guardrails:

- Never silently install or upgrade system tools.
- Never assume language/runtime preference when the user has already stated one.
- Prefer least-surprise behavior: explicit approval for machine changes, deterministic commands, and transparent outcomes.

Approved quickstart setup scope covers:

- installing or upgrading missing non-system setup tools needed for the selected baseline (`bun`, `pnpm`/`npm`, `agora`)
- running `agora login`
- selecting an existing suitable project
- enabling required Agora features on the selected project
- writing or updating the selected sample's expected env file
- updating the selected sample's documented agent prompt, greeting, persona, scenario details, or join/config fields requested by the user
- installing the selected sample's dependencies
- starting the selected sample

Ask again before:

- creating a new Agora project
- deleting files, uninstalling packages, or removing projects
- overwriting env files with `--overwrite`
- printing or exposing secrets in chat
- installing or upgrading system runtimes such as Node.js or Python
- changing files or settings outside the selected quickstart repo and selected Agora project

## Known Non-Blocking Warnings

Exit code alone does not determine whether to proceed. Read command output and match it against known non-blocking patterns before treating a non-zero exit as failure requiring remediation.

### Node/TS baseline (`agent-quickstart-nextjs`)

After `pnpm install`:

- **`[ERR_PNPM_IGNORED_BUILDS]`** is not a blocking error. The sample's dev script uses `next dev --webpack` explicitly — esbuild, sharp, and unrs-resolver build scripts are not required for the dev path. If packages were added and the only non-zero exit is this warning, proceed directly to `pnpm dev`.
- If `pnpm dev` re-runs an install check and prints the same ignored-builds warning, treat that as non-blocking too — run the README `pnpm dev` again or start the documented dev script from the quickstart directory. Do not stop before a dev server is listening.
- Do not run `pnpm approve-builds`, `pnpm config set onlyBuiltDependencies`, `pnpm dev --ignore-scripts`, edit `package.json` with pnpm config fields, create `pnpm.yaml`, or change global pnpm build-approval settings to resolve this warning during first-success setup.

## Command Integrity Under Environment Restrictions

For the first-success gate, treat the sample README commands as exact.

If a documented command fails because of sandbox, permission, port-binding, filesystem, or network restrictions:

1. Do **not** replace the command with an equivalent variant.
2. Do **not** add flags, env vars, host overrides, alternate entrypoints, or custom wrappers.
3. Re-run the exact documented command with required escalation or approval if available.
4. If escalation is unavailable or denied, stop and report that the baseline is blocked by the execution environment, not by the sample itself.
5. Do **not** continue to customization until the sample has been validated with the documented command.

Forbidden substitutions include:

- `pnpm dev` → `pnpm exec next dev ...`
- `npm run dev` → `next dev ...`
- README clone/start commands → custom shell variants that change the command semantics

## Failure Attribution

If the documented sample command fails before app code runs and the error indicates a local execution restriction, classify it as an environment constraint.

Typical signals include:

- `EPERM`
- `EACCES`
- blocked `listen` / `bind`
- blocked `chmod` / filesystem permission errors
- sandbox-denied network or local resource access

Do **not** reinterpret these failures as sample misconfiguration and do **not** change the command to work around them.

### Install warnings (Node/TS baseline)

When `pnpm install` exits non-zero:

- If the output is caused solely by `[ERR_PNPM_IGNORED_BUILDS]`, classify it as a **warning**, not a failure. Continue to the next documented command (`pnpm dev`). Do not attempt to resolve it before starting the app.
- Do not treat this warning as sample misconfiguration or as proof that dependencies failed to install.

## First-Success Readiness Layers

Use three readiness layers during quickstart:

- **Control-plane ready** — login works, the project resolves, App ID exists, App Certificate can be exported through the verified CLI surface, required features are enabled, and `agora project doctor` is not blocking.
- **Runtime ready** — services are actually usable. In practice, RTM enablement may lag behind control-plane state; after enablement, allow bounded wait/retry for up to about 5 minutes before deciding the project still needs intervention.
- **Sample ready** — the official sample installs, env is populated, the app starts, the browser can open, the user can press `Try it now`, the agent joins the RTC channel, and the frontend does not crash.

`agora project doctor` only proves **control-plane ready**. It does not prove runtime or sample readiness.

## CLI-Driven Readiness Check

The project readiness step requires the agent to directly execute Agora CLI commands to verify and fix prerequisites. Do not ask the user to run CLI commands themselves and do not offer manual alternatives. The agent checks directly; mutating actions may proceed inside the approved quickstart setup scope.

The CLI covers:

- login / auth status
- current project selection
- project env export
- official quickstart cloning and repo-local binding
- template-aware quickstart env writing
- feature enablement
- App ID presence, App Certificate presence, and other basic project checks
- `agora project doctor` readiness checks

Use the CLI in this order:

1. For a new official quickstart, prefer `agora init` when it can clone, bind the project, and write env safely.
2. For an existing official quickstart, use `agora quickstart env write` to seed env files.
3. Use `agora project env --with-secrets --json` only for manual mapping flows that need raw credential values.
4. Use `project show --json` only for project metadata inspection.

Do **not** treat a healthy doctor result as a proven ConvoAI baseline.

For command details, route to the CLI references:

- [../cli/README.md](../cli/README.md)
- [../cli/quickstarts.md](../cli/quickstarts.md)
- [../cli/env.md](../cli/env.md)
- [../cli/projects.md](../cli/projects.md)
- [../cli/doctor.md](../cli/doctor.md)

After the CLI readiness step is resolved, return to this quickstart and continue from the same readiness checkpoint.

## First-Success Baseline Selection

Select the baseline sample from user preference first, then installed tools:

- If user explicitly wants Python (or has no preference): use `agent-quickstart-python`.
- If user explicitly wants Node/TypeScript and has Node 22+ plus pnpm 8+ (preferred) or npm fallback: use `agent-quickstart-nextjs`.
- If user asks for Go as the final backend, still complete one official quickstart baseline first, then route to [go-sdk.md](go-sdk.md) for backend implementation.

If no stack preference is provided, default to:

- **Repo:** <https://github.com/AgoraIO-Conversational-AI/agent-quickstart-python> _(Python server + React frontend)_

1. Runtime prerequisites
   1.1 Python baseline: Bun (package manager & script runner) + Python 3.8+
   1.2 Node/TS baseline: Node.js 22+ + pnpm 8+ preferred; fallback to npm when pnpm is unavailable and the sample supports npm
2. CLI preflight
   2.1 Complete [CLI readiness](../cli/README.md#cli-readiness-agents) — block if below `0.1.7` or PATH resolves an old binary
   2.2 Log in: `agora login`
   2.3 Verify CLI version with `agora version` (minimum `0.2.1`, floor `0.1.7`)
   2.4 Prefer `agora init <name> --template <template> --json` where `<template>` matches the selected baseline (`python` or `nextjs`)
   2.5 For an existing official quickstart, use `agora quickstart env write <repo> --project <project>` — not `project env write`
   2.6 If decomposing the flow, prefer the current selected project only if it is directly usable for first-success
   2.7 Otherwise select another directly usable project, or ask before creating a new dedicated token-ready project
   2.8 Ensure `rtc`, `rtm`, and `convoai` are enabled for the first-success path
   2.9 Use `agora project env --with-secrets --json` only when direct raw credential values are explicitly needed outside `init` / `quickstart env write`
   2.10 Check `agora project doctor`
   2.11 If RTM was just enabled, allow bounded wait/retry before concluding runtime failure
3. Official sample baseline
   3.1 Clone the selected official quickstart (`agent-quickstart-python`, `agent-quickstart-nextjs`, or `agent-quickstart-go`) directly or through `agora init`
   3.2 Install and start with the selected sample's documented commands:
   - Python baseline: `bun install` then `bun run dev`
   - Node/TS baseline: run `pnpm install` then `pnpm dev` when pnpm is available; otherwise fall back to `npm install` then `npm run dev` when the sample supports npm
   3.3 Ensure the expected env file is present:
   - Python baseline: `server/.env` with `APP_ID` + `APP_CERTIFICATE`
   - Node/TS baseline: `.env.local` with `NEXT_PUBLIC_AGORA_APP_ID` + `NEXT_AGORA_APP_CERTIFICATE`
   - Go baseline: `server-go/.env` with `APP_ID` + `APP_CERTIFICATE`
     (`agora quickstart env write` is the default seeding path)
     3.4 Do not rename the sample's env variables during first success
4. Success gate
   4.1 App loads at the sample's documented local URL
   4.2 User can start a conversation from the UI
   4.3 Agent joins the RTC channel
   4.4 User can speak to the agent and hear TTS back
   4.5 Only after this counts as a working baseline

## First-Success Vendor Defaults

The official `agent-quickstart-nextjs` sample works out of the box with just Agora credentials.
Vendor API calls (STT, LLM, TTS) go through Agora by default — no vendor API keys needed.

Default pipeline:

- **STT:** Deepgram nova-3
- **LLM:** OpenAI gpt-4o-mini
- **TTS:** MiniMax speech_2_6_turbo

BYOK (Bring Your Own Key) is supported but optional. The sample includes commented-out
BYOK blocks for Deepgram, OpenAI, and ElevenLabs. Users who want to use their own vendor
API keys can uncomment those blocks and provide them.

BYOK provider families visible in the current sample and SDK docs:

- **STT:** Deepgram (BYOK)
- **LLM:** OpenAI (BYOK)
- **TTS:** ElevenLabs (BYOK), Microsoft
- **MLLM:** OpenAI Realtime, Google Gemini Live

Use this rule during quickstart:

- For the first end-to-end success path, prefer the **default pipeline** (no vendor keys).
- Only switch to BYOK during quickstart if the user explicitly asks for it or names a specific vendor key they want to use.
- Only switch away from the default cascading pipeline if the user explicitly asks for MLLM.
- For the current provider matrix or vendor-specific configs, fetch the official live docs before claiming support or listing parameters.

## Env Name Policy

### Default sample path (`agent-quickstart-python`)

Keep the official sample's env names as the source of truth.

Default (no vendor keys needed):

```bash
APP_ID=
APP_CERTIFICATE=
PORT=8000
```

Do **not** prompt for vendor API keys unless the user explicitly asks for BYOK.
Do **not** rename these env vars to a different custom scheme during quickstart.

### Custom-code path

If the user is no longer sample-aligned and needs provider-specific config layout, fetch the current official ConvoAI provider docs and use those as the source of truth.

## Agent Prompt and Join Details

When starting from scratch in an official quickstart, update the user-controlled agent details the user actually cares about before first run when they have provided them.

Allowed quickstart edits:

- agent/system prompt or instructions
- greeting or first message
- persona, role, language, tone, and scenario details
- documented agent name, channel naming, or join/config fields already present in the sample

Do not rewrite the join lifecycle, token generation, env loading, or provider schema by hand. If the requested change touches vendor-specific model/config fields not already clear in the sample, fetch the current official docs before editing those fields.

## Baseline Path

Default baseline is `agent-quickstart-python` unless the user explicitly chooses Node/TypeScript and the required Node plus package-manager runtime is available.

After first success, the user can explore other demos:

| Demo                      | Description                                     | Reference                            |
| ------------------------- | ----------------------------------------------- | ------------------------------------ |
| `agent-quickstart-nextjs` | Full-stack Next.js (single app with API routes) | [See below](#other-demo-references)  |
| `agent-samples`           | Decomposed backend + multiple client apps       | [agent-samples.md](agent-samples.md) |

## State Machine

The quickstart is a blocking state machine for source alignment and runtime proof. While a state is unresolved, the next action must stay inside the current gate. For integration mode, read-only workspace detection and quickstart source inspection are allowed when directed by [integration-from-quickstart.md](integration-from-quickstart.md).

| State               | Allowed                                                                                                                                                                                                                                                                                                | Forbidden                                           | Next prompt                | Advance when                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------------------- |
| `intro`             | Give a short plain-language intro to what ConvoAI is                                                                                                                                                                                                                                                   | Code, repo plans, framework recommendations         | Product intro text         | Intro delivered                                                                     |
| `intake`            | Confirm preferred stack (`python` or `node/ts`) and get scoped quickstart setup approval; in integration mode, use read-only detection before asking                                                                                                                                                   | Code generation, custom scaffolding, implementation | Intake prompt              | Stack preference + setup scope are resolved or inferred                             |
| `environment_check` | Check Node.js, Bun, Python, Agora CLI versions. Recommend and run installs/upgrades only after user confirmation.                                                                                                                                                                                      | Code, repo inspection, implementation               | Environment check commands | Required dependencies for selected baseline are installed and meet minimum versions |
| `project_readiness` | Execute CLI commands directly to verify auth, project, App ID, App Certificate, feature activation, and fix missing prerequisites inside the approved setup scope. Extract credentials from CLI env output.                                                                                            | Code, repo inspection, implementation               | Readiness prompt           | Control-plane readiness confirmed and credentials captured                          |
| `vendor_defaults`   | Ask whether to use the defaults (no vendor keys), BYOK, show the current official provider list, choose a non-default cascading / MLLM path, or reuse a Studio Agent ID. **Skip this gate entirely if the user has not mentioned BYOK, providers, or Studio Agent ID — defaults apply automatically.** | Code, implementation                                | Vendor-defaults prompt     | User picks or gate is auto-skipped                                                  |
| `vendor_selection`  | Collect only provider-mode and provider choices after checking the official current provider docs                                                                                                                                                                                                      | Code, implementation, secret collection             | Custom-provider prompt     | Provider mode and provider names are resolved                                       |
| `studio_agent_id`   | Collect the Agora Studio Agent ID and confirm the user wants Studio to remain the source of truth for agent config                                                                                                                                                                                     | Code, re-asking provider setup from scratch         | Studio-Agent-ID prompt     | The Studio Agent ID path is resolved                                                |
| `complete`          | Emit structured spec and continue to execution                                                                                                                                                                                                                                                         | Re-open resolved gates                              | None                       | Spec emitted                                                                        |

### Pre-Action Self-Check

Before every tool call or user-visible reply:

1. What is the current state?
2. Is the intended action allowed in that state?
3. If not, send the state prompt instead.

### Failure Branches

- If the user says they cloned a repo but never got an agent running, stay in quickstart.
- If the user asks for code before quickstart resolves, answer with the next gate instead of generating code.
- If a reply only partially resolves the current gate, ask a narrow follow-up for the missing field only.
- If the user asks for the fastest onboarding path or mentions setup during the readiness gate, proceed directly with the CLI verification sequence and then return to the quickstart once readiness is confirmed.
- If the user asks for the full fastest onboarding flow and has not stated a stack preference, use `agent-quickstart-python`.
- If the user names a provider that is not in the current official provider docs, say this clearly: it is **not currently documented as supported in the official Agora ConvoAI provider docs**, so do not proceed as if it is supported. Offer the documented default combo or a live-doc verification path.
- If the user asks to see the provider list, fetch the current official provider docs and stay in the vendor gate until they accept the default combo or choose a documented alternative.
- If the user says they already have an Agora Studio Agent ID, switch to the `studio_agent_id` state and stop re-asking provider-vendor questions unless they explicitly say they want to replace the Studio-managed config.

## Prompt Templates

### Product Intro

Keep it short. Explain that ConvoAI is a server-managed voice agent that joins an RTC channel, speaks through TTS, and usually pairs an RTC client with a backend that starts the agent.

Use a natural transition into quickstart. Preferred tone:

- Avoid saying "run the baseline flow" or "anchor on a proven baseline" to the user.
- Prefer "let's first use the official sample to get the whole link working once" language.

Suggested transition line:

```text
Before we jump into custom code, let's first use the official sample to get the whole flow working once. Once the agent can join the channel and finish one real conversation, we can turn that working version into your demo.
```

### Intake

Ask this right after intro when stack preference or install policy is still unknown:

```text
Before we run setup, which baseline do you want first: Python or Node/TypeScript?
I can check your environment and handle normal quickstart setup in one approved scope. I will ask again before creating a new Agora project, overwriting files, exposing secrets, installing Node/Python, or changing anything outside this quickstart.
```

### Environment Check

Before starting the CLI readiness flow, complete [CLI readiness](../cli/README.md#cli-readiness-agents) and verify runtime dependencies. Run read-only checks first, then use the approved setup scope for non-system quickstart tools.

| Dependency                     | Check command                                    | Minimum version                         | Install if missing                                                               |
| ------------------------------ | ------------------------------------------------ | --------------------------------------- | -------------------------------------------------------------------------------- |
| Node.js (Node/TS baseline)     | `node --version`                                 | 22+                                     | Direct the user to https://nodejs.org or use `nvm install 22`                    |
| pnpm or npm (Node/TS baseline) | `pnpm --version`, then `npm --version` if needed | pnpm 8+ preferred; npm fallback allowed | Use npm if pnpm is unavailable and the sample supports it                        |
| Bun (Python baseline)          | `bun --version`                                  | 1.0+                                    | `npm install -g bun`                                                             |
| Python (Python baseline)       | `python3 --version`                              | 3.8+                                    | Direct the user to https://python.org                                            |
| Agora CLI (all baselines)      | `agora version`                                  | Verified `0.2.1`; block if below `0.1.7` | Follow [CLI readiness](../cli/README.md#cli-readiness-agents): curl install first, npm alternate |

Execution rules:

- Check only the selected baseline's dependencies plus Agora CLI.
- Install or update non-system tools only inside the approved setup scope; otherwise stop with clear next steps.
- For Node.js and Python, if they are not installed, tell the user what to install and wait — do not attempt to install system-level runtimes.
- For Python baseline, install Bun only when covered by the approved setup scope.
- For Node/TS baseline, use pnpm if available; otherwise use npm if the sample supports it. Do not install pnpm just because it is preferred.
- For Agora CLI below minimum, follow [CLI readiness](../cli/README.md#cli-readiness-agents) — curl installer first, `npm install -g agoraio-cli` as alternate, then re-verify `agora version` and `which -a agora`. Do not use `--add-to-path` or invented `--force` flags.
- If Agora CLI is installed but outdated, use `agora upgrade --check --json` for channel-specific guidance or re-run the curl installer.
- Only proceed to project readiness after all required checks for the selected baseline pass.

### Project Readiness

Check readiness directly with the Agora CLI. Do not ask the user to self-report it. Mutating fixes may run inside the approved setup scope; ask again for out-of-scope actions.

Tell the user what you are about to check, then execute the commands yourself:

```text
I will check Agora login, project, App ID, App Certificate, and ConvoAI activation with the CLI. Read-only checks come first; setup fixes stay inside the approved scope.
```

#### Agent execution sequence

Run these commands in order. Use `--json` where available so you can parse the output programmatically.

1. **Auth check** — `agora auth status --json`
   - If not logged in → run `agora login` and wait for the user to complete the browser OAuth flow.

2. **Current project suitability** — check the currently selected project first.
   - Inspect the selected project with `agora project show --json`.
   - Treat it as directly usable only if the project resolves, App ID exists, App Certificate is exportable, and the required first-success features are present.
   - If the current project is directly usable → keep it.
   - If the current project is not directly usable → continue to project discovery.

3. **Project discovery and selection**
   - If the user explicitly named a project, inspect that exact project first and try to repair it with documented CLI commands.
   - If the user did **not** name a project and the current selected project is not directly usable, inspect existing projects and look for a directly usable candidate.
   - If a directly usable candidate is found, select it and explicitly tell the user which project was chosen before continuing.
   - If no directly usable candidate exists, ask before creating a new dedicated first-success project with the required features already enabled.

4. **Credential export / env write** — use `agora quickstart env write` as the default for official quickstarts.
   - If this fully seeds the sample env file, do not run `agora project env --with-secrets`.
   - Use `agora project env --with-secrets --json` only when direct raw values are explicitly needed for manual mapping.
   - If `--with-secrets` is used, do not echo secret values in chat output.
   - If `--with-secrets` fails because the project is still not token-ready, treat that as a project-readiness failure; repair within the approved setup scope or ask before replacing the project.

5. **Doctor** — `agora project doctor --json`
   - If `healthy` or `warning` → control-plane readiness is confirmed, not runtime/sample readiness.
   - If `not_ready` → read the reported issues and remediate within the approved setup scope:
     - ConvoAI not enabled → run `agora project feature enable convoai`, then re-run doctor.
     - RTM or related service just enabled → allow bounded wait/retry for up to about 5 minutes before concluding the project still needs intervention.
     - Other issues → run the matching in-scope recovery command (see [doctor.md](../cli/doctor.md)), then re-run doctor. Ask before out-of-scope recovery.
   - Repeat until doctor passes at the control-plane layer.

6. **Auto-populate env** — once control-plane readiness passes, seed the official quickstart env with `agora quickstart env write` when possible.
   - Python quickstart target: `server/.env` with `APP_ID` and `APP_CERTIFICATE`.
   - Node/TS quickstart target: `.env.local` with `NEXT_PUBLIC_AGORA_APP_ID` and `NEXT_AGORA_APP_CERTIFICATE`.
   - Go quickstart target: `server-go/.env` with `APP_ID` and `APP_CERTIFICATE`.
     No manual copy-paste needed when template-aware write succeeds.
   - When `AGORA_APP_ID` and `AGORA_APP_CERTIFICATE` are already exported in the shell (common in CI and local setups), the env file must contain **resolved literal values**, not unexpanded placeholders. Wrong: `NEXT_PUBLIC_AGORA_APP_ID=$AGORA_APP_ID` written as text. Right: expand variables when writing (e.g. `agora quickstart env write`, or a heredoc/`printf` that substitutes current env values). Verify the file has non-empty values before starting the dev server.

7. **Sample-ready gate**
   - Install dependencies and start the official sample using the documented commands.
   - If `pnpm install` exits non-zero with only `[ERR_PNPM_IGNORED_BUILDS]`, treat install as complete and continue to `pnpm dev` — see [Known Non-Blocking Warnings](#known-non-blocking-warnings).
   - The quickstart is only fully ready when the app opens, the user can press `Try it now`, the agent joins, and the frontend stays up.
   - If a failure is localized to the official sample itself rather than the environment or project readiness, a minimal upstream-shaped workaround is allowed. Do not replace the sample with a self-built implementation.

For CLI command details, route to:

- [../cli/README.md](../cli/README.md)
- [../cli/quickstarts.md](../cli/quickstarts.md)
- [../cli/env.md](../cli/env.md)
- [../cli/projects.md](../cli/projects.md)
- [../cli/doctor.md](../cli/doctor.md)

### Vendor Defaults

Use this only if the user has mentioned BYOK, vendor API keys, a specific provider, or a Studio Agent ID. If none of these were mentioned, skip this prompt entirely and use the defaults.

```text
The official quickstart works out of the box with just Agora credentials — no vendor API keys needed.

Default pipeline:
- STT: Deepgram nova-3
- LLM: OpenAI gpt-4o-mini
- TTS: MiniMax speech_2_6_turbo

A. Use the defaults (no vendor keys needed — fastest path)
B. I want to use my own vendor API keys (BYOK)
C. Show me the current official provider list first
D. I want to choose a non-default cascading or MLLM path
E. I already have an Agora Studio Agent ID and want to reuse that Studio-managed agent
```

### Custom Provider Prompt

Use only after the user picks `C` or directly asks for non-default providers.

```text
First check the current official ConvoAI provider docs, then choose from the documented provider modes:
- Cascading path: STT + LLM + TTS
- MLLM path: OpenAI Realtime or Google Gemini Live

Then choose the documented providers for that mode using the current official docs as the source of truth.

Reply in one line, for example:
- `TTS: Microsoft`
- `MLLM: OpenAI Realtime`
- `STT: Deepgram, LLM: OpenAI, TTS: Microsoft`
```

### Studio Agent ID Prompt

Use only when the user picks `D` or directly says they already have an Agora Studio Agent ID.

```text
If you already configured the agent in Agora Studio, we can treat Studio as the source of truth for the agent configuration instead of rebuilding the provider stack here.

Open `https://console.agora.io/studio/agents`, find the agent you want to reuse, and copy its **Agent ID**.

Important:
- This **Studio Agent ID** is different from the runtime `agent_id` returned by `/join`.
- The Studio Agent ID identifies the Studio-managed agent configuration and maps to the request field `pipeline_id`.
- The runtime `agent_id` identifies a live started session.

Reply with one of these:
A. I have the Studio Agent ID — here it is: `<agent-id>`
B. I need to look it up in Studio first
C. Go back — I want to use the default/provider path instead
```

### Unsupported Provider Prompt

Use this when the user names a provider that is not in the current official provider docs.

```text
That provider is not in the current official Agora ConvoAI provider docs, so I should not proceed as if it is supported.

You can choose one of these paths:
A. Use the documented default combo to get the first demo working
B. Show the current official provider list first
C. Re-check the latest official docs to verify whether that provider is supported now
```

## Output: Structured Quickstart Spec

After all gates are resolved, normalize the result into a short spec and continue within the approved setup scope. Ask before any unapproved mutating action.

```yaml
use_case: [text]
mode: quickstart
proven_working_baseline: yes
baseline_gate:
  quickstart_repo_cloned: true
  official_start_command_run: true
  agent_join_verified: true
  rtc_client_connected: true
project_readiness:
  app_id: [ready | missing | unknown]
  app_certificate: [ready | missing | unknown]
  convoai_activation: [ready | missing | unknown]
key_mode: [default | byok | unknown]
providers:
  pipeline: [cascading | mllm | unknown]
  stt: [deepgram | user-specified-supported | unknown]
  llm: [openai | user-specified-supported | unknown]
  tts: [minimax | elevenlabs | microsoft | user-specified-supported | unknown]
  mode: [default | byok-default | user-specified-cascading | mllm | unknown]
studio_agent:
  use_existing_agent_id: [yes | no | unknown]
  agent_id: [text | missing | unknown]
```

Notes:

- `stt` is the SDK-facing name in this quickstart spec. Platform docs may call the same stage `ASR`.
- `studio_agent.agent_id` means the **Agora Studio Agent ID** from `https://console.agora.io/studio/agents`, not the runtime `agent_id` returned by `/join`.
- When this Studio path is used, that Studio Agent ID maps to the request field `pipeline_id`.

## After Collection

Execute the selected quickstart baseline (clone the chosen official sample, configure, run, verify first success).

After first success, route by user's next request:

- existing Agora Studio Agent ID → use [conversational-ai-studio.md](conversational-ai-studio.md)
- provider selection or parameter confirmation → fetch the current official ConvoAI provider docs
- custom LLM backend → [server-custom-llm.md](server-custom-llm.md)
- direct REST API (non-SDK languages) → [auth-flow.md](auth-flow.md)
- other demos → see "After the Baseline Works" section below

## Other Demo References

These are available after the first success baseline is proven. Do not use these as the default quickstart path.

### Full-Stack Next.js (`agent-quickstart-nextjs`)

**Repo:** <https://github.com/AgoraIO-Conversational-AI/agent-quickstart-nextjs>

Single Next.js app with built-in API routes for token generation and agent lifecycle. Includes React UI with live transcription. Requires Node.js 22+ and a supported package manager; prefer pnpm 8+ and fall back to npm when pnpm is unavailable and the sample supports npm. See the repo README for setup.

### Decomposed Samples (`agent-samples`)

Multiple backend + client combinations. See [agent-samples.md](agent-samples.md).

## After the Baseline Works

Once the first end-to-end ConvoAI session works, route by task:

| Next step                                              | Reference                                                                   |
| ------------------------------------------------------ | --------------------------------------------------------------------------- |
| Customize LLM, TTS, ASR vendor or model                | Fetch `https://docs-md.agora.io/en/conversational-ai/develop/custom-llm.md` |
| Add transcript rendering or agent state to a custom UI | [agent-toolkit.md](agent-toolkit.md)                                        |
| Use React hooks (`useTranscript`, `useAgentState`)     | [agent-client-toolkit-react.md](agent-client-toolkit-react.md)              |
| Swap in pre-built React UI components                  | [agent-ui-kit.md](agent-ui-kit.md)                                          |
| Add a custom LLM backend (RAG, tool calling)           | [server-custom-llm.md](server-custom-llm.md)                                |
| Production token generation                            | [../server/tokens.md](../server/tokens.md)                                  |
| Full REST API reference                                | [README.md](README.md#rest-api-endpoints)                                   |
