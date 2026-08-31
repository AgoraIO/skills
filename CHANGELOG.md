# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Fixed

- Claude plugin packaging now uses the root `.mcp.json` default location so the bundled `agora-docs-mcp` server is discovered at runtime.
- Cursor and Claude MCP wrappers now use the same `agora-docs-mcp` key and HTTP transport declaration.

### Changed

- Claude plugin, Agora skill, and Cursor wrapper versions aligned at `1.8.2`.
- Claude plugin metadata now includes the existing DevRel contact and project homepage.
- Volatile provider model IDs and framework runtime matrices now route to the cloned official sample or current provider docs instead of freezing fast-changing values inline.
- Testing guidance is now an internal routed reference (`README.md`) rather than a nested `SKILL.md` that different hosts could discover inconsistently.
- CI now enforces Claude schemas, clean-install skill/MCP discovery, Markdown lint, and the 500-line Layer 4 topic ceiling.
- The public skill now declares its MIT license explicitly. A separate CI step installs the official Agent Skills reference validator at pinned commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379` and validates `skills/agora`.
- RTC Web client/join alternatives again retain their semantic comments, and the detailed screen-sharing pattern now lives in its own routed topic instead of leaving `web.md` at the size ceiling.
- Claude Code is pinned in CI, and clean-install packaging assertions now use `plugin list --json` instead of human-readable spacing.
- Agora CLI references now use the canonical `dl.agora.io` installer, the verified minimum is `0.2.1`, and region/config guidance is version-agnostic.
- ConvoAI quickstart readiness now verifies the sample page and uses the documented npm fallback when pnpm lifecycle scripts are blocked.

## [1.8.1] - 2026-06-26

### Fixed

- `.claude-plugin/mcp-config.json`: wrap server definition with `mcpServers` key and rename the server `agora-docs` → `agora-docs-mcp` so the Claude Code plugin loader registers it under the name referenced in `skills/agora/SKILL.md` and `skills/agora/references/mcp-tools.md`.
- `.claude-plugin/marketplace.json`: align version with `plugin.json` and `skills/agora/SKILL.md` (1.7.0 → 1.8.1).
- `README.md`: fix malformed "Powered by Agora" link and point Contributing at the in-repo `CONTRIBUTING.md` instead of a feature branch.

### Changed

- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `skills/agora/SKILL.md`: bump version to 1.8.1 so anyone who installed 1.8.0 picks up the working `mcp-config.json`.
- `skills/agora/references/mcp-tools.md`: update install command and remove the obsolete "configured here as `agora-docs`" caveat now that the server name matches.

## [1.8.0] - 2026-05-27

### Added

- `skills/agora/references/conversational-ai/server-sdk-rename.md`: opt-in migration reference for projects using outdated ConvoAI server SDK package names.

### Changed

- `skills/agora/SKILL.md` and `skills/agora/references/conversational-ai/README.md`: route existing projects with outdated server SDK package names through the migration reference before changing manifests or imports.
- `skills/agora/references/conversational-ai/server-sdks.md`, `python-sdk.md`, `go-sdk.md`, `auth-flow.md`, and `architecture.md`: updated default ConvoAI server SDK references to `agora-agents` and `github.com/AgoraIO/agora-agents-go`.

## [1.7.0] - 2026-05-22

### Added

- `skills/agora/references/conversational-ai/architecture.md` — ConvoAI call sequence, server `/join`, client RTC/RTM join order, and agent lifecycle overview
- `skills/agora/references/conversational-ai/integration-from-quickstart.md` — existing-app integration workflow from official quickstart source with copy-map gating
- `tests/eval-cases.md`: expanded ConvoAI architecture, integration, baseline-gate footer, recovery, and copy-map regression cases (I-28 through I-40)
- `tests/eval-cases.md`: I-41 regression case — `[ERR_PNPM_IGNORED_BUILDS]` after Node/TS `pnpm install` is non-blocking and must not trigger pnpm build-approval remediation

### Changed

- `skills/agora/SKILL.md`, `skills/agora/references/conversational-ai/README.md`, `skills/agora/references/conversational-ai/quickstarts.md`: hardened ConvoAI quickstart enforcement with `baseline_gate` runtime proof, recovery rules, silent-by-default status footers, source-scope stop, and integration routing
- `skills/agora/references/conversational-ai/quickstarts.md`: restored stack intake (`python` vs `node/ts`), consent-first setup scope, and baseline selection for `agent-quickstart-python` / `agent-quickstart-nextjs`
- `skills/agora/references/conversational-ai/quickstarts.md` (v1.5.0): hardened Node/TS first-success install handling — `[ERR_PNPM_IGNORED_BUILDS]` is a known non-blocking warning; read output before treating non-zero exit as failure, proceed to `pnpm dev`, and do not run `pnpm approve-builds` or edit pnpm config during setup; added matching Failure Attribution and Recovery Rule deviation triggers
- `skills/agora/references/rtc/web.md`, `skills/agora/references/server/tokens.md`, `skills/agora/references/rtm/web.md`, `skills/agora/references/integration-patterns.md`: clarified integer UID limits and account-name / RTM login-identity alignment rules
- `skills/agora/references/cli/README.md` and related CLI references: raised verified CLI baseline to `0.2.1` (floor `0.1.7`) and hardened agent readiness / PATH recovery guidance
- `skills/agora/references/conversational-ai/agent-client-toolkit-react.md`: include `agora-rtm` in React agent toolkit install instructions

## [1.6.1] - 2026-05-12

### Added

- `agora/.cursor-plugin/` — lightweight Cursor plugin wrapper that references the canonical Agora skills

### Changed

- `skills/agora/SKILL.md`: refined capability-first trigger description and routing workflow
- `skills/agora/SKILL.md`: tightened skill trigger recall for voice AI, RTC, RTM, and CLI requests
- Skill install and runtime guidance aligned across references
- `skills/agora/references/cli/`: updated CLI reference coverage

## [1.6.0] - 2026-04-30

### Added

- `skills/agora/references/cli/quickstarts.md` — Agora CLI `init`, `quickstart create`, `quickstart env write`, and repo-local `.agora/project.json` binding guidance verified against CLI `0.1.7`
- `skills/agora/references/cli/env.md` — dedicated Agora CLI `project env` reference covering export formats, `AGORA_` variable names, secret opt-in behavior, managed-block writes, and default `.env*` target selection
- CLI eval coverage for `agora introspect --json`, telemetry controls, auth JSON unauthenticated handling, quickstart env vs project env, installed `agora` notation, and non-ConvoAI CLI routing
- CLI eval coverage in `tests/eval-cases.md` for `project env` export-first semantics, `--with-secrets`, default write-target safety, and OAuth loopback redirect mismatch guidance
- README prompt templates for explicitly telling agents to use the Agora skill, stay on the official sample-first path, and avoid undocumented CLI commands
- Anthropic fork sync automation for downstream skill distribution

### Changed

- `skills/agora/references/cli/README.md`, `skills/agora/references/cli/install-auth.md`, `skills/agora/references/cli/env.md`, `skills/agora/references/cli/projects.md`, `skills/agora/references/cli/doctor.md`, `skills/agora/references/cli/automation.md`: raised the verified CLI baseline to Go CLI `0.1.7`, `https://github.com/AgoraIO/cli`, curl/PowerShell/npm-wrapper install paths, `agora init`, `quickstart`, `introspect`, telemetry, upgrade, and v0.1.7 JSON automation behavior
- `skills/agora/references/conversational-ai/README.md`, `skills/agora/references/conversational-ai/quickstarts.md`: aligned ConvoAI first-success setup with `agora init`, `agora quickstart env write`, v0.1.7 CLI checks, and current quickstart env targets
- `skills/agora/SKILL.md`, `skills/agora/intake/SKILL.md`, `skills/agora/references/doc-fetching.md`, `skills/agora/references/mcp-tools.md`: expanded CLI routing, local-first CLI doc lookup, and clarified that `agora-docs-mcp` is docs traversal only while the CLI handles backend/account/project workflows
- `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`: documented Agora CLI as a first-class skill area and added the v0.1.7 maintenance workflow
- `skills/agora/references/cli/README.md`, `skills/agora/SKILL.md`: updated CLI routing and examples to include `agora project env` and `agora project env write` as first-class workflows
- `skills/agora/references/cli/automation.md`, `skills/agora/references/cli/projects.md`: shifted env guidance from `project show --json` toward `project env` / `project env write`, while keeping `project show --json` as metadata inspection
- `skills/agora/references/cli/install-auth.md`: documented the verified OAuth loopback rule that authorize and token-exchange `redirect_uri` values must match exactly, with `localhost` vs `127.0.0.1` mismatch called out explicitly
- `skills/agora/references/conversational-ai/README.md`, `skills/agora/references/conversational-ai/quickstarts.md`, `skills/agora/references/cli/doctor.md`: split ConvoAI onboarding into control-plane, runtime, and sample readiness so `doctor` no longer overclaims first-success readiness
- `skills/agora/references/conversational-ai/quickstarts.md`: replaced the old “use current project or create one” shortcut with a deterministic first-success project-selection policy that prefers the current project only when it is directly usable, otherwise selects a usable candidate or creates a new token-ready project
- `skills/agora/references/conversational-ai/auth-flow.md`, `skills/agora/references/integration-patterns.md`, `skills/agora/references/conversational-ai/agent-toolkit.md`, `skills/agora/references/conversational-ai/agent-client-toolkit-react.md`: added explicit RTM token-subject / login-identity alignment guidance and the RTM propagation-delay rule for first-success troubleshooting
- `tests/eval-cases.md`: added coverage for first-success project selection, RTM propagation delay, minimal sample workarounds, explicit skill prompting, `doctor` boundary checks, and rejection of invented CLI shortcuts

