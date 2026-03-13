# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
- Agora MCP server config bundled in `.claude-plugin/mcp-config.json`

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
