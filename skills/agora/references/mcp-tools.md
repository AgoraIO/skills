# Agora Docs MCP Server

<!-- applies-from: v0.2.0 -->

The Agora Docs MCP server gives AI assistants access to Agora documentation search.
The bundled plugin uses `agora-docs-mcp` as the connection name.
Follow the lookup policy in [doc-fetching.md](doc-fetching.md) for live documentation.

**MCP endpoint:** `https://mcp.agora.io`

The server searches product guides and SDK API references.
Use filter discovery when an advertised tool supports it.
Use the local `agora` CLI for login, projects, environment files, and readiness checks.

**Use MCP only when the user explicitly asks for it.** The Claude Code plugin connects this server automatically, so being connected is not consent. For every other Level 2 lookup, use the HTTP flow in [doc-fetching.md](doc-fetching.md).

## Data sent to the server

`mcp.agora.io` is a read-only documentation search server hosted by [Algolia](https://www.algolia.com/doc/guides/model-context-protocol) for Agora. Every tool call sends its arguments to Algolia. Besides search terms, the tool schemas can require context fields: for example, the user's original request, the assistant's interpretation of the user's intent, and a conversation session ID. Algolia processes this data under its [Privacy Policy](https://www.algolia.com/policies/privacy/).

When filling any field that carries user context:

- Include only the documentation question: product, platform, feature, and error text.
- Never include credentials, tokens, App IDs, App Certificates, Customer Secrets, API keys, `.env` contents, or private URLs.
- Never include personal data, customer data, or proprietary source code. Describe the code's API usage instead of pasting it.
- If the request cannot be summarized without sensitive content, use the HTTP lookup instead and tell the user why.

## Discover tools before calling them

The connected MCP client exposes tool names, descriptions, and input schemas.
Use those definitions as the source of truth for each call.

1. Inspect the tools exposed by the connected Agora Docs MCP server.
2. Select a tool whose description matches the product, platform, and task.
3. Read its input schema. Supply every required field, including any required context or session fields, following the rules in [Data sent to the server](#data-sent-to-the-server).
4. Use the declared types for queries and filters. Read supported filter values from the schema or discovery results.
5. Read the result. Open returned documentation URLs when excerpts do not contain the complete answer.

For a guide on `docs.agora.io`, append `.md` to read its Markdown content.
Use the original URL for references hosted on other domains.

If the server rejects a tool name or its arguments, refresh the tool catalog.
Inspect the current schema before another call.
If MCP is unavailable or returns no useful content, use the HTTP lookup in [doc-fetching.md](doc-fetching.md).

For a custom MCP client, initialize the connection and request the catalog with `tools/list`.
Follow `nextCursor` until the catalog is complete.
For protocol details, see the [MCP tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools).

## Installation

**Claude Code:**

```bash
claude mcp add agora-docs-mcp --transport http https://mcp.agora.io
```

**Cursor / Windsurf / other MCP-compatible tools:** Add `https://mcp.agora.io` as
an HTTP MCP server in your tool's MCP settings. See your tool's documentation for
the exact configuration format.

For setup instructions, see:
<https://docs.agora.io/en/introduction/agora-mcp.md>

## Usage note

Use quickstart documentation to check API structure and field names.
Apply the credential handling and generation rules in [ConvoAI integration guidance](conversational-ai/README.md) before generating ConvoAI code.
