# Agora Skills

**The fastest way to build real-time conversational AI applications and Voice Agents with your AI coding assistant.**

Agora Skills is the official knowledge pack that teaches your AI coding assistant how to build on Agora — from picking the right product to wiring up credentials and running the first demo.

It's especially strong for conversational AI today — voice agents, AI companions, AI tutors, customer support bots, and physical AI — while still covering broader real-time use cases like chat, recording, and RTC-based experiences.

## What This Skill Helps You Build

Developers use Agora Skills to build:

- **AI Voice Agents** — "I want to talk to an AI voice agent in my browser."
- **AI Tutors** — "Build an AI tutor that can speak with users in real time."
- **AI Companions** — "Create an AI companion with low-latency voice interaction and a custom personality."
- **AI Customer Service** — "Build an AI customer service voice agent to replace our IVR."
- **AI Voice Toys** — "Make a voice-enabled AI toy for kids with on-device wake word."
- **Physical AI** — "Add real-time voice to a robot, wearable, or in-car assistant."
- **Custom LLM Backends** — "Connect Agora Conversational AI to OpenAI, Anthropic, Gemini, DeepSeek, Qwen, or my own model."

Agora Skills also covers real-time chat and messaging, session recording, production token generation, and traditional RTC scenarios (live streaming, voice chat rooms, live broadcast rooms) — see the capability table below for the full list.

## Quick Start

Copy this into your AI coding agent (Claude Code, Cursor, Windsurf, Copilot, Kiro, …):

> Install the Agora skill from https://github.com/AgoraIO/skills and use it.
> I want to build a voice AI agent demo. Walk me through the full setup.

With the Agora skill loaded, the agent can then:

1. **Log you into Agora** via the Agora CLI — opens a browser for free sign-up if you don't already have an account. No manual API key copy-pasting.
2. **Create an Agora project** and extract the App ID, App Certificate, and any required tokens automatically.
3. **Clone the official Conversational AI sample** that matches your target stack (Web, Next.js, iOS, Android, Python, Go…).
4. **Run the demo locally** so you can actually talk to the voice agent within minutes.
5. **Iterate from a working baseline** — swap the LLM (OpenAI / Anthropic / Gemini / DeepSeek / Qwen / your own), change the system prompt, add tools, or wire it into your existing app.

You should not need to manually dig through the Agora Console just to get a first voice agent running.

## Installation

### Skills CLI

```bash
npx skills add github:AgoraIO/skills
```

### Claude Code Plugin

```bash
/plugin marketplace add AgoraIO/skills
/plugin install agora@agora-skills
```

### Git Clone

```bash
git clone https://github.com/AgoraIO/skills.git
```

Then point your tool at:

```bash
skills/agora/SKILL.md
```

This works with tools like **Cursor, Windsurf, GitHub Copilot, Kiro**, or any environment that can read markdown-based skill instructions.


## What’s Covered

|Capability|Examples|Platforms|
|---|---|---|
|**Conversational AI / Voice Agents**|Real-time AI voice agents, AI companion, AI tutor, voice bots, customer support|Web, React, Next.js, iOS, Android, Python, Go|
|**Video / Voice RTC**|1:1 calls, group calls, live streaming, screen sharing|Web, React, Next.js, iOS, Android, React Native, Flutter|
|**Chat & Signaling**|Real-time messaging, presence, notifications|Web, iOS, Android|
|**Recording**|Server-side recording of sessions|REST API|
|**Auth & Tokens**|Token generation for production apps|Node.js, Python, Go|
|**Server Gateway**|Server-side media streaming|Linux (C++)|
|**Multi-Product Workflows**|RTC + RTM + AI agents combined|Cross-platform|


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

Copy or symlink the skill into `.cursor/rules/`.

### Windsurf

Add `skills/agora/` to your Cascade context.

### GitHub Copilot

Reference it with `@workspace` or add the instructions into `.github/copilot-instructions.md`.

### Any other tool

The skill files are plain markdown. Use `skills/agora/SKILL.md` as the entry point.

## Contributing

See[ `CONTRIBUTING.md`](https://github.com/AgoraIO/skills/blob/feat/readme-and-description-rewrite/CONTRIBUTING.md).

## About

Powered by [Agora](agora.io)(agora.io) — the real-time engagement platform behind voice, video, messaging, and interactive AI experiences.

- Agora Documentation: [https://docs.agora.io/](https://docs.agora.io/)
- Agora Console: [https://console.agora.io/](https://console.agora.io/)
- Agora GitHub: [https://github.com/AgoraIO](https://github.com/AgoraIO)

## License

MIT
