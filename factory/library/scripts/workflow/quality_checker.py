"""
quality_checker.py — Sovereign Parallel Quality Gate Runner
===========================================================
Runs all 5 quality gates IN PARALLEL for the /review command.
Gates: SEO (≥85%), Brand Voice (≥92%), Readability (≥65), Image SEO (100%), Originality (≤15%)

Owner: workflow-agent / quality-checker sub-agent
Writes: .ai/logs/quality-report.json (authoritative owner)
"""

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, logs_dir, project_content_root, project_scraped_dir, scripts_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
_sd = scripts_dir()
sys.path.insert(0, str(_sd / "seo"))
sys.path.insert(0, str(_sd / "brand"))

QUALITY_REPORT_PATH = logs_dir() / "quality-report.json"
WORKFLOW_LOG = logs_dir() / "workflow.jsonl"

# Gate thresholds
THRESHOLDS = {
    "seo": 0.85,
    "brand_voice": 0.92,
    "readability": 65.0,
    "image_seo": 1.00,
    "originality": 0.15,   # MAXIMUM (lower is better)
}


def get_staged_content() -> list[dict]:
    """Get all draft Markdown files from content/ with their metadata."""
    content_dir = project_content_root()
    staged = []

    for md_file in content_dir.rglob("*.md"):
        if "_references" in str(md_file):
            continue
        content = md_file.read_text(encoding="utf-8")
        # Check if status is draft (eligible for review)
        if "status: \"draft\"" in content or "status: 'draft'" in content:
            staged.append({
                "file_path": md_file,
                "relative_path": str(md_file.relative_to(WORKSPACE_ROOT)),
                "content": content,
            })

    return staged


# ── Individual Gate Runners ────────────────────────────────────────────────────

def run_seo_gate(staged_files: list[dict]) -> dict:
    """SEO gate: check all staged files, return worst-case score."""
    try:
        from seo_optimizer import audit_file
        scores = []
        violations = []
        for item in staged_files:
            result = audit_file(item["file_path"])
            scores.append(result.get("seo_score", 0))
            violations.extend(result.get("violations", [])[:3])

        score = min(scores) if scores else 0.0
        return {
            "gate": "seo",
            "score": round(score, 4),
            "passed": score >= THRESHOLDS["seo"],
            "threshold": THRESHOLDS["seo"],
            "violations": violations[:5],
        }
    except Exception as e:
        return {"gate": "seo", "score": 0.0, "passed": False, "error": str(e)}


def run_brand_voice_gate(staged_files: list[dict]) -> dict:
    """Brand voice gate: check all staged files for tone compliance."""
    try:
        from voice_validator import score_content
        scores = []
        violations = []
        for item in staged_files:
            result = score_content(item["content"], item["relative_path"])
            scores.append(result.get("compliance_score", 0))
            violations.extend(result.get("violations", [])[:2])

        score = min(scores) if scores else 0.0
        return {
            "gate": "brand_voice",
            "score": round(score, 4),
            "passed": score >= THRESHOLDS["brand_voice"],
            "threshold": THRESHOLDS["brand_voice"],
            "violations": violations[:5],
        }
    except Exception as e:
        return {"gate": "brand_voice", "score": 0.0, "passed": False, "error": str(e)}


def run_readability_gate(staged_files: list[dict]) -> dict:
    """Readability gate: Flesch-Kincaid ≥ 65 for all files."""
    try:
        from seo_optimizer import flesch_kincaid_score
        scores = []
        violations = []
        for item in staged_files:
            body = re.sub(r"^---[\s\S]*?---\n", "", item["content"], count=1)
            score = flesch_kincaid_score(body)
            scores.append(score)
            if score < THRESHOLDS["readability"]:
                violations.append({
                    "file": item["relative_path"],
                    "score": score,
                    "message": f"Readability score {score} is below {THRESHOLDS['readability']} threshold.",
                })

        min_score = min(scores) if scores else 0.0
        return {
            "gate": "readability",
            "score": round(min_score, 1),
            "passed": min_score >= THRESHOLDS["readability"],
            "threshold": THRESHOLDS["readability"],
            "violations": violations[:5],
        }
    except Exception as e:
        return {"gate": "readability", "score": 0.0, "passed": False, "error": str(e)}


def run_image_seo_gate(staged_files: list[dict]) -> dict:
    """Image SEO gate: all images must have alt-text and WebP format."""
    img_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    total_images = 0
    images_with_alt = 0
    images_webp = 0
    violations = []

    for item in staged_files:
        matches = img_pattern.findall(item["content"])
        for alt, src in matches:
            total_images += 1
            if alt.strip():
                images_with_alt += 1
            else:
                violations.append({
                    "file": item["relative_path"],
                    "src": src,
                    "message": "Image missing alt text.",
                })
            if src.lower().endswith(".webp"):
                images_webp += 1
            else:
                violations.append({
                    "file": item["relative_path"],
                    "src": src,
                    "message": f"Image not in WebP format: {src.split('/')[-1]}",
                })

    if total_images == 0:
        # No images found — pass this gate (images may not be required)
        return {
            "gate": "image_seo",
            "score": 1.0,
            "passed": True,
            "threshold": THRESHOLDS["image_seo"],
            "total_images": 0,
            "note": "No images found in staged content.",
            "violations": [],
        }

    coverage = images_with_alt / total_images
    webp_rate = images_webp / total_images
    combined = (coverage + webp_rate) / 2

    return {
        "gate": "image_seo",
        "score": round(combined, 4),
        "passed": combined >= THRESHOLDS["image_seo"],
        "threshold": THRESHOLDS["image_seo"],
        "total_images": total_images,
        "alt_text_coverage": round(coverage, 4),
        "webp_coverage": round(webp_rate, 4),
        "violations": violations[:5],
    }


