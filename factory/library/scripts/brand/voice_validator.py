"""
voice_validator.py — Sovereign Brand Voice Validator
====================================================
Scores content against brand voice style rules.
Returns compliance score + violation list.
Threshold: ≥ 92% required for export.

Owner: brand-agent / brand-voice-applier sub-agent
"""

import json
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

from paths import REPO_ROOT, logs_dir, project_content_root, project_reference_dir  # noqa: E402

WORKSPACE_ROOT = REPO_ROOT
_ref = project_reference_dir()
STYLE_RULES_PATH = _ref / "brand-voice" / "style-rules.md"
GLOSSARY_PATH = _ref / "brand-voice" / "glossary.md"
COMPLIANCE_LOG = logs_dir() / "content-polish.jsonl"

COMPLIANCE_THRESHOLD = 0.92


# ── Hard-coded rule checks (loaded from style-rules.md in production) ─────────

PROHIBITED_TERMS = [
    "amazing", "stunning", "world-class", "state-of-the-art", "best-in-class",
    "passionate about", "excited to announce", "game-changing", "disrupting",
    "next-level", "seamless", "leverage", "utilize", "synergy", "solutions",
    "holistic", "journey", "empower",
]

FILLER_PHRASES = [
    "in today's world", "it goes without saying", "as we all know",
    "at the end of the day", "having said that",
]

TONE_RULES = {
    "no_exclamation_editorial": {
        "pattern": re.compile(r"!(?!\[)"),  # ! not followed by [ (allows Markdown images)
        "weight": 0.10,
        "rule": "T-05",
        "severity": "minor",
        "message": "Exclamation marks not permitted in editorial content.",
    },
    "no_filler_phrases": {
        "patterns": [re.compile(re.escape(p), re.IGNORECASE) for p in FILLER_PHRASES],
        "weight": 0.08,
        "rule": "L-04",
        "severity": "minor",
        "message": "Filler phrase detected.",
    },
    "no_prohibited_terms": {
        "patterns": [re.compile(r"\b" + re.escape(t) + r"\b", re.IGNORECASE) for t in PROHIBITED_TERMS],
        "weight": 0.15,
        "rule": "Glossary",
        "severity": "major",
        "message": "Prohibited term detected.",
    },
    "active_voice": {
        "pattern": re.compile(
            r"\b(is|are|was|were|be|been|being)\s+(being\s+)?\w+ed\b",
            re.IGNORECASE
        ),
        "weight": 0.08,
        "rule": "L-03",
        "severity": "minor",
        "message": "Passive voice construction detected.",
    },
    "no_generic_cta": {
        "patterns": [
            re.compile(r"\b(buy now|click here|learn more|sign up|subscribe)\b", re.IGNORECASE),
            re.compile(r"\bdon't miss\b", re.IGNORECASE),
            re.compile(r"\blimited time\b", re.IGNORECASE),
        ],
        "weight": 0.12,
        "rule": "T-03",
        "severity": "major",
        "message": "Generic or pressuring CTA detected.",
    },
    "no_generic_opener": {
        "patterns": [
            re.compile(r"^in today'?s", re.IGNORECASE | re.MULTILINE),
            re.compile(r"^in this article", re.IGNORECASE | re.MULTILINE),
            re.compile(r"^we('ll| will) (explore|discuss|cover|look at)", re.IGNORECASE | re.MULTILINE),
        ],
        "weight": 0.08,
        "rule": "S-02",
        "severity": "minor",
        "message": "Generic opener pattern detected.",
    },
}


def check_sentence_variety(text: str) -> tuple[float, list[dict]]:
    """
    Check sentence length variety (rule L-01).
    Returns (score, violations).
    Score: 1.0 if variety is good, lower if monotone.
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 1.0, []

    lengths = [len(s.split()) for s in sentences]
    if not lengths:
        return 1.0, []

    avg_len = sum(lengths) / len(lengths)
    variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)

    # Low variance = monotone sentence structure
    score = min(1.0, variance / 50)
    violations = []
    if score < 0.5:
        violations.append({
            "rule": "L-01",
            "severity": "minor",
            "message": f"Sentence length variety is low (variance: {variance:.1f}). Mix short and longer sentences.",
        })
    return score, violations


def check_passive_voice_rate(text: str) -> tuple[float, list[dict]]:
    """Check passive voice rate. Target: < 15%."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return 1.0, []

    passive_pattern = re.compile(r"\b(is|are|was|were|be|been|being)\s+(being\s+)?\w+ed\b", re.IGNORECASE)
    passive_count = sum(1 for s in sentences if passive_pattern.search(s))
    rate = passive_count / len(sentences)

    score = 1.0 - max(0, rate - 0.15)  # Deduct for rate > 15%
    violations = []
    if rate > 0.15:
        violations.append({
            "rule": "L-03",
            "severity": "minor",
            "message": f"Passive voice rate is {rate:.0%} (target: < 15%). Review passive constructions.",
        })
    return score, violations


