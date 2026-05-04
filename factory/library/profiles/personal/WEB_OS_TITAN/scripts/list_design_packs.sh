#!/usr/bin/env bash
# List every design pack `design.md` under the factory design catalog (repo-root relative).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# WEB_OS_TITAN/scripts → repo root (6 parents: scripts→template→personal→profiles→library→factory→root)
ROOT="$(cd "$HERE/../../../../../.." && pwd)"
DESIGN_ROOT="$ROOT/factory/library/templates/design"
if [[ ! -d "$DESIGN_ROOT" ]]; then
  echo "Missing: $DESIGN_ROOT" >&2
  exit 1
fi
find "$DESIGN_ROOT" -path "*/design.md" -type f | LC_ALL=C sort
