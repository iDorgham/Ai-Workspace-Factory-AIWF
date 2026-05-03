# Generated reports

**Canonical output location** for machine-generated reports (audits, scans, exports) so the repository root stays clean.

| Artifact | Produced by |
|----------|-------------|
| `audit_report.json` | `python3 .ai/scripts/maintenance/audit.py` (run from repo root) |
| `cleanup_lists.txt` | `python3 .ai/scripts/maintenance/generate_lists.py` (after an audit exists) |
| `CANONICAL_LIBRARY_AUDIT.md` | Human-maintained summary; registries rebuilt via `python3 factory/scripts/analytics/rebuild_canonical_registries.py` |

**Factory library merge output** (default paths under `factory/library/reports/`, not this folder unless relocated):

| Artifact | Produced by |
|----------|-------------|
| `external_library_merge_report.json` / `.md` | `python3 factory/library/scripts/maintenance/external_library_sync.py` |

Orientation: [docs/CONTEXT.md](../CONTEXT.md) · Full spec: [docs/PRD.md](../PRD.md) §4.8.

Add new report types here (e.g. `similarity_scan.json`) rather than writing to the repo root.
