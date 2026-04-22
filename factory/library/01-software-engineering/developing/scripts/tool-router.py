#!/usr/bin/env python3
"""Canonical tool router entrypoint.

`tool_router_v2.py` contains the only active implementation.
This module exists as a compatibility shim for older imports.
"""

from tool_router_v2 import ToolRouter  # noqa: F401


if __name__ == "__main__":
    raise SystemExit(
        ".ai/scripts/tool-router.py is a compatibility shim. "
        "Run .ai/scripts/tool_router_v2.py directly for implementation details."
    )
