#!/usr/bin/env bash
set -euo pipefail

python3 .ai/scripts/docs_quality_gate.py
python3 .ai/scripts/workspace_health.py

echo "docs-check-all: pass"
