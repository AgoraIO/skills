# Agora Skills

Add real-time voice, video, and AI voice agent capabilities to your app — with your AI coding assistant doing the heavy lifting. This skill gives your agent the knowledge to build video calls, live streaming, AI voice conversations, chat, recording, and more.

## What Can You Build?

- "I want to talk to an AI voice agent in my browser"
- "Add video calling to my app"
- "Build a live streaming feature"
- "I need real-time chat and messaging"
- "Record my voice/video sessions"
- "Generate auth tokens for my backend"

Just describe what you want. The skill handles the rest — from account setup and credentials to running a working demo.

## Quick Start

Copy this into your AI agent:

```text
Install the Agora skill from https://github.com/AgoraIO/skills and use it.
I want to build a voice AI agent demo. Walk me through the full setup.
```

The agent will:
1. Log in to your Agora account via CLI (opens browser — sign up for free if you don't have one)
2. Create a project and get credentials automatically
3. Configure credentials automatically
4. Start the demo

You don't need to visit the Agora Console or copy API keys — the agent uses the CLI to handle login, project creation, and credential extraction. You just complete the browser sign-in when prompted.

## Installation

### Skills CLI

```bash
npx skills add github:AgoraIO/skills
```

### Claude Code Plugin

```
/plugin marketplace add AgoraIO/skills
/plugin install agora@agora-skills
```

### Git Clone

```bash
git clone https://github.com/AgoraIO/skills.git
```

Point your tool at `skills/agora/SKILL.md` as the entry point. Works with Cursor, Windsurf, GitHub Copilot, Kiro, or any tool that reads markdown.

## How It Works

1. You describe what you want to build
2. The skill routes to the right product (voice AI, video, chat, etc.)
3. For demos and prototypes, the agent clones an official sample and runs it as-is
4. Credentials are handled via the [Agora CLI](https://www.npmjs.com/package/agoraio-cli) — the agent logs into your Agora account, creates a project, and extracts the credentials automatically
5. Once the baseline works, you can customize

## What's Covered

| Capability | Examples | Platforms |
|-----------|----------|-----------|
| AI Voice Agents | Talk to an AI in real time, custom LLM backends, voice bots | Web, React, Next.js, iOS, Android, Python, Go |
| Video/Voice Calls | 1:1 calls, group calls, live streaming, screen sharing | Web, React, Next.js, iOS, Android, React Native, Flutter |
| Chat & Signaling | Real-time messaging, presence, notifications | Web, iOS, Android |
| Recording | Server-side recording of sessions | REST API |
| Auth & Tokens | Token generation for production apps | Node.js, Python, Go |
| Server Gateway | Server-side media streaming | Linux (C++) |
| Multi-Product | RTC + RTM + AI agents combined | Cross-platform |

For architecture details and file structure, see [ARCHITECTURE.md](ARCHITECTURE.md).

## IDE & Tool Setup

### Claude Code — symlink (user-level)

```bash
npx skills add github:AgoraIO/skills
# or manually:
ln -s ~/agora-skills/skills/agora ~/.claude/skills/agora
```

### Claude Code — copy (project-level, shared with team)

```bash
mkdir -p .claude/skills
cp -r ~/agora-skills/skills/agora .claude/skills/agora
```

### Cursor

Copy or symlink into `.cursor/rules/`. See [Cursor skills docs](https://cursor.com/docs/skills#skill-directories).

### Windsurf

Add `skills/agora/` to your Cascade context. See [Windsurf skills docs](https://docs.windsurf.com/windsurf/cascade/skills).

### GitHub Copilot

Reference via `@workspace` or add to `.github/copilot-instructions.md`. See [Copilot skills docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-skills).

### Any other tool

The skill files are plain markdown. Point your tool at `skills/agora/SKILL.md` as the entry point — it links to everything else.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## About

Powered by [Agora](https://www.agora.io) (agora.io) — the real-time engagement platform behind billions of voice, video, and interactive experiences worldwide.

- [Agora Documentation](https://docs.agora.io)
- [Agora Console](https://console.agora.io)
- [Agora GitHub](https://github.com/AgoraIO)

## License

MIT
