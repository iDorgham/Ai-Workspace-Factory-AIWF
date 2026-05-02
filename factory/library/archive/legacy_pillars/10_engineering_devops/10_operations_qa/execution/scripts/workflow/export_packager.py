"""
export_packager.py — Sovereign Export Packager
=============================================
Packages approved content into CSV exports and CMS packs.
HARD BLOCK: Refuses to export if content status ≠ "approved".

Owner: workflow-agent / export-packager sub-agent
"""

import csv
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import (  # noqa: E402
    REPO_ROOT,
    logs_dir,
    project_content_root,
    project_outputs_dir,
    templates_dir,
)

WORKSPACE_ROOT = REPO_ROOT
OUTPUTS_DIR = project_outputs_dir()
CSV_SCHEMA_PATH = templates_dir() / "csv-schemas" / "content-export.json"
QUALITY_REPORT_PATH = logs_dir() / "quality-report.json"
WORKFLOW_LOG = logs_dir() / "workflow.jsonl"


def load_csv_schema() -> dict:
    if CSV_SCHEMA_PATH.exists():
        with open(CSV_SCHEMA_PATH) as f:
            return json.load(f)
    return {"schema": {}}


def get_approved_content() -> list[dict]:
    """Get all approved Markdown files from content/."""
    content_dir = project_content_root()
    approved = []

    for md_file in content_dir.rglob("*.md"):
        if "_references" in str(md_file):
            continue
        content = md_file.read_text(encoding="utf-8")
        if 'status: "approved"' in content or "status: 'approved'" in content:
            metadata = extract_frontmatter(content)
            metadata["_file_path"] = md_file
            metadata["_content"] = content
            approved.append(metadata)

    return approved


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter as a flat dict."""
    fm_match = re.search(r"^---\s*([\s\S]*?)\s*---", content)
    if not fm_match:
        return {}

    fm = fm_match.group(1)
    result = {}

    for line in fm.splitlines():
        if ":" in line and not line.strip().startswith("-"):
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"\'')

    return result


def check_export_eligibility() -> dict:
    """Check if export can proceed: approved content + quality report."""
    approved = get_approved_content()

    if not approved:
        return {
            "eligible": False,
            "reason": "No approved content found. Run /review → /approve first.",
        }

    if not QUALITY_REPORT_PATH.exists():
        return {
            "eligible": False,
            "reason": "No quality report found. Run /review first.",
        }

    with open(QUALITY_REPORT_PATH) as f:
        report = json.load(f)

    if not report.get("overall_pass"):
        return {
            "eligible": False,
            "reason": "Quality gates have not all passed. Run /review, fix violations, then /approve.",
        }

    return {"eligible": True, "approved_files": approved}


def build_csv_row(metadata: dict, schema: dict) -> dict:
    """Build a CSV row from content metadata against the schema."""
    row = {}
    schema_fields = schema.get("schema", {})

    for field, rules in schema_fields.items():
        value = metadata.get(field, "")

        # Apply defaults for missing optional fields
        if not value and not rules.get("required"):
            if field == "cms_target":
                value = "custom"
            elif field == "version":
                value = "1"

        row[field] = value

    return row


def export_csv(approved_files: list[dict]) -> Path:
    """Generate CSV export from approved content."""
    schema = load_csv_schema()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    csv_dir = OUTPUTS_DIR / "csv-exports"
    csv_dir.mkdir(parents=True, exist_ok=True)
    csv_path = csv_dir / f"sovereign-content-export-{timestamp}.csv"

    if not approved_files:
        return csv_path

    fieldnames = list(schema.get("schema", {}).keys()) or list(approved_files[0].keys())

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for meta in approved_files:
            row = build_csv_row(meta, schema)
            writer.writerow(row)

    return csv_path


def build_cms_pack(approved_files: list[dict]) -> Path:
    """Package approved Markdown + metadata into a ZIP for CMS upload."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    cms_dir = OUTPUTS_DIR / "cms-packs"
    cms_dir.mkdir(parents=True, exist_ok=True)
    pack_path = cms_dir / f"sovereign-cms-pack-{timestamp}.zip"

    with zipfile.ZipFile(pack_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for meta in approved_files:
            file_path = meta.get("_file_path")
            if file_path and Path(file_path).exists():
                arcname = Path(file_path).relative_to(WORKSPACE_ROOT)
                zf.write(file_path, arcname)

        # Include quality report
        if QUALITY_REPORT_PATH.exists():
            zf.write(QUALITY_REPORT_PATH, "quality-report.json")

        # Include export manifest
        manifest = {
            "export_timestamp": timestamp,
            "total_files": len(approved_files),
            "files": [meta.get("slug", "unknown") for meta in approved_files],
            "workspace_version": "3.2.0",
        }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))

    return pack_path


def run_export() -> dict:
    """Main export function: validate eligibility, generate CSV and CMS pack."""
    eligibility = check_export_eligibility()

    if not eligibility["eligible"]:
        return {
            "status": "blocked",
            "error": eligibility["reason"],
        }

    approved_files = eligibility["approved_files"]

    # Generate outputs
    csv_path = export_csv(approved_files)
    cms_pack_path = build_cms_pack(approved_files)

    result = {
        "status": "success",
        "files_exported": len(approved_files),
        "csv_export": str(csv_path.relative_to(WORKSPACE_ROOT)),
        "cms_pack": str(cms_pack_path.relative_to(WORKSPACE_ROOT)),
        "exported_at": datetime.now(timezone.utc).isoformat(),
    }

    log_export(len(approved_files), str(csv_path.name), str(cms_pack_path.name))
    return result


def log_export(file_count: int, csv_name: str, pack_name: str) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "export_completed",
        "files_exported": file_count,
        "csv": csv_name,
        "cms_pack": pack_name,
    }
    WORKFLOW_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(WORKFLOW_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
