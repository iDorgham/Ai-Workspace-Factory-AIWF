#!/usr/bin/env bash
# Rotate runtime-logs: total >500KB or files >30d → .ai/plans/archive/runtime-logs/
# Portable macOS/Linux (stat mtime).
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[[ -n "$ROOT" ]] || exit 0
SRC="$ROOT/.ai/plans/active/audit/runtime-logs"
DST="$ROOT/.ai/plans/archive/runtime-logs"
mkdir -p "$DST"

if [[ ! -d "$SRC" ]]; then
  exit 0
fi

mtime() {
  if stat -f%m "$1" >/dev/null 2>&1; then
    stat -f%m "$1"
  else
    stat -c%Y "$1"
  fi
}

now="$(date +%s)"
cutoff=$((now - 30 * 86400))

shopt -s nullglob
for f in "$SRC"/*.md; do
  [[ "$(basename "$f")" == "README.md" ]] && continue
  [[ -f "$f" ]] || continue
  mt="$(mtime "$f")"
  if (( mt < cutoff )); then
    mv "$f" "$DST/"
  fi
done

cap_kb=500
while true; do
  size_kb="$(du -sk "$SRC" 2>/dev/null | awk '{print $1}')"
  [[ -z "${size_kb:-}" ]] && break
  if (( size_kb <= cap_kb )); then
    break
  fi
  oldest=""
  oldest_t=9999999999
  for f in "$SRC"/*.md; do
    [[ "$(basename "$f")" == "README.md" ]] && continue
    [[ -f "$f" ]] || continue
    mt="$(mtime "$f")"
    if (( mt < oldest_t )); then
      oldest_t="$mt"
      oldest="$f"
    fi
  done
  [[ -z "${oldest:-}" ]] && break
  mv "$oldest" "$DST/"
done

shopt -u nullglob
exit 0
