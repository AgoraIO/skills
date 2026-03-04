# Agora Doc MCP Tools

Internal guide for the model. Describes how to use the Agora Doc MCP server
to fetch up-to-date documentation during skill execution.

**MCP endpoint:** `https://doc-mcp.shengwang.cn/mcp`

## Tools

| Tool | Input | Returns | When to use |
|------|-------|---------|-------------|
| `get-doc-content` | `{"uri": "docs://..."}` | Full markdown content | Read a specific doc (preferred) |
| `search-docs` | `{"query": "keyword"}` | List of matching doc URIs | Find docs when URI is unknown |
| `list-docs` | `{"category": "...", "limit": 20}` | All docs in a category | Browse available docs |

## Preferred Approach: Direct URI

When the doc URI is known, call `get-doc-content` directly — no search needed.

> **After fetching quick-start docs:** use the fetched content for API structure and field names only. Do NOT copy sample code verbatim — quick-start examples typically hardcode credentials and omit production requirements. Apply the gotchas and rules in `references/conversational-ai/README.md` to any generated code (token auth, uid types, agent name uniqueness, credential env vars).

```text
get-doc-content {"uri": "docs://default/convoai/restful/get-started/quick-start"}
```

## Known Doc URIs

| Product | Topic | URI |
|---------|-------|-----|
| ConvoAI | Quick Start (Python/curl) | `docs://default/convoai/restful/get-started/quick-start` |
| ConvoAI | Quick Start (Go) | `docs://default/convoai/restful/get-started/quick-start-go` |
| ConvoAI | Quick Start (Java) | `docs://default/convoai/restful/get-started/quick-start-java` |
| RTC | Quick Start (Web) | `docs://default/rtc/javascript/get-started/quick-start` |
| RTC | Quick Start (Android) | `docs://default/rtc/android/get-started/quick-start` |
| RTC | Quick Start (iOS) | `docs://default/rtc/ios/get-started/quick-start` |
| RTM | Quick Start (Web) | `docs://default/rtm2/javascript/get-started/quick-start` |
| Cloud Recording | Quick Start | `docs://default/cloud-recording/restful/get-started/quick-start` |

## Fallback: Search Then Read

When the URI is unknown, search first:

```text
Step 1: search-docs {"query": "convoai <topic>"}
        → returns [{uri: "docs://...", text: "..."}, ...]

Step 2: get-doc-content {"uri": "docs://..."}
        → returns full doc content
```

## When to Call MCP

**Always call for:**

- ConvoAI API field details, request/response schemas, vendor configurations (TTS, ASR)
- Error codes and their meanings (ConvoAI, Cloud Recording)
- Any content that changes with documentation updates

**Do NOT call for:**

- RTC initialization, track management, event registration — stable, in `references/rtc/`
- RTM messaging patterns — stable, in `references/rtm/`
- Token generation patterns — stable, in `references/server/`
- ConvoAI gotchas and critical rules — behavioral knowledge, inline in `references/conversational-ai/README.md`

## Freeze-Forever Content

The "When to Call MCP" section above is the categorization table. Rule: if content changes with doc updates or vendor releases, call MCP. If it's a stable SDK pattern, use inline skill content.

## AI Assistant MCP Support

MCP tool calls require an MCP-compatible AI assistant with the Agora Doc MCP server
configured at `https://doc-mcp.shengwang.cn/mcp`.

- **Claude Code**: MCP supported. Install the Agora Doc MCP server per official instructions.
- **Cursor, Windsurf, GitHub Copilot**: MCP support varies by version. Check your tool's documentation.

When MCP is not available: use the graceful degradation paths defined in each product skill.
For ConvoAI: see the MCP Fallback section in `references/conversational-ai/README.md`.
For all other products: inline code in the skill files is the primary source — no degradation needed.
