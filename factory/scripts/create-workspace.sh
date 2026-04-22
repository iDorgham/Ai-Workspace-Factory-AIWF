#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"

echo "Workspace Factory intake"
python3 "$ROOT/scripts/intake.py"

read -r -p "Enter workspace slug to compose: " CLIENT
if [[ -z "$CLIENT" ]]; then
  echo "Client slug is required"
  exit 1
fi

python3 "$ROOT/scripts/compose.py" "$CLIENT"
python3 "$ROOT/scripts/validate.py" "$CLIENT"
echo "Workspace created at $REPO_ROOT/workspaces/$CLIENT"
