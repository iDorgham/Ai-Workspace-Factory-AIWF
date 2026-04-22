"""
seo_optimizer.py — Sovereign SEO Optimization Engine
====================================================
Runs keyword audit, heading structure validation, meta generation,
and Flesch-Kincaid readability scoring on content files.

Owner: seo-agent
Sub-agents: keyword-auditor, technical-auditor
"""

import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, logs_dir, project_content_root  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
KEYWORD_MAPS_PATH = project_content_root() / "_references" / "keyword-maps.md"
SEO_LOG = logs_dir() / "content-polish.jsonl"

# Thresholds
SEO_PASS_THRESHOLD = 0.85
READABILITY_PASS_THRESHOLD = 65
KEYWORD_DENSITY_MIN = 0.01
KEYWORD_DENSITY_MAX = 0.02


# ── Flesch-Kincaid Readability ────────────────────────────────────────────────

def count_syllables(word: str) -> int:
    """Rough syllable counter."""
    word = word.lower().strip(".,!?;:'\"")
    if len(word) <= 3:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e"):
        count -= 1
    return max(1, count)


def flesch_kincaid_score(text: str) -> float:
    """
    Calculate Flesch Reading Ease score.
    Score ≥ 65 = Plain English (target for Sovereign content).
    """
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = text.split()

    if not sentences or not words:
        return 0.0

    num_sentences = len(sentences)
    num_words = len(words)
    num_syllables = sum(count_syllables(w) for w in words)

    avg_sentence_length = num_words / num_sentences
    avg_syllables_per_word = num_syllables / num_words

    # Flesch Reading Ease formula
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    return round(max(0.0, min(100.0, score)), 1)


def suggest_simplifications(text: str) -> list[dict]:
    """Flag overly dense sentences for simplification."""
    suggestions = []
    sentences = re.split(r"[.!?]+", text)
    for i, sentence in enumerate(sentences):
        words = sentence.split()
        if len(words) > 30:
            suggestions.append({
                "sentence_index": i,
                "word_count": len(words),
                "excerpt": sentence.strip()[:100] + "...",
                "suggestion": "Consider splitting this sentence or reducing clauses.",
            })
    return suggestions[:5]  # Cap at 5 suggestions


# ── Keyword Analysis ──────────────────────────────────────────────────────────

def extract_frontmatter_keywords(content: str) -> list[str]:
    """Extract keywords from YAML frontmatter."""
    fm_match = re.search(r"^---\s*([\s\S]*?)\s*---", content)
    if not fm_match:
        return []
    fm = fm_match.group(1)
    kw_match = re.search(r"keywords:\s*\n((?:\s+-\s+.+\n?)+)", fm)
    if not kw_match:
        return []
    keywords = re.findall(r"-\s+(.+)", kw_match.group(1))
    return [k.strip().strip('"') for k in keywords]


def calculate_keyword_density(text: str, keyword: str) -> float:
    """Calculate keyword density (case-insensitive)."""
    words = text.lower().split()
    keyword_words = keyword.lower().split()
    if not words or not keyword_words:
        return 0.0

    count = 0
    kw_len = len(keyword_words)
    for i in range(len(words) - kw_len + 1):
        if words[i:i+kw_len] == keyword_words:
            count += 1

    return count / len(words)


