#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_ROOT="${1:-$REPO_ROOT/.build/anthropic-export}"
TARGET_SKILL_DIR="$OUTPUT_ROOT/skills/voice-ai-integration"

rm -rf "$TARGET_SKILL_DIR"
mkdir -p "$(dirname "$TARGET_SKILL_DIR")"

rsync -a --delete "$REPO_ROOT/skills/agora/" "$TARGET_SKILL_DIR/"

# Rename the exported skill to match the anthropics/skills contribution name.
perl -0pi -e \
  's/^name:\s*agora$/name: voice-ai-integration/m;
   s/^# Agora \(agora\.io\)$/# Voice AI Integration (Agora)/m' \
  "$TARGET_SKILL_DIR/SKILL.md"

# Keep nested skill names unique in the destination repo as well.
perl -0pi -e \
  's/^name:\s*agora-intake$/name: voice-ai-integration-intake/m;
   s/^# Agora Intake — Product Routing & Needs Analysis$/# Voice AI Integration Intake — Product Routing & Needs Analysis/m;
   s/skills\/agora\/SKILL\.md/skills\/voice-ai-integration\/SKILL.md/g' \
  "$TARGET_SKILL_DIR/intake/SKILL.md"

cat > "$TARGET_SKILL_DIR/README.md" <<'EOF'
# voice-ai-integration

This directory is generated from `AgoraIO/skills`.

- Source skill: `skills/agora/`
- Exported name for anthropics/skills: `voice-ai-integration`

Do not edit files in this directory manually in the fork. Update the source repository and rerun the sync workflow instead.
EOF

echo "Exported anthropics/skills bundle to: $TARGET_SKILL_DIR"
