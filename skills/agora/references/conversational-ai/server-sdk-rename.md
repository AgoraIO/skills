---
name: agora-server-sdk-rename
description: |
  Opt-in only. Load when the user's project uses outdated ConvoAI server SDK package or
  module names and they need to migrate to current names. Do not load for greenfield work.
  Triggers on: agora-agent-server-sdk, agora-agent (PyPI), agora-agent-server-sdk-go,
  AgoraIO-Community/agora-agent-server-sdk-go, migrate agora sdk, upgrade server sdk package.
license: MIT
metadata:
  author: agora
  version: '1.0.0'
---

# ConvoAI Server SDK — package rename migration

> **Opt-in only.** Load this file when workspace detection or the user shows outdated server SDK names. Default ConvoAI routing uses [server-sdks.md](server-sdks.md), [python-sdk.md](python-sdk.md), and [go-sdk.md](go-sdk.md) with current names.

Apply the renames below in dependency manifests and import statements. The public API is unchanged — only install paths and import strings move.

## Detection signals

Scan the user's project (read-only) for any of:

| Signal | Where to look |
|--------|----------------|
| `agora-agent-server-sdk` | `package.json`, lockfiles, `import` / `require` strings |
| `agora-agent` (not `agora-agents`) | `pyproject.toml`, `requirements.txt`, `Pipfile`, `poetry.lock` |
| `github.com/AgoraIO-Community/agora-agent-server-sdk-go` | `go.mod`, Go import paths |
| `agent-server-sdk-go` repo URL | README, CI config, docs |

If none match, do not load this file.

## Rename map

### TypeScript / npm

| Update | From | To |
|--------|------|-----|
| Dependency | `agora-agent-server-sdk` | `agora-agents` |
| Import | `from 'agora-agent-server-sdk'` | `from 'agora-agents'` |

The npm package `agora-agent-server-sdk` still resolves via a compat shim, but new projects and migrations should use `agora-agents`.

### Python / PyPI

| Update | From | To |
|--------|------|-----|
| Dependency | `agora-agent` or `agora-agent-server-sdk` | `agora-agents` |
| Import | `from agora_agent import ...` | **No change** |

Only the PyPI install name changes. Python import paths stay `agora_agent`.

### Go

| Update | From | To |
|--------|------|-----|
| Module | `github.com/AgoraIO-Community/agora-agent-server-sdk-go` | `github.com/AgoraIO/agora-agents-go` |
| Imports | `.../agora-agent-server-sdk-go/...` | `github.com/AgoraIO/agora-agents-go/...` |
| Repo | `AgoraIO-Conversational-AI/agent-server-sdk-go` | `AgoraIO/agora-agents-go` |

Go has no module alias — update `go.mod` and all import paths together, then `go mod tidy`.

## Migration steps

1. Update the manifest (`package.json`, `pyproject.toml` / `requirements.txt`, or `go.mod`).
2. Replace import strings in source files per the table above.
3. Reinstall / tidy (`npm install`, `pip install -r ...`, or `go mod tidy`).
4. Run the project's test suite or a minimal start/stop agent smoke test.

Do not change application logic, env var names, or AgentKit builder code — the API surface is the same.

## After migration

Route back to the current SDK references for ongoing work:

- TypeScript: [server-sdks.md](server-sdks.md)
- Python: [python-sdk.md](python-sdk.md)
- Go: [go-sdk.md](go-sdk.md)