def audit_keywords(content: str, keywords: list[str]) -> dict:
    """
    Full keyword audit: density, placement, H1 presence, meta presence.
    """
    # Strip frontmatter for body analysis
    body = re.sub(r"^---[\s\S]*?---\n", "", content, count=1)
    fm_match = re.search(r"^---\s*([\s\S]*?)\s*---", content)
    frontmatter = fm_match.group(1) if fm_match else ""

    # Extract structural elements
    h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    h1_text = h1_match.group(1).lower() if h1_match else ""
    meta_match = re.search(r"meta_description:\s*[\"'](.+?)[\"']", frontmatter)
    meta_text = meta_match.group(1).lower() if meta_match else ""
    first_100_words = " ".join(body.split()[:100]).lower()

    results = {}
    violations = []

    primary_kw = keywords[0] if keywords else ""

    for i, keyword in enumerate(keywords[:5]):  # Audit top 5 keywords
        kw_lower = keyword.lower()
        density = calculate_keyword_density(body, keyword)
        in_h1 = kw_lower in h1_text
        in_meta = kw_lower in meta_text
        in_first_100 = kw_lower in first_100_words

        density_ok = KEYWORD_DENSITY_MIN <= density <= KEYWORD_DENSITY_MAX

        kw_result = {
            "keyword": keyword,
            "density": round(density, 4),
            "density_ok": density_ok,
            "in_h1": in_h1 if i == 0 else None,  # Only check for primary keyword
            "in_meta": in_meta if i == 0 else None,
            "in_first_100_words": in_first_100 if i == 0 else None,
        }
        results[keyword] = kw_result

        # Violations
        if not density_ok and density > 0:
            violations.append({
                "keyword": keyword,
                "type": "density_out_of_range",
                "density": density,
                "message": f"'{keyword}' density is {density:.1%} (target: {KEYWORD_DENSITY_MIN:.0%}–{KEYWORD_DENSITY_MAX:.0%})",
            })
        if i == 0 and not in_h1:
            violations.append({"keyword": keyword, "type": "missing_from_h1", "message": f"Primary keyword '{keyword}' not in H1"})
        if i == 0 and not in_meta:
            violations.append({"keyword": keyword, "type": "missing_from_meta", "message": f"Primary keyword '{keyword}' not in meta description"})
        if i == 0 and not in_first_100:
            violations.append({"keyword": keyword, "type": "missing_from_opening", "message": f"Primary keyword '{keyword}' not in first 100 words"})

    return {"keyword_results": results, "violations": violations}


# ── Heading Structure ─────────────────────────────────────────────────────────

def validate_heading_structure(content: str) -> dict:
    """Validate heading hierarchy (H1→H2→H3 only, no skips)."""
    body = re.sub(r"^---[\s\S]*?---\n", "", content, count=1)
    headings = re.findall(r"^(#{1,6})\s+(.+)$", body, re.MULTILINE)

    h1_count = sum(1 for h, _ in headings if len(h) == 1)
    violations = []

    if h1_count == 0:
        violations.append({"type": "missing_h1", "message": "No H1 found. Every page needs exactly one H1."})
    elif h1_count > 1:
        violations.append({"type": "multiple_h1", "count": h1_count, "message": f"{h1_count} H1 tags found. Use exactly one."})

    # Check for skipped levels
    prev_level = 0
    for hashes, text in headings:
        level = len(hashes)
        if level > prev_level + 1 and prev_level > 0:
            violations.append({
                "type": "skipped_heading_level",
                "from": f"H{prev_level}",
                "to": f"H{level}",
                "heading": text.strip(),
                "message": f"Heading hierarchy skips from H{prev_level} to H{level}.",
            })
        prev_level = level

    return {
        "h1_count": h1_count,
        "total_headings": len(headings),
        "hierarchy_valid": len(violations) == 0,
        "violations": violations,
    }


# ── Meta Generation ───────────────────────────────────────────────────────────

def generate_meta_description(content: str, primary_keyword: str = "") -> str:
    """Generate meta description from content if missing or too short."""
    # Try to get first substantive paragraph
    body = re.sub(r"^---[\s\S]*?---\n", "", content, count=1)
    body = re.sub(r"^#{1,6}\s+.+$", "", body, flags=re.MULTILINE)  # Remove headings
    body = body.strip()

    # Find first meaningful paragraph
    paragraphs = [p.strip() for p in body.split("\n\n") if len(p.strip()) > 50]
    if not paragraphs:
        return f"Discover Sovereign's approach to {primary_keyword or 'premium interior design'}."

    first_para = paragraphs[0][:200]
    # Trim to sentence boundary
    sentence_end = max(
        first_para.rfind("."),
        first_para.rfind("?"),
    )
    if sentence_end > 120:
        meta = first_para[:sentence_end + 1]
    else:
        meta = first_para[:155]

    return meta.strip()


# ── Main SEO Audit ────────────────────────────────────────────────────────────

