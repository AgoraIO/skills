# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