## [1.5.1] - 2026-04-29

### Added

- `skills/agora/references/cli/` — initial Agora CLI skill references (install, auth, projects, doctor, automation)
- CLI-assisted ConvoAI quickstart flow with agent-driven project readiness and auto env population
- Hermes Agent eval workflow
- ConvoAI quickstart hard gates: SAMPLE INTEGRITY, official-demo-first, and skill-only doc source rules
- Environment check step in the ConvoAI quickstart state machine

### Changed

- `skills/agora/references/conversational-ai/quickstarts.md`: default first-success path to `agent-quickstart-python`; removed baseline-path choices before first success
- `skills/agora/references/conversational-ai/quickstarts.md`: tightened first-success guidance and CLI version check requirements
- `skills/agora/references/cli/`: aligned CLI skill with `0.1.3` env workflows before the `0.1.7` expansion in v1.6.0
- `README.md`: capability-first rewrite and SEO/GEO optimization
- Skill and plugin versions aligned to `1.5.1`

## [1.4.0]

### Added

- Codex skill evaluation workflow (`codex-eval.yml`)
- Gemini CLI skill evaluation workflow (`gemini-eval.yml`)
- Skill quality review workflow (`skill-judge.yml`)
- ConvoAI quickstart gating regression cases in `tests/eval-cases.md` — working-baseline detection, no `/join` bypass, and quickstart-skip coverage
- ConvoAI vendor-default coverage in `tests/eval-cases.md` — Python SDK-backed first-success provider combo and default-parameter checks

