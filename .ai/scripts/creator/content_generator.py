"""
content_generator.py — Sovereign Content Generation Orchestrator
===============================================================
Orchestrates the full content creation pipeline for all /create commands.
Reads brand rules, loads the appropriate blueprint, builds structured
generation prompts, validates output, and writes final Markdown with
required YAML frontmatter.

Owner: creator-agent
Sub-agents: blueprint-architect, content-generator, brand-voice-applier
Trigger: /create website pages | /create blog posts about [topic] |
         /create project pages | /create landing pages for [campaign]

Pipeline:
  1. Load brand context (style-rules + glossary + market-positioning)
  2. Select blueprint template for content type
  3. Load competitive reference (optional — structural inspiration only)
  4. Build generation prompt per blueprint section
  5. Validate: brand voice ≥ 92%, originality ≤ 15%
  6. Write output to content/[type]/[slug].md with YAML frontmatter
  7. Log to .ai/logs/workflow.jsonl
"""

import json
import re
import hashlib
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import (  # noqa: E402
    REPO_ROOT,
    active_project,
    logs_dir,
    project_comparisons_dir,
    project_content_root,
    project_reference_dir,
    project_scraped_dir,
    templates_dir,
)

# ── Paths ─────────────────────────────────────────────────────────────────────

WORKSPACE_ROOT = REPO_ROOT
REFERENCE_DIR = project_reference_dir()
BRAND_VOICE_DIR = REFERENCE_DIR / "brand-voice"
CONTENT_DIR = project_content_root()
TEMPLATES_DIR = templates_dir() / "content-blueprints"
LOGS_DIR = logs_dir()
WORKFLOW_LOG = LOGS_DIR / "workflow.jsonl"
_P = active_project()


# ── Content Type Registry ──────────────────────────────────────────────────────

CONTENT_TYPES = {
    "website_pages": {
        "output_dir": CONTENT_DIR / "website-pages",
        "template": TEMPLATES_DIR / "website-page.md",
        "default_variants": ["home", "about", "services", "contact", "faq"],
        "intent": "create_website_pages",
    },
    "blog_posts": {
        "output_dir": CONTENT_DIR / "blog-posts",
        "template": TEMPLATES_DIR / "blog-post.md",
        "default_variants": ["educational", "perspective", "project-spotlight"],
        "intent": "create_blog_posts",
    },
    "project_pages": {
        "output_dir": CONTENT_DIR / "projects",
        "template": TEMPLATES_DIR / "project-page.md",
        "default_variants": ["residential", "commercial"],
        "intent": "create_project_pages",
    },
    "landing_pages": {
        "output_dir": CONTENT_DIR / "landing-pages",
        "template": TEMPLATES_DIR / "landing-page.md",
        "default_variants": [],
        "intent": "create_landing_pages",
    },
}

# Originality gate: similarity score must stay BELOW this threshold
ORIGINALITY_THRESHOLD = 0.15

# Brand voice gate: compliance score must meet or exceed this threshold
BRAND_VOICE_THRESHOLD = 0.92

# Maximum auto-retry count before flagging for human review
MAX_AUTO_RETRIES = 2


# ── Brand Context Loader ───────────────────────────────────────────────────────

def load_brand_context() -> dict:
    """
    Load all brand context files required before content generation.
    Returns structured dict with positioning + voice rules + glossary.

    Raises FileNotFoundError if critical brand files are missing.
    Called by: blueprint-architect sub-agent before any generation.
    """
    context = {
        "market_positioning": "",
        "style_rules": "",
        "glossary": "",
        "keyword_maps": "",
        "brand_loaded": False,
        "missing_files": [],
    }

    # market-positioning.md — required
    mp_path = REFERENCE_DIR / "market-positioning.md"
    if mp_path.exists() and mp_path.stat().st_size > 50:
        context["market_positioning"] = mp_path.read_text(encoding="utf-8")
    else:
        context["missing_files"].append(f"content/{_P}/reference/market-positioning.md")

    # style-rules.md — required
    sr_path = BRAND_VOICE_DIR / "style-rules.md"
    if sr_path.exists() and sr_path.stat().st_size > 50:
        context["style_rules"] = sr_path.read_text(encoding="utf-8")
    else:
        context["missing_files"].append(f"content/{_P}/reference/brand-voice/style-rules.md")

    # glossary.md — required
    gl_path = BRAND_VOICE_DIR / "glossary.md"
    if gl_path.exists() and gl_path.stat().st_size > 50:
        context["glossary"] = gl_path.read_text(encoding="utf-8")
    else:
        context["missing_files"].append(f"content/{_P}/reference/brand-voice/glossary.md")

    # keyword-maps.md — optional (generate from topic if missing)
    km_path = CONTENT_DIR / "_references" / "keyword-maps.md"
    if km_path.exists():
        context["keyword_maps"] = km_path.read_text(encoding="utf-8")

    context["brand_loaded"] = len(context["missing_files"]) == 0
    return context


