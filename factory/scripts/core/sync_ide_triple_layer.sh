#!/usr/bin/env bash
# Sync command docs and IDE rules across .ai ↔ .cursor ↔ .antigravity (AIWF).
# Usage: bash factory/scripts/core/sync_ide_triple_layer.sh [--with-agents] [--with-subagents]
# Run from repository root (or any cwd — script locates root).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
WITH_AGENTS=0
WITH_SUBAGENTS=0
for arg in "$@"; do
  case "$arg" in
    --with-agents) WITH_AGENTS=1 ;;
    --with-subagents) WITH_SUBAGENTS=1 ;;
  esac
done

AI_CMD="${ROOT}/.ai/commands"
CR_CMD="${ROOT}/.cursor/commands"
AG_CMD="${ROOT}/.antigravity/commands"
CR_RULES="${ROOT}/.cursor/rules"
AG_RULES="${ROOT}/.antigravity/rules"
AI_RULES="${ROOT}/.ai/rules"
CR_HOOKS="${ROOT}/.cursor/hooks"
AG_HOOKS="${ROOT}/.antigravity/hooks"
AI_HOOKS="${ROOT}/.ai/hooks"

mkdir -p "$CR_CMD" "$AG_CMD" "$AI_RULES" "$AG_RULES" "$AG_HOOKS" "$AI_HOOKS"

# --- Commands: authoritative tree is .ai/commands ---
if [[ ! -d "$AI_CMD" ]]; then
  echo "error: missing ${AI_CMD}" >&2
  exit 1
fi
rsync -a "${AI_CMD}/" "${CR_CMD}/"
rsync -a "${AI_CMD}/" "${AG_CMD}/"
# Legacy duplicate command docs (pre–v4 merge). Not in `.ai/commands/` — remove so Cursor/Antigravity match canonical tree.
for legacy in "commands-multi-tool.md" "commands_multi_tool.md" "guide_humanize.md"; do
  rm -f "${CR_CMD}/${legacy}" "${AG_CMD}/${legacy}"
done

# --- Rules: authoritative UI tree is .cursor/rules (mdc + md) ---
if [[ -d "$CR_RULES" ]]; then
  rsync -a "${CR_RULES}/" "${AG_RULES}/"
  rsync -a "${CR_RULES}/" "${AI_RULES}/"
fi

# --- Hooks: copy structure only; hook machine state stays local ---
if [[ -d "$CR_HOOKS" ]]; then
  rsync -a --exclude 'state' "${CR_HOOKS}/" "${AG_HOOKS}/" 2>/dev/null || true
  rsync -a --exclude 'state' "${CR_HOOKS}/" "${AI_HOOKS}/" 2>/dev/null || true
fi

# --- Optional: agents / subagents (large; off by default) ---
if [[ "$WITH_AGENTS" -eq 1 && -d "${ROOT}/.ai/agents" ]]; then
  mkdir -p "${ROOT}/.cursor/agents" "${ROOT}/.antigravity/agents"
  rsync -a "${ROOT}/.ai/agents/" "${ROOT}/.cursor/agents/"
  rsync -a "${ROOT}/.ai/agents/" "${ROOT}/.antigravity/agents/"
fi
if [[ "$WITH_SUBAGENTS" -eq 1 && -d "${ROOT}/.ai/subagents" ]]; then
  mkdir -p "${ROOT}/.cursor/subagents" "${ROOT}/.antigravity/subagents"
  rsync -a "${ROOT}/.ai/subagents/" "${ROOT}/.cursor/subagents/"
  rsync -a "${ROOT}/.ai/subagents/" "${ROOT}/.antigravity/subagents/"
fi

if [[ -f "${ROOT}/factory/scripts/core/industrial_mirror_sync.py" ]]; then
  (cd "$ROOT" && python3 factory/scripts/core/industrial_mirror_sync.py) || true
fi

echo "sync_ide_triple_layer: OK"
echo "  commands: .ai/commands/ → .cursor/commands/ + .antigravity/commands/"
echo "  rules:    .cursor/rules/ → .antigravity/rules/ + .ai/rules/"
echo "  hooks:    .cursor/hooks/ (excluding state/) → .antigravity/hooks/ + .ai/hooks/"
if [[ "$WITH_AGENTS" -eq 1 ]]; then echo "  agents:   .ai/agents/ → .cursor + .antigravity"; fi
if [[ "$WITH_SUBAGENTS" -eq 1 ]]; then echo "  subagents:.ai/subagents/ → .cursor + .antigravity"; fi
