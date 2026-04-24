#!/usr/bin/env bash
# Enable one or more optional AI tool integrations in a single terminal command.
# Wraps add-tool.sh for each name. Works before or after /init.
#
# Usage:
#   bash scripts/tools/enable-ai-tools.sh
#   bash scripts/tools/enable-ai-tools.sh --all
#   bash scripts/tools/enable-ai-tools.sh codex gemini vscode
#
# Primary tools (claude, cursor, antigravity) are always active — add-tool.sh skips them.
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADD_TOOL="${_GALERIA_HERE}/add-tool.sh"

# Keep in sync with add-tool.sh TOOLS=
ALL_OPTIONAL_TOOLS=(
  codex
  vscode
  github
  windsurf
  gemini
  qwen
  opencode
  kilocode
  copilot
  amazonq
  continue
)

usage() {
  printf '\n'
  printf '%s\n' "Usage: bash scripts/tools/enable-ai-tools.sh [--all | <tool> ...]"
  printf '\n'
  printf '%s\n' "  --all              Enable every optional AI tool integration"
  printf '%s\n' "  <tool> ...         Enable only the named tools (space-separated)"
  printf '\n'
  printf '%s\n' "Optional tool names:"
  printf '%s\n' "  codex  vscode  github  windsurf  gemini  qwen"
  printf '%s\n' "  opencode  kilocode  copilot  amazonq  continue"
  printf '\n'
  printf '%s\n' "See status:  bash scripts/tools/list-tools.sh"
  printf '%s\n' "Add one:     bash scripts/tools/add-tool.sh <name>"
  printf '\n'
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

if [[ "$1" == "--all" ]]; then
  if [[ $# -gt 1 ]]; then
    printf '%s\n' "error: use --all alone, or pass tool names without --all" >&2
    exit 1
  fi
  printf '\n'
  printf '%s\n' "Enabling all optional AI tool integrations…"
  printf '\n'
  for t in "${ALL_OPTIONAL_TOOLS[@]}"; do
    bash "$ADD_TOOL" "$t"
  done
  printf '\n'
  printf '%s\n' "Done. Verify: bash scripts/tools/list-tools.sh"
  printf '\n'
  exit 0
fi

printf '\n'
printf '%s\n' "Enabling: $*"
printf '\n'
for t in "$@"; do
  if [[ "$t" == "--all" ]]; then
    printf '%s\n' "error: --all must be the only argument" >&2
    exit 1
  fi
  bash "$ADD_TOOL" "$t"
done
printf '\n'
printf '%s\n' "Done. Verify: bash scripts/tools/list-tools.sh"
printf '\n'