def assert_brand_ready(context: dict) -> None:
    """Hard block if critical brand files are missing."""
    if not context["brand_loaded"]:
        missing = "\n  - ".join(context["missing_files"])
        raise RuntimeError(
            f"Cannot generate content — brand context is incomplete.\n"
            f"Missing files:\n  - {missing}\n\n"
            f"Run /brand to complete brand discovery, or /extract brand voice from [source] first."
        )


# ── Blueprint Loader ───────────────────────────────────────────────────────────

def load_blueprint(content_type: str) -> str:
    """Load the content blueprint template for the given type."""
    spec = CONTENT_TYPES.get(content_type)
    if not spec:
        raise ValueError(f"Unknown content type: {content_type}. Valid: {list(CONTENT_TYPES.keys())}")

    template_path = spec["template"]
    if not template_path.exists():
        raise FileNotFoundError(
            f"Blueprint template not found: {template_path}\n"
            f"Expected at: .ai/templates/content-blueprints/{template_path.name}"
        )

    return template_path.read_text(encoding="utf-8")


# ── Slug Generator ─────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert a title or topic string to a safe file slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:80].strip("-")


def versioned_path(output_dir: Path, slug: str, ext: str = ".md") -> Path:
    """Return a versioned path if slug already exists (slug_v2.md, _v3.md...)"""
    base = output_dir / f"{slug}{ext}"
    if not base.exists():
        return base

    for i in range(2, 20):
        candidate = output_dir / f"{slug}_v{i}{ext}"
        if not candidate.exists():
            return candidate

    # Fallback: timestamp suffix
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return output_dir / f"{slug}_{ts}{ext}"


# ── Generation Prompt Builder ──────────────────────────────────────────────────

def build_generation_prompt(
    content_type: str,
    topic_or_variant: str,
    blueprint: str,
    brand_context: dict,
) -> str:
    """
    Build a structured generation prompt for the AI content-generator sub-agent.
    This prompt is passed to the LLM invocation layer (not executed directly here).

    Returns: fully structured prompt string ready for LLM consumption.
    Called by: content-generator sub-agent.
    """
    positioning = brand_context.get("market_positioning", "")[:2000]
    style_rules = brand_context.get("style_rules", "")[:3000]
    glossary = brand_context.get("glossary", "")[:1500]
    keyword_maps = brand_context.get("keyword_maps", "")[:1000]

    # Extract key voice signals for tighter prompt constraints
    voice_section = _extract_voice_signals(style_rules)
    prohibited = _extract_prohibited_terms(glossary)

    prompt = f"""You are the content-generator sub-agent for Sovereign, a premium interior design studio.

## TASK
Generate original {content_type.replace("_", " ")} content for: **{topic_or_variant}**

## BRAND CONTEXT (non-negotiable — follow exactly)

### Market Positioning
{positioning}

### Voice & Tone Rules
{voice_section}

### Prohibited Language
{prohibited}

### Keyword Context
{keyword_maps or "Use natural interior design terminology aligned to the target audience."}

## CONTENT BLUEPRINT (structure to follow)
{blueprint}

## OUTPUT REQUIREMENTS

1. **Format:** Markdown with YAML frontmatter at top
2. **Frontmatter schema:**
   ```yaml
   ---
   title: ""
   meta_description: ""       # 150-160 chars, keyword-leading
   keywords: []               # 3-5 primary keywords
   content_type: "{content_type}"
   variant: "{topic_or_variant}"
   created_at: "{datetime.now(timezone.utc).isoformat()}"
   version: "1.0"
   status: "draft"
   tone_score: null           # Filled by brand-voice-applier gate
   originality_score: null    # Filled by originality gate
   author: "creator-agent"
   ---
   ```
3. **Voice:** Must match the style rules above. Check every sentence.
4. **Originality:** Write from Sovereign's specific perspective — never generic industry copy.
5. **No filler:** Every sentence must earn its place. Remove hedging language.
6. **Word count:** 600-900 words for blog posts; 250-500 per page section for website pages.

## VALIDATION TARGETS (auto-checked after generation)
- Brand voice compliance: ≥ 92%
- Originality: ≤ 15% similarity to any source
- Readability: Flesch-Kincaid ≥ 65
- Image SEO: alt-text placeholders for every image reference
- SEO: Primary keyword in H1, first paragraph, and meta description

Generate the complete Markdown document now.
"""
    return prompt


