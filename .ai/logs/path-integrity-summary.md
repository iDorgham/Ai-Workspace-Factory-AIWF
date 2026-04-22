# Path Integrity Summary

Last run: 2026-04-20 19:33 UTC (from `audit_path_integrity.py`)

## Validation Results
- Python literal file-path references: fail (`python_broken = 1`)
- Documentation path scan: fail (`doc_broken = 211`)
- Total broken references: fail (`total_broken = 212`)
- Ignored placeholder references: `ignored_placeholders = 3207`
- Machine-readable source: `.ai/logs/path-integrity-report.json`

## Status
- Path integrity is currently not clean — see report JSON.
- Summary is regenerated after each audit (canonical logs live under `.ai/logs/`).

## Notes
- Placeholder-heavy references are intentionally ignored by scanner rules.
- Files under `.ai/logs/` are excluded from path scans so generated reports and JSONL lines do not create self-referential findings.
- Continue using `.ai/scripts/audit_path_integrity.py` before releasing structural changes.