### Changed

- `SKILL.md`, `references/conversational-ai/README.md`: changed documentation lookup to a strict local-reference-first policy so ConvoAI requests consult bundled module references before any Level 2 live-doc fetch
- `SKILL.md`: added stronger direct-routing cues for clearly ConvoAI-specific requests such as agent demos, provider questions, and MLLM requests instead of sending them to intake first
- `references/conversational-ai/README.md`: added working-baseline routing so new-project and unproven integration requests enter a constrained quickstart path before code generation
- `references/conversational-ai/quickstarts.md`: rewritten as a locked quickstart state machine with baseline-path, readiness, and backend-path gates; preserves the existing repo/setup references after the gates resolve
- `references/conversational-ai/quickstarts.md`, `references/conversational-ai/python-sdk.md`, `references/conversational-ai/README.md`: now use the official current provider docs as the source of truth for provider matrices and vendor-specific configs, while keeping the local quickstart focused on the first-success default combo and sample-aligned env names
- `references/conversational-ai/quickstarts.md`, `references/conversational-ai/README.md`: aligned the sequence with the state machine, made the MLLM vs cascading split explicit in the vendor gate, documented baseline-path rollback behavior, and clarified that Path B may require a private repo fallback
- `references/conversational-ai/quickstarts.md`: softened the opening quickstart wording for user-facing conversations and added an explicit unsupported-provider prompt instead of implicit discouragement
- `references/conversational-ai/quickstarts.md`, `references/conversational-ai/README.md`: added a Studio Agent ID branch so Agora ConvoAI can reuse agents configured in `https://console.agora.io/studio/agents` instead of rebuilding the provider stack during quickstart
- `references/conversational-ai/conversational-ai-studio.md`: added a dedicated reference for the Agora Studio Agent ID path and clarified that it is different from the runtime `agent_id` returned by `/join`
- `references/conversational-ai/conversational-ai-studio.md`, `references/conversational-ai/quickstarts.md`, `references/conversational-ai/README.md`: documented the confirmed mapping that the Agora Studio Agent ID is passed via the request field `pipeline_id`
- `references/conversational-ai/conversational-ai-studio.md`: expanded the Studio path into a fixed request contract mirroring the preconfigured-agent flow, including field mapping, token separation, and response expectations