def score_content(content: str, file_path: str = None) -> dict:
    """
    Score content against Sovereign brand voice rules.

    Args:
        content: Markdown content to score
        file_path: Optional file path for logging

    Returns:
        {
            compliance_score: float,
            passed: bool,
            violations: [{rule, severity, message, location}],
            summary: str
        }
    """
    violations = []
    total_weight = 0.0
    failed_weight = 0.0

    # Strip YAML frontmatter for analysis
    body = re.sub(r"^---[\s\S]*?---\n", "", content, count=1)

    # ── Check each tone rule ──────────────────────────────────────────────────

    for rule_name, rule in TONE_RULES.items():
        weight = rule["weight"]
        total_weight += weight

        patterns = rule.get("patterns") or ([rule.get("pattern")] if rule.get("pattern") else [])
        found_violations = []

        for pattern in patterns:
            matches = list(pattern.finditer(body))
            for match in matches[:3]:  # Cap at 3 examples per rule
                start = max(0, match.start() - 30)
                end = min(len(body), match.end() + 30)
                found_violations.append({
                    "rule": rule["rule"],
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "excerpt": f"...{body[start:end].strip()}...",
                    "position": match.start(),
                })

        if found_violations:
            failed_weight += weight * min(1.0, len(found_violations) / 3)
            violations.extend(found_violations[:2])  # Max 2 violations per rule in output

    # ── Sentence variety ──────────────────────────────────────────────────────
    variety_weight = 0.10
    total_weight += variety_weight
    variety_score, variety_violations = check_sentence_variety(body)
    if variety_score < 1.0:
        failed_weight += variety_weight * (1 - variety_score)
        violations.extend(variety_violations)

    # ── Passive voice ─────────────────────────────────────────────────────────
    passive_weight = 0.08
    total_weight += passive_weight
    passive_score, passive_violations = check_passive_voice_rate(body)
    if passive_score < 1.0:
        failed_weight += passive_weight * (1 - passive_score)
        violations.extend(passive_violations)

    # ── Calculate final score ─────────────────────────────────────────────────
    compliance_score = max(0.0, 1.0 - (failed_weight / total_weight)) if total_weight > 0 else 1.0
    passed = compliance_score >= COMPLIANCE_THRESHOLD

    result = {
        "compliance_score": round(compliance_score, 4),
        "passed": passed,
        "threshold": COMPLIANCE_THRESHOLD,
        "violations": violations[:10],  # Cap at 10 violations in output
        "total_violations_found": len(violations),
        "summary": (
            f"Brand voice: {compliance_score:.0%} "
            f"({'✅ Pass' if passed else '❌ Fail — ' + str(len(violations)) + ' violations'})"
        ),
    }

    # Log result
    log_validation(file_path or "unknown", compliance_score, passed, len(violations))

    return result


def log_validation(file_path: str, score: float, passed: bool, violation_count: int) -> None:
    """Log validation result."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "brand_voice_validation",
        "file": file_path,
        "score": round(score, 4),
        "passed": passed,
        "violations_found": violation_count,
    }
    COMPLIANCE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(COMPLIANCE_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def validate_directory(content_dir: Path = None) -> dict:
    """Validate all draft Markdown files in a content directory."""
    if content_dir is None:
        content_dir = project_content_root()

    results = {}
    for md_file in content_dir.rglob("*.md"):
        if "_references" in str(md_file):
            continue
        content = md_file.read_text(encoding="utf-8")
        results[str(md_file.relative_to(WORKSPACE_ROOT))] = score_content(content, str(md_file))

    return results