def _extract_voice_signals(style_rules: str) -> str:
    """Extract key voice rules summary from style-rules.md for prompt injection."""
    if not style_rules:
        return "Use professional, precise, confident language. No filler words."

    # Find tone rules section
    lines = style_rules.split("\n")
    tone_lines = []
    in_tone_section = False

    for line in lines:
        if "## Tone Rules" in line or "## Brand Spectrum" in line or "## Language Rules" in line:
            in_tone_section = True
        elif line.startswith("## ") and in_tone_section and "Tone" not in line and "Language" not in line and "Spectrum" not in line:
            in_tone_section = False
        if in_tone_section:
            tone_lines.append(line)

    return "\n".join(tone_lines[:40]) if tone_lines else style_rules[:800]


def _extract_prohibited_terms(glossary: str) -> str:
    """Extract prohibited terms from glossary.md for prompt injection."""
    if not glossary:
        return "Avoid: generic claims, weak adjectives (very/really), hedging language (we think/we feel)."

    lines = glossary.split("\n")
    prohibited_lines = []
    in_prohibited = False

    for line in lines:
        if "## Prohibited" in line:
            in_prohibited = True
        elif line.startswith("## ") and in_prohibited and "Prohibited" not in line:
            in_prohibited = False
        if in_prohibited:
            prohibited_lines.append(line)

    return (
        "\n".join(prohibited_lines[:25])
        if prohibited_lines
        else f"See content/{_P}/reference/brand-voice/glossary.md"
    )


# ── Frontmatter Builder ────────────────────────────────────────────────────────

def build_frontmatter(
    title: str,
    meta_description: str,
    keywords: list[str],
    content_type: str,
    variant: str,
    tone_score: Optional[float] = None,
    originality_score: Optional[float] = None,
) -> str:
    """Generate YAML frontmatter block for a content file."""
    keywords_yaml = "\n".join(f'  - "{kw}"' for kw in keywords)
    return f"""---
title: "{title}"
meta_description: "{meta_description[:160]}"
keywords:
{keywords_yaml}
content_type: "{content_type}"
variant: "{variant}"
created_at: "{datetime.now(timezone.utc).isoformat()}"
version: "1.0"
status: "draft"
tone_score: {tone_score if tone_score is not None else "null"}
originality_score: {originality_score if originality_score is not None else "null"}
author: "creator-agent"
---
"""


# ── Originality Checker ────────────────────────────────────────────────────────

def compute_content_hash(text: str) -> str:
    """Compute SHA-256 hash of content for deduplication tracking."""
    normalized = re.sub(r"\s+", " ", text.lower().strip())
    return hashlib.sha256(normalized.encode()).hexdigest()


