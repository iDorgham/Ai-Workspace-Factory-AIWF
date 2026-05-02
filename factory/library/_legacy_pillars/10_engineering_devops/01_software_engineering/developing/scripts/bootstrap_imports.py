"""Insert `.ai/scripts` on sys.path so `paths` resolves from nested packages."""

from __future__ import annotations

import sys
from pathlib import Path


def install() -> Path:
    here = Path(__file__).resolve().parent
    s = str(here)
    if s not in sys.path:
        sys.path.insert(0, s)
    return here
