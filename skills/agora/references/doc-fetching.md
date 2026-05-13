# Documentation Lookup

**Level 1 — Bundled references (always try first)**

Check the relevant file under `skills/agora/references/`. These are inline-stable:
RTC init patterns, RTM messaging, token generation, ConvoAI gotchas and generation
rules. If the answer is here, stop — no fetch needed.

**Level 2 — Live docs (when Level 1 is insufficient)**

When bundled references don't cover the detail needed (full request/response schemas,
vendor-specific configs, language-specific quick-start code):

If the Agora Docs MCP tool (`agora-docs-mcp`) is available in the current tool/runtime, prefer it for Level 2 documentation lookup. Otherwise use the HTTP fetch flow below. If MCP returns no useful result, fall back to HTTP fetch.

1. Fetch the Agora docs sitemap:
   ```
   GET https://docs.agora.io/en/llms.txt
   ```
2. Scan the response for a URL matching the product and topic.
3. Fetch that URL and use its content to answer.

## Fallback

If `llms.txt` is unreachable or the fetched URL returns no useful content, try these
known markdown entry points directly:

| Product / Language | Markdown URL |
|---|---|
| RTC (Web/general) | https://docs-md.agora.io/en/video-calling/get-started/get-started-sdk.md |
| RTC (voice-only) | https://docs-md.agora.io/en/voice-calling/get-started/get-started-sdk.md |
| RTM (Web/general) | https://docs-md.agora.io/en/signaling/get-started/sdk-quickstart.md |
| RTM (iOS) | https://docs-md.agora.io/en/signaling/get-started/sdk-quickstart?platform=ios.md |
| RTM (Android) | https://docs-md.agora.io/en/signaling/get-started/sdk-quickstart?platform=android.md |
| ConvoAI | https://docs-md.agora.io/en/conversational-ai/get-started/quickstart.md |
| ConvoAI (TypeScript SDK) | https://docs-md.agora.io/en/conversational-ai/develop/integrate-sdk.md |
| ConvoAI (Python SDK) | https://docs-md.agora.io/en/conversational-ai/develop/integrate-sdk?platform=python.md |
| Cloud Recording | https://docs-md.agora.io/en/cloud-recording/get-started/getstarted.md |
| Server Gateway (C++) | https://docs-md.agora.io/en/server-gateway/get-started/integrate-sdk.md |
| Server Gateway (Java) | https://docs-md.agora.io/en/server-gateway/get-started/integrate-sdk?platform=java.md |
| Server Gateway (Python) | https://docs-md.agora.io/en/server-gateway/get-started/integrate-sdk?platform=python.md |
| Server Gateway (Go) | https://docs-md.agora.io/en/server-gateway/get-started/integrate-sdk?platform=go.md |
| Tokens | https://docs-md.agora.io/en/video-calling/token-authentication/deploy-token-server.md |

## Agora Docs MCP Server (optional)

Agora also provides `agora-docs-mcp`, an MCP server that gives AI assistants
direct tool-call access to documentation — an alternative to the Level 2 HTTP
fetch above. It traverses docs only; it does not use Agora backend APIs, log in,
create projects, or inspect account state. If a user asks about installing or
using the Agora Docs MCP server, see [mcp-tools.md](mcp-tools.md).

## Agora CLI

For local `agora` command-line usage, check [cli/README.md](cli/README.md) first. Treat that file as the source of truth for the currently verified CLI baseline and command surface.

If the bundled CLI references do not cover a CLI-only detail, use the canonical CLI repository instead of general Agora product docs:

- <https://github.com/AgoraIO/cli>
- `README.md` — install, first run, command model, common workflows
- `docs/commands.md` — generated command reference
- `docs/automation.md` — JSON envelopes and automation contract
- `docs/error-codes.md` — stable error codes and recovery decisions
- `docs/telemetry.md` — telemetry preferences and environment controls
- `CHANGELOG.md` and GitHub Releases — version-specific changes

Do not invent CLI commands, flags, environment variables, or JSON fields. If the installed CLI exposes a command that is not in the bundled references, prefer `agora introspect --json` or `agora --help --all`, then cross-check the CLI repository docs before answering.