def estimate_originality_score(content: str, reference_dir: Optional[Path] = None) -> float:
    """
    Simplified originality estimate using n-gram overlap.
    Returns a float 0.0–1.0 representing estimated similarity (lower = more original).

    Production version would use semantic similarity via embeddings.
    This implementation uses trigram overlap as a fast proxy.
    """
    if not reference_dir or not reference_dir.exists():
        return 0.05  # No references available — assume original

    content_trigrams = _extract_trigrams(content)
    if not content_trigrams:
        return 0.0

    max_similarity = 0.0
    ref_files = list(reference_dir.rglob("*.md"))[:20]  # Cap at 20 refs for performance

    for ref_file in ref_files:
        try:
            ref_text = ref_file.read_text(encoding="utf-8", errors="ignore")
            ref_trigrams = _extract_trigrams(ref_text)
            if not ref_trigrams:
                continue
            overlap = len(content_trigrams & ref_trigrams) / len(content_trigrams)
            max_similarity = max(max_similarity, overlap)
        except Exception:
            continue

    return round(max_similarity, 3)


def _extract_trigrams(text: str) -> set:
    """Extract word trigrams from text."""
    words = re.findall(r"\b\w+\b", text.lower())
    return {" ".join(words[i:i+3]) for i in range(len(words) - 2)}


# ── Content Writer ─────────────────────────────────────────────────────────────