def run_originality_gate(staged_files: list[dict]) -> dict:
    """
    Originality gate: semantic similarity ≤ 15% vs scraped competitor content.
    Simplified: checks for verbatim phrase overlap with scraped content.
    """
    scraped_dir = project_scraped_dir()
    scraped_texts = []

    # Load competitor scraped content (summaries only — first 300 chars each)
    for md_file in scraped_dir.rglob("scraped/content/**/*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")[:300]
            scraped_texts.append(content.lower())
        except Exception:
            pass

    if not scraped_texts:
        return {
            "gate": "originality",
            "score": 0.0,  # 0% similarity = fully original
            "passed": True,
            "threshold": THRESHOLDS["originality"],
            "note": "No competitor content to compare against — originality assumed.",
            "violations": [],
        }

    max_similarity = 0.0
    violations = []

    for item in staged_files:
        body = re.sub(r"^---[\s\S]*?---\n", "", item["content"], count=1).lower()
        words = body.split()

        # Check 5-gram overlap with scraped content
        if len(words) < 5:
            continue

        matched_grams = 0
        total_grams = len(words) - 4

        for i in range(total_grams):
            gram = " ".join(words[i:i+5])
            if any(gram in scraped for scraped in scraped_texts):
                matched_grams += 1

        similarity = matched_grams / total_grams if total_grams > 0 else 0.0
        if similarity > max_similarity:
            max_similarity = similarity

        if similarity > THRESHOLDS["originality"]:
            violations.append({
                "file": item["relative_path"],
                "similarity": round(similarity, 4),
                "message": f"Content similarity {similarity:.0%} exceeds {THRESHOLDS['originality']:.0%} threshold.",
            })

    return {
        "gate": "originality",
        "score": round(max_similarity, 4),
        "passed": max_similarity <= THRESHOLDS["originality"],
        "threshold": THRESHOLDS["originality"],
        "note": "Lower score = more original.",
        "violations": violations[:3],
    }


# ── Main Review Runner ────────────────────────────────────────────────────────

def run_review() -> dict:
    """
    Run all 5 quality gates IN PARALLEL.
    Returns comprehensive quality report.
    """
    staged = get_staged_content()

    if not staged:
        return {
            "status": "no_content",
            "error": "No staged draft content found in content/. Run /create first.",
            "overall_pass": False,
        }

    gate_functions = [
        run_seo_gate,
        run_brand_voice_gate,
        run_readability_gate,
        run_image_seo_gate,
        run_originality_gate,
    ]

    gate_results = {}
    start_time = datetime.now(timezone.utc)

    # Run all gates in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fn, staged): fn.__name__ for fn in gate_functions}
        for future in as_completed(futures):
            result = future.result()
            gate_name = result["gate"]
            gate_results[gate_name] = result

    overall_pass = all(r.get("passed", False) for r in gate_results.values())
    elapsed_ms = int((datetime.now(timezone.utc) - start_time).total_seconds() * 1000)

    report = {
        "reviewed_at": start_time.isoformat(),
        "duration_ms": elapsed_ms,
        "files_reviewed": [item["relative_path"] for item in staged],
        "total_files": len(staged),
        "gates": gate_results,
        "overall_pass": overall_pass,
        "summary": build_summary(gate_results, overall_pass),
    }

    # Write report (authoritative — only quality-checker writes this)
    write_report(report)

    # Log
    log_review(overall_pass, elapsed_ms, len(staged))

    return report


def build_summary(gate_results: dict, overall_pass: bool) -> str:
    """Build human-readable review summary."""
    if overall_pass:
        return "✅ All quality gates passed. Ready for /approve."

    failed = [r for r in gate_results.values() if not r.get("passed")]
    failed_names = [f["gate"].replace("_", " ").title() for f in failed]
    lines = [f"❌ {len(failed)} gate(s) failed: {', '.join(failed_names)}"]

    for gate in failed:
        name = gate["gate"].replace("_", " ").title()
        if "score" in gate:
            score = gate["score"]
            threshold = gate["threshold"]
            if gate["gate"] == "originality":
                lines.append(f"  • {name}: {score:.0%} similarity (max: {threshold:.0%})")
            elif gate["gate"] == "readability":
                lines.append(f"  • {name}: score {score} (min: {threshold})")
            else:
                lines.append(f"  • {name}: {score:.0%} (min: {threshold:.0%})")
        for v in gate.get("violations", [])[:2]:
            lines.append(f"    → {v.get('message', '')}")

    return "\n".join(lines)


def write_report(report: dict) -> None:
    """Write quality report. Backs up previous report with timestamp."""
    QUALITY_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Back up existing report
    if QUALITY_REPORT_PATH.exists():
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup = QUALITY_REPORT_PATH.parent / f"quality-report-{timestamp}.json"
        QUALITY_REPORT_PATH.rename(backup)

    with open(QUALITY_REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)


def log_review(overall_pass: bool, duration_ms: int, file_count: int) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "review_completed",
        "overall_pass": overall_pass,
        "duration_ms": duration_ms,
        "files_reviewed": file_count,
    }
    with open(WORKFLOW_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    print("Running quality review...")
    result = run_review()
    print(result.get("summary", "Review complete."))
