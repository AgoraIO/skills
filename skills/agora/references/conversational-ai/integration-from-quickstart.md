---
name: conversational-ai-integration-from-quickstart
description: |
  Existing-app integration workflow for Agora Conversational AI. Use when the user has a web, mobile, backend, or multi-project app and wants ConvoAI added. Detect the app shape with read-only inspection, clone or inspect the official quickstart as source, then produce a copy map before editing the existing app.
license: MIT
metadata:
  author: agora
  version: '1.0.0'
---

# ConvoAI Integration From Quickstart

Use this file after [README.md](README.md) classifies a request as `integration`: the user has an existing app or multi-project workspace and wants Agora ConvoAI added.

The workflow is:

1. **Detect the app shape** with read-only inspection.
2. **Inspect the official quickstart source** in a separate folder or branch.
3. **Map what to copy or adapt** before editing the existing app.
4. **Integrate minimally** while preserving the app's architecture.

Do not edit the existing app until the official quickstart source has been inspected and a copy map exists. Runtime proof from [quickstarts.md](quickstarts.md) is required before claiming the integrated app works, but the quickstart's main role is to provide source-of-truth code rather than code generated from memory.

## Detect First, Then Ask

Resolve required values in this order:

1. **Session memory**: use what the user already said.
2. **Workspace detection**: inspect files read-only.
3. **Ask the user**: only for the missing value, after stating what was detected.

Explicit user statements win over detected values. The latest user statement wins on conflict.

## Read-Only Detection Signals

Use file inspection only. Do not install, run, write config, or start app code during detection.

Initial scan scope:

- repo root
- first-level common dirs: `server/`, `api/`, `backend/`, `client/`, `web/`, `frontend/`, `mobile/`, `apps/*`, `packages/*`
- skip `node_modules`, `.git`, `dist`, `build`, `.next`, `coverage`

| Signal                                                                | Detects                                                                                                                                             |
| --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `package.json` deps                                                   | Frontend (`next`, `react`, `vue`, `svelte`, `astro`, `nuxt`, `remix`, `solid-js`) and backend (`express`, `fastify`, `koa`, `@nestjs/core`, `hono`) |
| `pyproject.toml` / `requirements.txt`                                 | Python backend; framework via `fastapi`, `flask`, `django`                                                                                          |
| `go.mod`                                                              | Go backend; framework via `gin`, `echo`, `fiber`                                                                                                    |
| `pom.xml` / `build.gradle`                                            | Java backend                                                                                                                                        |
| `Gemfile`                                                             | Ruby / Rails backend                                                                                                                                |
| `composer.json`                                                       | PHP backend                                                                                                                                         |
| `.csproj` / `.sln`                                                    | .NET backend                                                                                                                                        |
| `pubspec.yaml`                                                        | Flutter mobile                                                                                                                                      |
| `Podfile` + `*.xcodeproj`                                             | iOS native                                                                                                                                          |
| `build.gradle` + `app/src/main/AndroidManifest.xml`                   | Android native                                                                                                                                      |
| `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`          | Monorepo roots and workspace apps                                                                                                                   |
| `.env`, `.env.local`, `.env.example`                                  | Existing env naming conventions                                                                                                                     |
| `agora-rtc-sdk-ng`, `agora-rtm-sdk`, `agora-token`, `agora-rtc-react` | Existing Agora RTC/RTM/token wiring                                                                                                                 |
| `vercel.json`, `netlify.toml`, `Dockerfile`, `fly.toml`               | Deployment hints only                                                                                                                               |

## App Inventory Artifact

Emit `app_inventory` once during integration setup.

```yaml
app_inventory:
  workspace_layout: single # single | monorepo-configured | monorepo-implicit | client-backend-split | side-by-side
  frontend:
    framework: nextjs # nextjs | react | vue | svelte | astro | nuxt | remix | none | unknown
    version: '15'
    detected_from: package.json
  backend:
    language: python # node | python | go | java | ruby | php | csharp | none | unknown
    framework: fastapi # express | fastapi | django | gin | spring | rails | none | unknown
    detected_from: pyproject.toml
  mobile:
    platform: none # ios | android | flutter | react-native | none
  projects:
    - path: apps/web
      role: frontend
      framework: nextjs
    - path: apps/api
      role: backend
      language: python
      framework: fastapi
  integration_targets:
    - apps/api
    - apps/web
  agora_already_installed: false
  baseline_track: python # python | nextjs | agent-samples | unsupported
  detection_confidence: high # high | medium | low
```

For `workspace_layout: single`, `projects` may be absent and `integration_targets` can be auto-populated. For multi-project workspaces, populate `integration_targets` from the user's answer to the listing question.

## Detection Confidence

Confidence is `high` only when the target frontend and backend resolve to a single, documented framework with no conflicts.