def audit_file(file_path: Path) -> dict:
    """
    Run full SEO audit on a single Markdown file.
    Returns comprehensive report with scores, violations, and suggested fixes.
    """
    content = file_path.read_text(encoding="utf-8")
    body = re.sub(r"^---[\s\S]*?---\n", "", content, count=1)

    keywords = extract_frontmatter_keywords(content)
    primary_keyword = keywords[0] if keywords else ""

    # Run all auditors
    readability = flesch_kincaid_score(body)
    simplifications = suggest_simplifications(body) if readability < READABILITY_PASS_THRESHOLD else []
    keyword_audit = audit_keywords(content, keywords)
    heading_audit = validate_heading_structure(content)

    # Check meta description
    fm_match = re.search(r"^---\s*([\s\S]*?)\s*---", content)
    fm = fm_match.group(1) if fm_match else ""
    meta_match = re.search(r"meta_description:\s*[\"'](.+?)[\"']", fm)
    meta = meta_match.group(1) if meta_match else ""
    meta_length = len(meta)
    meta_ok = 120 <= meta_length <= 155

    # Calculate SEO score (weighted)
    score_components = {
        "readability": (1.0 if readability >= READABILITY_PASS_THRESHOLD else readability / READABILITY_PASS_THRESHOLD, 0.20),
        "keyword_density": (1.0 if not keyword_audit["violations"] else 0.7, 0.25),
        "heading_structure": (1.0 if heading_audit["hierarchy_valid"] else 0.6, 0.20),
        "meta_description": (1.0 if meta_ok else 0.5, 0.20),
        "keyword_placement": (
            1.0 if all(
                keyword_audit["keyword_results"].get(primary_keyword, {}).get(k)
                for k in ["in_h1", "in_meta", "in_first_100_words"]
                if keyword_audit["keyword_results"].get(primary_keyword, {}).get(k) is not None
            ) else 0.6,
            0.15
        ),
    }

    weighted_score = sum(score * weight for score, weight in score_components.values())

    # Generate seo-meta.json
    seo_meta = {
        "file": str(file_path.relative_to(WORKSPACE_ROOT)),
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "primary_keyword": primary_keyword,
        "meta_description": meta or generate_meta_description(content, primary_keyword),
        "meta_description_length": meta_length,
        "meta_ok": meta_ok,
        "h1_count": heading_audit["h1_count"],
        "heading_structure_valid": heading_audit["hierarchy_valid"],
        "flesch_kincaid_score": readability,
        "readability_pass": readability >= READABILITY_PASS_THRESHOLD,
        "word_count": len(body.split()),
        "seo_score": round(weighted_score, 4),
        "seo_pass": weighted_score >= SEO_PASS_THRESHOLD,
        "violations": (
            keyword_audit["violations"] +
            heading_audit["violations"] +
            ([{"type": "meta_length", "message": f"Meta description is {meta_length} chars (target: 120–155)"}] if not meta_ok else []) +
            ([{"type": "readability", "message": f"Flesch score is {readability} (target: ≥{READABILITY_PASS_THRESHOLD})", "suggestions": simplifications}] if readability < READABILITY_PASS_THRESHOLD else [])
        ),
    }

    # Save seo-meta.json next to the file
    seo_meta_path = file_path.parent / "seo-meta.json"
    existing = {}
    if seo_meta_path.exists():
        with open(seo_meta_path) as f:
            existing = json.load(f)

    # Upsert by file path
    file_key = str(file_path.relative_to(WORKSPACE_ROOT))
    if "files" not in existing:
        existing["files"] = {}
    existing["files"][file_key] = seo_meta
    existing["last_updated"] = datetime.now(timezone.utc).isoformat()

    with open(seo_meta_path, "w") as f:
        json.dump(existing, f, indent=2)

    # Log
    log_seo_audit(str(file_path.relative_to(WORKSPACE_ROOT)), weighted_score, readability)

    return seo_meta


def audit_directory(content_dir: Path = None) -> dict:
    """Audit all Markdown files in content directory."""
    if content_dir is None:
        content_dir = project_content_root()

    results = {}
    for md_file in content_dir.rglob("*.md"):
        if "_references" in str(md_file) or "templates" in str(md_file):
            continue
        results[str(md_file.relative_to(WORKSPACE_ROOT))] = audit_file(md_file)

    return results


def log_seo_audit(file_path: str, score: float, readability: float) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "seo_audit",
        "file": file_path,
        "seo_score": round(score, 4),
        "flesch_score": readability,
        "passed": score >= SEO_PASS_THRESHOLD,
    }
    SEO_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(SEO_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