def write_content_file(
    content_type: str,
    slug: str,
    body: str,
    frontmatter: str,
) -> Path:
    """
    Write the final content Markdown file to the correct output directory.
    Versioning applied automatically if slug already exists.
    Returns the path written to.
    """
    spec = CONTENT_TYPES[content_type]
    output_dir: Path = spec["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = versioned_path(output_dir, slug)
    full_content = frontmatter + "\n" + body
    output_path.write_text(full_content, encoding="utf-8")

    return output_path


# ── Pipeline Orchestrator ──────────────────────────────────────────────────────

def run_content_pipeline(
    content_type: str,
    topic_or_variant: str,
    generated_body: str,
    title: str = "",
    meta_description: str = "",
    keywords: Optional[list] = None,
) -> dict:
    """
    Main orchestration function for the content creation pipeline.
    Intended to be called by the guide-agent after AI content has been generated.

    Steps:
    1. Load brand context (assert brand is ready)
    2. Validate originality
    3. Build frontmatter
    4. Write file
    5. Log to workflow.jsonl

    Args:
        content_type:      One of CONTENT_TYPES keys
        topic_or_variant:  Topic string (e.g. "sustainable interior design")
        generated_body:    Markdown body text (AI-generated)
        title:             Page title (extracted from body or provided)
        meta_description:  SEO meta description (extracted or provided)
        keywords:          Primary keywords list

    Returns:
        {status, output_path, slug, originality_score, warnings}
    """
    warnings = []
    keywords = keywords or []

    # Step 1: Brand context
    brand_context = load_brand_context()
    assert_brand_ready(brand_context)

    # Step 2: Originality check
    reference_path = project_scraped_dir()
    originality_score = estimate_originality_score(generated_body, reference_path)

    retries = 0
    if originality_score > ORIGINALITY_THRESHOLD:
        warnings.append(
            f"Originality score {originality_score:.0%} exceeds threshold {ORIGINALITY_THRESHOLD:.0%}. "
            f"Structural shift recommended. Retry {retries + 1}/{MAX_AUTO_RETRIES}."
        )
        # In production: trigger content-generator sub-agent retry with stricter prompt
        if retries >= MAX_AUTO_RETRIES:
            warnings.append("Max retries reached. Content flagged for manual review.")

    # Step 3: Build frontmatter
    slug = slugify(topic_or_variant or title or content_type)
    frontmatter = build_frontmatter(
        title=title or topic_or_variant,
        meta_description=meta_description,
        keywords=keywords,
        content_type=content_type,
        variant=topic_or_variant,
        originality_score=originality_score,
        # tone_score: filled by brand-voice-applier — left null here
    )

    # Step 4: Write file
    output_path = write_content_file(content_type, slug, generated_body, frontmatter)

    # Step 5: Log
    _log_content_event(
        content_type=content_type,
        slug=slug,
        output_path=output_path,
        originality_score=originality_score,
        warnings=warnings,
    )

    return {
        "status": "draft_written",
        "output_path": str(output_path.relative_to(WORKSPACE_ROOT)),
        "slug": slug,
        "content_type": content_type,
        "originality_score": originality_score,
        "originality_pass": originality_score <= ORIGINALITY_THRESHOLD,
        "warnings": warnings,
        "next_step": "/polish content in content/" if not warnings else "/revise [address originality flag]",
    }


def _log_content_event(
    content_type: str,
    slug: str,
    output_path: Path,
    originality_score: float,
    warnings: list,
) -> None:
    """Append content creation event to workflow.jsonl."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "content_draft_written",
        "content_type": content_type,
        "slug": slug,
        "output_path": str(output_path.relative_to(WORKSPACE_ROOT)),
        "originality_score": originality_score,
        "originality_pass": originality_score <= ORIGINALITY_THRESHOLD,
        "warnings": warnings,
    }
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(WORKFLOW_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ── Comparison Generator ───────────────────────────────────────────────────────

def run_comparison_pipeline(
    competitor_slug: str,
    sovereign_draft_path: Optional[str] = None,
) -> dict:
    """
    Orchestrate the /compare sovereign vs competitor [name] pipeline.
    Loads competitor scraped content, builds comparison prompt,
    outputs to comparisons/sovereign_vs_[slug].md.

    Owner: creator-agent / comparison-analyst sub-agent.
    """
    competitor_dir = project_scraped_dir() / competitor_slug
    scraped_dir = competitor_dir / "scraped" / "content"

    if not competitor_dir.exists():
        return {
            "status": "error",
            "error": f"Competitor '{competitor_slug}' not found in registry. Run /research competitors first.",
            "next_step": "/research competitors",
        }

    if not scraped_dir.exists():
        return {
            "status": "error",
            "error": f"No scraped content for '{competitor_slug}'. Run /scrape {competitor_slug} all website first.",
            "next_step": f"/scrape {competitor_slug} all website",
        }

    # Load brand context
    brand_context = load_brand_context()
    assert_brand_ready(brand_context)

    # Comparison output
    comparisons_dir = project_comparisons_dir()
    comparisons_dir.mkdir(parents=True, exist_ok=True)
    output_path = versioned_path(comparisons_dir, f"sovereign_vs_{competitor_slug}")

    _log_comparison_event(competitor_slug, output_path)

    return {
        "status": "comparison_initiated",
        "competitor": competitor_slug,
        "output_path": str(output_path.relative_to(WORKSPACE_ROOT)),
        "scraped_source": str(scraped_dir.relative_to(WORKSPACE_ROOT)),
        "next_step": f"Review comparison at {output_path.relative_to(WORKSPACE_ROOT)}",
    }


def _log_comparison_event(competitor_slug: str, output_path: Path) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "comparison_initiated",
        "competitor_slug": competitor_slug,
        "output_path": str(output_path.relative_to(WORKSPACE_ROOT)),
    }
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(WORKFLOW_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ── Context Validation ─────────────────────────────────────────────────────────

def validate_content_prerequisites(content_type: str) -> dict:
    """
    Pre-flight check before any content generation command.
    Returns dict with {ready: bool, missing: list, clarifying_question: str}

    Called by: guide-agent / cli_router before routing to creator-agent.
    """
    brand_context = load_brand_context()
    missing = brand_context.get("missing_files", [])

    spec = CONTENT_TYPES.get(content_type, {})
    template_path = spec.get("template")
    if template_path and not template_path.exists():
        missing.append(f".ai/templates/content-blueprints/{template_path.name}")

    if missing:
        return {
            "ready": False,
            "missing": missing,
            "clarifying_question": (
                "Brand foundation files are missing. "
                "Run /brand to complete the brand discovery session first."
                if any("market-positioning" in m or "style-rules" in m for m in missing)
                else f"Some required files are missing: {', '.join(missing[:2])}. How would you like to proceed?"
            ),
        }

    return {"ready": True, "missing": [], "clarifying_question": None}


if __name__ == "__main__":
    # Diagnostic: print loaded brand context status
    ctx = load_brand_context()
    print(f"Brand context loaded: {ctx['brand_loaded']}")
    if ctx["missing_files"]:
        print(f"Missing: {ctx['missing_files']}")
    else:
        print("All brand files present — ready for /create commands.")
