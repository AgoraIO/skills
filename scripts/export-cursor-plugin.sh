#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_ROOT="$REPO_ROOT/agora"

mkdir -p "$PLUGIN_ROOT/skills"
rm -rf "$PLUGIN_ROOT/skills/agora"
rsync -a "$REPO_ROOT/skills/agora/" "$PLUGIN_ROOT/skills/agora/"
cp "$REPO_ROOT/LICENSE" "$PLUGIN_ROOT/LICENSE"

echo "Synced Cursor plugin skill bundle into: $PLUGIN_ROOT"
