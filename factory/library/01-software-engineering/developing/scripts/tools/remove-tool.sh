#!/usr/bin/env bash
# Deactivate an AI coding tool — removes its files from the workspace root.
# Config is safely preserved in .ai/support/<tool>/ and can be re-added anytime.
#
# Usage:   bash scripts/tools/remove-tool.sh <tool-name>
# Example: bash scripts/tools/remove-tool.sh windsurf
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"

tool="${1:-}"

if [[ -z "$tool" ]]; then
  printf '\n'
  printf '%s\n' "Usage: bash scripts/tools/remove-tool.sh <tool-name>"
  printf '%s\n' "Run list-tools.sh to see what is currently active."
  printf '\n'
  exit 1
fi

gone() {
  local path="${ROOT}/${1}"
  if [[ -e "$path" ]]; then
    rm -rf "$path"
    printf '  ✓ removed %s\n' "$1"
  else
    printf '  – already absent: %s\n' "$1"
  fi
}

rmdir_if_empty() {
  local path="${ROOT}/${1}"
  if [[ -d "$path" ]] && [[ -z "$(ls -A "$path" 2>/dev/null)" ]]; then
    rmdir "$path"
  fi
}

printf '\n'
printf 'Deactivating: %s\n' "$tool"

case "$tool" in
  codex)
    gone "CODEX.md"
    gone "AGENTS.md"
    gone ".codex"
    ;;
  vscode)
    gone ".vscode/tasks.json"
    gone ".vscode/extensions.json"
    rmdir_if_empty ".vscode"
    ;;
  github)
    gone ".github/workflows"
    rmdir_if_empty ".github"
    ;;
  windsurf)
    gone ".windsurfrules"
    ;;
  gemini)
    gone "GEMINI.md"
    ;;
  qwen)
    gone "QWEN.md"
    gone ".qwen"
    ;;
  opencode)
    gone ".opencode/AGENTS.md"
    rmdir_if_empty ".opencode"
    ;;
  kilocode)
    gone ".kilocode/rules/main.md"
    rmdir_if_empty ".kilocode/rules"
    rmdir_if_empty ".kilocode"
    ;;
  copilot)
    gone ".github/copilot-instructions.md"
    rmdir_if_empty ".github"
    ;;
  amazonq)
    gone ".amazonq/rules/sovereign-workspace.md"
    rmdir_if_empty ".amazonq/rules"
    rmdir_if_empty ".amazonq"
    ;;
  continue)
    gone ".continue/rules/01-sovereign-workspace.md"
    rmdir_if_empty ".continue/rules"
    rmdir_if_empty ".continue"
    ;;
  claude|cursor|antigravity)
    printf '  "%s" is a primary tool — cannot be deactivated.\n' "$tool"
    exit 0
    ;;
  *)
    printf 'Unknown tool: "%s"\n' "$tool"
    exit 1
    ;;
esac

printf '\n'
printf '"%s" deactivated. Config is safe in .ai/support/%s/\n' "$tool" "$tool"
printf 'To re-add: bash scripts/tools/add-tool.sh %s\n' "$tool"
printf '\n'
