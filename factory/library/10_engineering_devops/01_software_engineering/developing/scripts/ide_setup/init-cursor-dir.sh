#!/usr/bin/env bash
# Create a minimal .cursor/ layout for Cursor IDE (no Continual Learning files — see CURSOR_IDE.md).
# Run from /init — durable memory stays in .ai/memory/ per Sovereign convention.
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"

CUR_DIR="${ROOT}/.cursor"
TX_DIR="${CUR_DIR}/agent-transcripts"

mkdir -p "$TX_DIR"

cat >"${CUR_DIR}/README.md" <<'EOF'
# Cursor (project)

Created by **`/init`** via `scripts/cursor/init-cursor-dir.sh`.

- **Durable workspace memory:** `.ai/memory/` — not this folder.
- **Continual Learning** (`hooks/state/continual-learning*.json`): only if you install that Cursor plugin — see `docs/workspace/guides/CURSOR_IDE.md` to disable it.
- **Rules:** root `.cursorrules` and optional `.cursor/rules/*.mdc`

Full guide: `docs/workspace/guides/CURSOR_IDE.md`
EOF

printf '%s\n' "→ Cursor project folder ready: ${CUR_DIR}"
printf '%s\n' "  See docs/workspace/guides/CURSOR_IDE.md"