| Case                                                                  | Confidence | Action                                                                                        |
| --------------------------------------------------------------------- | ---------- | --------------------------------------------------------------------------------------------- |
| Single Next.js app, no conflicting backend                            | `high`     | Pick `baseline_track: nextjs`; skip stack-preference intake.                                  |
| Single Python backend + web client                                    | `high`     | Pick `baseline_track: python`; skip stack-preference intake.                                  |
| Conflicting frontend frameworks, such as `next` and `vite`            | `medium`   | State both candidates and ask which is active.                                                |
| React dependency but no framework or directory signal                 | `medium`   | Ask whether it is Vite, CRA, Next.js, or custom.                                              |
| Mixed Node and Python backend frameworks                              | `medium`   | Ask which backend starts server-side actions.                                                 |
| Configured monorepo with multiple apps                                | `medium`   | List apps and ask which are integration targets.                                              |
| Implicit monorepo with multiple project files but no workspace config | `medium`   | List candidate projects and ask which target to use.                                          |
| Client/backend split, such as `client/` + `server/`                   | `medium`   | Explain backend starts the agent and client joins RTC; ask whether to wire both.              |
| Web plus mobile clients                                               | `medium`   | Ask which client or clients should join the channel.                                          |
| Existing Agora RTC packages but no proven ConvoAI baseline            | `medium`   | State that RTC is already present, but baseline still runs separately first.                  |
| Empty or stub project files                                           | `low`      | Ask whether this is the correct project root or a fresh project.                              |
| Scan error, unreadable file, broken symlink, or encoding failure      | `low`      | Report which file failed and ask one focused question. Never guess.                           |
| Only unsupported backend stack, such as Rails, PHP, Java, or .NET     | `medium`   | Prove baseline in Python or Node, then use [auth-flow.md](auth-flow.md) for REST integration. |
| No actionable signals                                                 | `low`      | Treat as likely `quickstart`, not `integration`.                                              |

Before asking any question for `medium` or `low`, list what was detected. Do not ask blind.

Example:

```text
I see:
- apps/web: Next.js
- apps/api: FastAPI
- apps/mobile: React Native

ConvoAI needs a backend to start the agent and at least one client to join the RTC channel. Should I wire `apps/api` + `apps/web`, or include `apps/mobile` too?
```

## Source Phase

Clone or open the official quickstart separately from the user's app:

- use a separate directory or branch
- do not scaffold a replacement app
- do not edit the existing app until the copy map exists
- use [quickstarts.md](quickstarts.md) for commands, state machine, prompt/config customization, and runtime proof
- if the user has an Agora Studio Agent ID, source the baseline from the official quickstart using the Studio-managed path from [conversational-ai-studio.md](conversational-ai-studio.md), then return here

If quickstart clone or source inspection fails, troubleshoot that first and pause integration edits. If runtime verification fails later, keep troubleshooting the quickstart/environment before claiming the existing-app integration works.

## Copy Map Required

Before editing the existing app, produce a copy map from inspected quickstart files:

| Source quickstart file | Destination in existing app | Adaptation notes                                                     |
| ---------------------- | --------------------------- | -------------------------------------------------------------------- |
| `[quickstart path]`    | `[existing app path]`       | Env names, auth route, token generation, client hook, RTC/RTM events |

Allowed to copy or adapt after baseline:

- ConvoAI session lifecycle
- auth and token flow
- RTC/RTM channel wiring
- event handling for agent state, metrics, errors, and transcripts
- minimal UI controls needed to start, stop, and observe the agent

Forbidden before source alignment:

- replacing the user's app architecture
- creating a fresh standalone app in the user's repo
- using undocumented commands or command variants
- adding new server routes, client hooks, or UI code before the copy map exists

## Integration Completion Gates

Track these after source alignment. `baseline_verified` may remain false while the agent prepares the copy map or adapts quickstart-derived code, but it must be true before the agent claims the integration works.

```yaml
integration_gate:
  source_inspected: true
  baseline_verified: false
  copy_map_approved: false
  integration_compiles: false
  agent_start_stop_in_app: false
  voice_roundtrip_verified: false
```

- `source_inspected`: official quickstart files were cloned/opened and used as source for the copy map.
- `baseline_verified`: `baseline_gate` from [quickstarts.md](quickstarts.md) is all true.
- `copy_map_approved`: user approved the map, or explicitly said to proceed.
- `integration_compiles`: existing app builds or type-checks with the integration.
- `agent_start_stop_in_app`: existing app can start and stop the agent.
- `voice_roundtrip_verified`: user can speak from the existing app and hear agent audio.

## Integration Response Template

For integration replies, be quiet unless state changes or something is blocked. Before runtime proof, make clear that the app is being adapted from quickstart source; do not claim it works until `voice_roundtrip_verified` is true.

When status is needed, include:

```yaml
current_gate:
  baseline_verified: true
  copy_map_approved: false
next_command: '[exact command or none]'
files_to_copy_or_adapt_next:
  - source: '[quickstart file]'
    destination: '[existing app file]'
blocked: 'copy_map_approved is false; produce or approve the copy map first'
```

Use user-facing words "baseline" and "integration"; do not say "Track A" or "Track B" in chat.
