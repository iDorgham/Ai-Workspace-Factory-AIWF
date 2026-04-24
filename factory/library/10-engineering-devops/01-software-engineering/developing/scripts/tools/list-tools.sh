#!/usr/bin/env bash
# Show which AI tools and IDE integrations are active in this workspace.
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"

is_active() {
  # Returns 0 (true) if ALL given paths exist at root
  for path in "$@"; do
    [[ -e "${ROOT}/${path}" ]] || return 1
  done
  return 0
}

row() {
  local name="$1" label="$2"; shift 2
  if is_active "$@"; then
    printf '  ✓  %-12s  %s\n' "$name" "$label"
  else
    printf '  ○  %-12s  %s\n' "$name" "$label"
  fi
}

printf '\n'
printf '%s\n' "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf '%s\n' "  Sovereign — AI Tool Support   (✓ active  ○ available)"
printf '%s\n' "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf '\n'

printf '%s\n' "Primary (always active — cannot be removed):"
printf '  ✓  %-12s  %s\n' "claude"      "Claude Code  →  CLAUDE.md  .claude/"
printf '  ✓  %-12s  %s\n' "cursor"      "Cursor IDE   →  .cursorrules"
printf '  ✓  %-12s  %s\n' "antigravity" "Antigravity  →  .antigravity/"
printf '\n'

printf '%s\n' "Optional — add or remove anytime:"
row "codex"    "OpenAI Codex           CODEX.md  AGENTS.md  .codex/"     "CODEX.md" "AGENTS.md" ".codex"
row "vscode"   "VS Code tasks / Cursor .vscode/"                          ".vscode/tasks.json" ".vscode/extensions.json"
row "github"   "GitHub Actions CI/CD   .github/workflows/"               ".github/workflows"
row "windsurf" "Windsurf IDE           .windsurfrules"                    ".windsurfrules"
row "gemini"   "Gemini CLI             GEMINI.md"                         "GEMINI.md"
row "qwen"     "Qwen CLI               QWEN.md  .qwen/"                   "QWEN.md" ".qwen/settings.json"
row "opencode" "OpenCode               .opencode/"                        ".opencode/AGENTS.md"
row "kilocode" "Kilo Code              .kilocode/"                        ".kilocode/rules/main.md"
row "copilot"  "GitHub Copilot         .github/copilot-instructions.md"   ".github/copilot-instructions.md"
row "amazonq"  "Amazon Q Developer     .amazonq/"                         ".amazonq/rules/sovereign-workspace.md"
row "continue" "Continue.dev           .continue/"                        ".continue/rules/01-sovereign-workspace.md"
printf '\n'

printf '%s\n' "Commands:"
printf '%s\n' "  bash scripts/tools/add-tool.sh <name>      Activate"
printf '%s\n' "  bash scripts/tools/remove-tool.sh <name>   Deactivate"
printf '%s\n' "  All configs stored in: .ai/support/"
printf '\n'
