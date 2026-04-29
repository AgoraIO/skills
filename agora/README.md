# Agora Cursor Plugin

Official Cursor plugin wrapper for the Agora skills repository.

## Included

- `skills/agora/` — the Agora skill pack for Conversational AI, RTC, RTM, Cloud Recording, token generation, and Agora CLI workflows
- `mcp.json` — remote MCP configuration for `https://mcp.agora.io`

## Source Of Truth

The canonical skill content lives in the repository root under `skills/agora/`.

When the source skill changes, resync this plugin wrapper with:

```bash
bash scripts/export-cursor-plugin.sh
```
