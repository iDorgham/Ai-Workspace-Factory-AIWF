#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
python3 "$(dirname "$0")/validate_library.py"