## [1.2.0]

### Added

- RTC React Native reference (`references/rtc/react-native.md`) — `react-native-agora`: engine init, events, `RtcSurfaceView`, cleanup
- RTC Flutter reference (`references/rtc/flutter.md`) — `agora_rtc_engine`: engine init, `AgoraVideoView`, `RtcEngineEventHandler`, cleanup
- RTM iOS reference (`references/rtm/ios.md`) — `AgoraRtmClientKit` v2 (Swift): init, login, subscribe, publish, presence, delegate
- RTM Android reference (`references/rtm/android.md`) — `RtmClient` v2 (Kotlin): init, login, subscribe, publish, event listener
- ConvoAI iOS toolkit reference (`references/conversational-ai/agent-toolkit-ios.md`) — `ConversationalAIAPIImpl` Swift patterns
- ConvoAI Android toolkit reference (`references/conversational-ai/agent-toolkit-android.md`) — `ConversationalAIAPIImpl` Kotlin patterns
- Multi-product integration guide (`references/integration-patterns.md`) — RTC+RTM+ConvoAI init order, UID strategy, channel naming, token matrix, codec selection, cleanup sequence
- Testing guidance expanded — RTC React Native, Flutter, RTM Web/iOS/Android mocking patterns; token renewal section; table of contents

### Changed

- `rtc/react.md`: add codec interop note — `vp8` recommended; `vp9` hardware-limited on older iOS Safari; `h264` does not scale for multi-user
- `rtc/cross-platform-coordination.md`: corrected codec table — `vp8` is the safe default; `vp9` requires iPhone 15 Pro / M3+ hardware on iOS Safari; `h264` avoid for multi-user
- `rtc/README.md`: updated codec interop note to match corrected recommendation
- `rtm/ios.md`, `rtm/android.md`: added v2 to titles to prevent v1 API misuse
- `rtm/README.md`: added Platform Scope section clarifying client-side only, all v2, no server/desktop variant
- `rtm/web.md`: removed RTM v1 legacy section; constructor wrapped in try/catch; token-only login form
- `conversational-ai/README.md`: added SDK-vs-REST routing table; RTM channel name = RTC channel name gotcha; scoped auth section to direct REST implementors
- `conversational-ai/auth-flow.md`: scoped to REST API implementors; added SDK-skip callout at top
- `SKILL.md`: bumped version to 1.2.0; added Multi-Product Integration entry; expanded RTC platform list (React Native, Flutter) and RTM platform list (iOS, Android)
- `CLAUDE.md`, `README.md`: updated file structure trees and product lists to reflect all new files and platforms

## [1.1.0]

### Added

- Cloud Recording references (`references/cloud-recording/`) — REST API acquire/start/query/stop lifecycle
- Server Gateway references (`references/server-gateway/`) — Linux C++ SDK setup and media pipeline
- Testing Guidance skill (`references/testing-guidance/SKILL.md`) — ConvoAI and RTC test patterns
- Next.js RTC pattern (`references/rtc/nextjs.md`) — SSR-safe dynamic import guidance
- ConvoAI agent client toolkit React references (`references/conversational-ai/agent-client-toolkit-react.md`) — provider, hooks, transcript, state
- Intake router (`skills/agora/intake/SKILL.md`) — multi-product needs analysis for ambiguous requests
- Agora token-based auth for ConvoAI REST API — inline gotcha + implementation in `conversational-ai/README.md`
- OpenAI Realtime MLLM configuration in `agent-samples.md`
- Agora Docs MCP server config bundled in `.claude-plugin/mcp-config.json`

### Changed

- `plugin.json` repository URL corrected to `AgoraIO/skills`
- `marketplace.json` version aligned to `1.1.0`
- `SECURITY.md` vulnerability report URL corrected to `AgoraIO/skills`

## [1.0.0]

### Added

- RTC references for Web, React, iOS (Swift), Android (Kotlin/Java)
- RTM Web references — messaging, presence, stream channels
- Conversational AI references — REST API, agent config, 5 recipe files
- Server-side token generation references
- 4-layer progressive disclosure architecture (`SKILL.md` → product README → topic file)
- Eval cases in `tests/eval-cases.md` (25 cases across R, C, F, I series)
- Validation script (`scripts/validate-skills.sh`)
