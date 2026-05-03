#!/usr/bin/env python3
"""
DEPRECATED — factory/profiles/ was removed in favor of industrial OS templates
under factory/shards/ and /mat materialization.

This stub remains so old automation URLs do not 404 silently.
"""

import sys


def main() -> None:
    print(
        "migrate_profiles.py is retired: use factory/shards "
        "and bash .ai/scripts/factory_materialize.sh (/mat)."
    )
    raise SystemExit(0)


if __name__ == "__main__":
    main()
