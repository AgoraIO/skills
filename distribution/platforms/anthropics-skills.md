# anthropics/skills Contribution Pack

## Target

- Repository: `https://github.com/anthropics/skills`
- Current fit: public example and partner-signal repository for Claude-compatible Agent Skills

## Why Agora Fits

- Official vendor-maintained skill pack
- Uses the standard `SKILL.md` + references layout
- Includes plugin metadata in `.claude-plugin/`
- Covers a real developer workflow with clear product routing, onboarding rules, and eval coverage

## Contribution Shape

This repo now includes an automated export path that publishes the Agora source skill to the Anthropic-style contribution name `voice-ai-integration`.

- Source skill: `skills/agora/`
- Exported skill name: `voice-ai-integration`
- Exported intake skill name: `voice-ai-integration-intake`
- Sync workflow: `.github/workflows/sync-anthropics-fork.yml`
- Export script: `scripts/export-anthropic-skill.sh`

## Suggested PR Title

`Add voice-ai-integration skill for Agora-powered voice AI workflows`

## Suggested PR Summary

This PR adds `voice-ai-integration`, a Claude-compatible skill bundle generated from Agora's official skill pack.

The skill pack helps agents build real-time voice, video, messaging, and conversational AI applications on Agora. It includes:

- RTC guidance for Web, React, Next.js, iOS, Android, React Native, and Flutter
- RTM guidance for Web, iOS, and Android
- Conversational AI guidance with strict sample-first onboarding
- Cloud Recording and server-side token generation references
- Multi-product routing and testing guidance

The repository already includes:

- canonical `SKILL.md` entrypoints
- validation coverage via `scripts/validate-skills.sh`
- eval coverage in `tests/eval-cases.md`
- Claude-compatible plugin metadata in `.claude-plugin/`
- an automated sync workflow that keeps the forked contribution branch up to date

## Suggested Reviewer Notes

- Official Agora-maintained repository
- Uses progressive disclosure to keep context small
- Strongest value is reliable routing and prevention of common integration mistakes
- ConvoAI paths intentionally enforce an official sample-first workflow

## Sample Prompts

- `Use the voice-ai-integration skill to help me build a voice AI agent demo.`
- `Use the voice-ai-integration skill and show me how to implement RTC video calling on Web.`
- `Route this request through the voice-ai-integration skill and help me generate a production token server.`

## Asset Mapping

- Source skill entry: `skills/agora/SKILL.md`
- Exported contribution path: `skills/voice-ai-integration/`
- Sync workflow: `.github/workflows/sync-anthropics-fork.yml`
- PR body template: `distribution/platforms/anthropics-pr-body.md`

## Ready-To-Submit Checklist

- [x] PR title prepared
- [x] PR summary prepared
- [x] Reviewer notes prepared
- [x] Sample prompts prepared
- [x] Repo asset mapping prepared
- [x] Sync automation prepared for the fork `chenyuguo-agora/skills`
- [ ] Secret `ANTHROPICS_SKILLS_SYNC_TOKEN` added in GitHub Actions
- [ ] First sync workflow run completed
- [ ] Upstream PR opened to `anthropics/skills`
