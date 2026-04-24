#!/usr/bin/env bash
# Copy Sovereign GitHub Actions templates into .github/workflows/ (idempotent).
# Invoked during /init — see .ai/commands/init.md (Step 4).
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
cd "$ROOT"

SRC="${ROOT}/.ai/templates/github-workflows"
DEST="${ROOT}/.github/workflows"

if [[ ! -d "$SRC" ]]; then
  printf '%s\n' "create-github-workflows: missing template directory: ${SRC}" >&2
  exit 1
fi

mkdir -p "${DEST}"

count=0
for f in "${SRC}"/*; do
  [[ -f "$f" ]] || continue
  base="$(basename "$f")"
  cp -f "$f" "${DEST}/${base}"
  printf 'create-github-workflows: installed %s\n' "${DEST}/${base}"
  count=$((count + 1))
done

if [[ "$count" -eq 0 ]]; then
  printf '%s\n' "create-github-workflows: no files found in ${SRC} (add workflow templates there)." >&2
  exit 1
fi

printf 'create-github-workflows: done (%s file(s)).\n' "${count}"
