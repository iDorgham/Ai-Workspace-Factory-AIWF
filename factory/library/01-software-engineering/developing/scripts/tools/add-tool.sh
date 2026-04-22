#!/usr/bin/env bash
# Activate an AI coding tool or IDE integration in this workspace.
# Copies config files from .ai/support/<tool>/ to the locations each tool expects.
#
# Usage:   bash scripts/tools/add-tool.sh <tool-name>
# Example: bash scripts/tools/add-tool.sh windsurf
#
# Tools:  codex  vscode  github  windsurf  gemini  qwen
#         opencode  kilocode  copilot  amazonq  continue
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
SUPPORT="${ROOT}/.ai/support"

TOOLS="codex vscode github windsurf gemini qwen opencode kilocode copilot amazonq continue"

tool="${1:-}"

if [[ -z "$tool" ]]; then
  printf '\n'
  printf '%s\n' "Usage: bash scripts/tools/add-tool.sh <tool-name>"
  printf '\n'
  printf '%s\n' "Available tools:"
  printf '%s\n' "  codex      OpenAI Codex          (CODEX.md  AGENTS.md  .codex/)"
  printf '%s\n' "  vscode     VS Code / Cursor tasks (.vscode/)"
  printf '%s\n' "  github     GitHub Actions CI/CD   (.github/workflows/)"
  printf '%s\n' "  windsurf   Windsurf IDE           (.windsurfrules)"
  printf '%s\n' "  gemini     Gemini CLI             (GEMINI.md)"
  printf '%s\n' "  qwen       Qwen CLI               (QWEN.md  .qwen/)"
  printf '%s\n' "  opencode   OpenCode               (.opencode/)"
  printf '%s\n' "  kilocode   Kilo Code              (.kilocode/)"
  printf '%s\n' "  copilot    GitHub Copilot         (.github/copilot-instructions.md)"
  printf '%s\n' "  amazonq    Amazon Q Developer     (.amazonq/)"
  printf '%s\n' "  continue   Continue.dev           (.continue/)"
  printf '\n'
  printf '%s\n' "See all: bash scripts/tools/list-tools.sh"
  printf '\n'
  exit 1
fi

cp_file() {
  local src="${SUPPORT}/${1}"
  local dst="${ROOT}/${2}"
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  printf '  ✓ %s\n' "$2"
}

cp_dir() {
  local src="${SUPPORT}/${1}"
  local dst="${ROOT}/${2}"
  mkdir -p "$dst"
  cp -r "$src/." "$dst/"
  printf '  ✓ %s/\n' "$2"
}

printf '\n'
printf 'Activating: %s\n' "$tool"

case "$tool" in
  codex)
    cp_file "codex/CODEX.md"          "CODEX.md"
    cp_file "codex/AGENTS.md"         "AGENTS.md"
    cp_file "codex/.codex/config.toml" ".codex/config.toml"
    ;;
  vscode)
    cp_file "vscode/tasks.json"      ".vscode/tasks.json"
    cp_file "vscode/extensions.json" ".vscode/extensions.json"
    ;;
  github)
    cp_dir "github/workflows" ".github/workflows"
    ;;
  windsurf)
    cp_file "windsurf/.windsurfrules" ".windsurfrules"
    ;;
  gemini)
    cp_file "gemini/GEMINI.md" "GEMINI.md"
    ;;
  qwen)
    cp_file "qwen/QWEN.md"           "QWEN.md"
    cp_file "qwen/.qwen/settings.json" ".qwen/settings.json"
    ;;
  opencode)
    cp_file "opencode/AGENTS.md" ".opencode/AGENTS.md"
    ;;
  kilocode)
    cp_file "kilocode/rules/main.md" ".kilocode/rules/main.md"
    ;;
  copilot)
    cp_file "copilot/copilot-instructions.md" ".github/copilot-instructions.md"
    ;;
  amazonq)
    cp_file "amazonq/rules/sovereign-workspace.md" ".amazonq/rules/sovereign-workspace.md"
    ;;
  continue)
    cp_file "continue/rules/01-sovereign-workspace.md" ".continue/rules/01-sovereign-workspace.md"
    ;;
  claude|cursor|antigravity)
    printf '  "%s" is a primary tool — always active, nothing to install.\n' "$tool"
    exit 0
    ;;
  *)
    printf 'Unknown tool: "%s"\n' "$tool"
    printf 'Run without arguments to see the list.\n'
    exit 1
    ;;
esac

printf '\n'
printf '"%s" is now active.\n' "$tool"
printf 'See all active tools: bash scripts/tools/list-tools.sh\n'
printf '\n'
