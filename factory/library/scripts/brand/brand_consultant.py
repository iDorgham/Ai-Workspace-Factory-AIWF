"""
brand_consultant.py — Sovereign Brand Discovery Interview Engine
===============================================================
Runs a structured, phase-by-phase brand consultation interview.
Reads questions from templates/brand-discovery/questions.json.
Outputs: market-positioning.md, style-rules.md, glossary.md,
         tone-examples.md, voice-refinement.md

Owner: brand-agent / brand-consultant sub-agent
Pipeline: /brand command — must run BEFORE /create or /extract brand voice

Usage:
    python3 .ai/scripts/brand/brand_consultant.py

Output files:
    reference/market-positioning.md
    reference/brand-voice/style-rules.md
    reference/brand-voice/glossary.md
    reference/brand-voice/tone-examples.md
    reference/brand-voice/voice-refinement.md
    .ai/logs/brand-session.json  (full session record)
"""

import json
import sys
import textwrap
from pathlib import Path
from datetime import datetime, timezone

_scripts = Path(__file__).resolve().parent
while _scripts.name != "scripts" and _scripts != _scripts.parent:
    _scripts = _scripts.parent
if not (_scripts / "paths.py").is_file():
    raise RuntimeError("Expected .ai/scripts/paths.py — run from Sovereign workspace.")
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, logs_dir, project_reference_dir, templates_dir  # noqa: E402

# ── Paths ─────────────────────────────────────────────────────────────────────

WORKSPACE_ROOT = REPO_ROOT
_td = templates_dir()
QUESTION_PATH_CANDIDATES = [
    _td / "brand-discovery" / "questions.json",
    WORKSPACE_ROOT / "templates" / "brand-discovery" / "questions.json",
]
REFERENCE_DIR = project_reference_dir()
BRAND_VOICE_DIR = REFERENCE_DIR / "brand-voice"
LOGS_DIR = logs_dir()
WORKFLOW_LOG = LOGS_DIR / "workflow.jsonl"
SESSION_LOG = LOGS_DIR / "brand-session.json"


# ── Terminal Formatting ────────────────────────────────────────────────────────

RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
CYAN    = "\033[36m"
YELLOW  = "\033[33m"
GREEN   = "\033[32m"
MAGENTA = "\033[35m"
WHITE   = "\033[97m"
BG_DARK = "\033[48;5;235m"


def hr(char: str = "─", width: int = 60, color: str = DIM) -> str:
    return f"{color}{char * width}{RESET}"


def header(title: str, icon: str = "◆") -> None:
    print()
    print(hr("═", 60, CYAN))
    print(f"{BOLD}{CYAN}  {icon}  {title.upper()}{RESET}")
    print(hr("═", 60, CYAN))
    print()


def phase_header(phase_num: int, phase_name: str, icon: str, description: str) -> None:
    print()
    print(hr("─", 60, DIM))
    print(f"{BOLD}{YELLOW}  {icon}  PHASE {phase_num}: {phase_name.upper()}{RESET}")
    print(f"{DIM}  {description}{RESET}")
    print(hr("─", 60, DIM))
    print()


def question_prompt(q_num: int, total: int, text: str, required: bool) -> None:
    req_badge = f"{MAGENTA}[required]{RESET}" if required else f"{DIM}[optional]{RESET}"
    print(f"{BOLD}{WHITE}Q{q_num}/{total}  {req_badge}{RESET}")
    print(f"{CYAN}{textwrap.fill(text, width=58, subsequent_indent='  ')}{RESET}")


def success(msg: str) -> None:
    print(f"\n{GREEN}  ✓  {msg}{RESET}")


def info(msg: str) -> None:
    print(f"{DIM}  ℹ  {msg}{RESET}")


def error_msg(msg: str) -> None:
    print(f"\n{YELLOW}  ⚠  {msg}{RESET}")


# ── Question Loading ───────────────────────────────────────────────────────────

def load_questions() -> dict:
    for path in QUESTION_PATH_CANDIDATES:
        if path.exists():
            with open(path) as f:
                return json.load(f)
    print(
        f"\n{YELLOW}ERROR: questions.json not found in expected locations:{RESET}\n"
        + "\n".join([f"  - {p}" for p in QUESTION_PATH_CANDIDATES])
    )
    sys.exit(1)


def get_phases(questions_data: dict) -> list[dict]:
    return questions_data.get("phases", [])


def get_questions_for_phase(questions_data: dict, phase_id: str) -> list[dict]:
    all_q = questions_data.get("questions", [])
    return [q for q in all_q if q.get("phase") == phase_id]


# ── Input Handlers ─────────────────────────────────────────────────────────────

def ask_single_choice(question: dict) -> str:
    """Display numbered options; user enters number or types 'other'."""
    choices = question.get("choices", [])
    has_other = question.get("type") == "single_choice_with_other"

    for i, choice in enumerate(choices, 1):
        print(f"  {DIM}{i}.{RESET}  {choice}")
    if has_other:
        print(f"  {DIM}{len(choices)+1}.{RESET}  Other (type your own)")

    print()

    while True:
        raw = input(f"  {BOLD}→ Enter number: {RESET}").strip()

        if not raw and not question.get("required"):
            return ""

        # Numeric selection
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(choices):
                return choices[idx - 1]
            if has_other and idx == len(choices) + 1:
                custom = input(f"  {BOLD}→ Type your answer: {RESET}").strip()
                return custom if custom else ""
            error_msg(f"Enter a number between 1 and {len(choices) + (1 if has_other else 0)}.")
        else:
            # Allow typing the value directly
            match = next((c for c in choices if c.lower() == raw.lower()), None)
            if match:
                return match
            if has_other:
                return raw
            error_msg("Please enter the number of your choice.")


def ask_multi_choice(question: dict) -> list[str]:
    """Multi-select: comma-separated numbers or 'other'."""
    choices = question.get("choices", [])
    has_other = question.get("type") == "multi_choice_with_other"
    max_sel = question.get("max_selections", len(choices))

    for i, choice in enumerate(choices, 1):
        print(f"  {DIM}{i}.{RESET}  {choice}")
    if has_other:
        print(f"  {DIM}{len(choices)+1}.{RESET}  Other (add your own after comma)")

    print()
    info(f"Select up to {max_sel}. Enter numbers separated by commas (e.g. 1,3,5)")
    print()

    while True:
        raw = input(f"  {BOLD}→ Your choices: {RESET}").strip()

        if not raw and not question.get("required"):
            return []

        parts = [p.strip() for p in raw.split(",") if p.strip()]
        selected = []
        custom_added = False

        for part in parts:
            if part.isdigit():
                idx = int(part)
                if 1 <= idx <= len(choices):
                    selected.append(choices[idx - 1])
                elif has_other and idx == len(choices) + 1:
                    if not custom_added:
                        custom = input(f"  {BOLD}→ Add your own: {RESET}").strip()
                        if custom:
                            selected.append(custom)
                        custom_added = True
                else:
                    error_msg(f"Invalid choice: {part}. Skipped.")
            else:
                # Treat as direct text entry (for 'other' type)
                if has_other:
                    selected.append(part)
                else:
                    match = next((c for c in choices if c.lower() == part.lower()), None)
                    if match:
                        selected.append(match)

        if len(selected) > max_sel:
            error_msg(f"Please select at most {max_sel} options.")
            continue

        if not selected and question.get("required"):
            error_msg("This field is required. Please select at least one option.")
            continue

        return selected


def ask_open_text(question: dict) -> str:
    """Free-form text input with optional placeholder hint."""
    placeholder = question.get("placeholder", "")
    if placeholder:
        info(f"Example: {placeholder}")
        print()

    while True:
        raw = input(f"  {BOLD}→ Your answer: {RESET}").strip()
        if not raw and question.get("required"):
            error_msg("This field is required. Please provide an answer.")
            continue
        return raw


def ask_spectrum_grid(question: dict) -> dict:
    """
    Spectrum grid: 5 scales, each with 5 positions (A-E or 1-5).
    A = left pole, E = right pole.
    """
    scales = question.get("scales", [])
    results = {}

    info("Rate each scale from 1 (far left) to 5 (far right).")
    print()

    for scale in scales:
        left = scale.get("left", "")
        right = scale.get("right", "")
        scale_id = scale.get("id", left.lower())

        # Visual scale display
        print(f"  {DIM}{'─'*50}{RESET}")
        print(f"  {CYAN}{left:<22}{RESET}  ◄──────►  {CYAN}{right}{RESET}")
        print(f"  {DIM}1 = strongly {left[:10]}   5 = strongly {right[:10]}{RESET}")

        while True:
            raw = input(f"  {BOLD}→ Score (1-5): {RESET}").strip()
            if raw in {"1", "2", "3", "4", "5"}:
                results[scale_id] = int(raw)
                label = _spectrum_label(int(raw), left, right)
                success(f"Recorded: {label}")
                break
            error_msg("Enter a number from 1 to 5.")

        print()

    return results


def _spectrum_label(score: int, left: str, right: str) -> str:
    labels = {
        1: f"Strongly {left}",
        2: f"Leaning {left}",
        3: "Balanced",
        4: f"Leaning {right}",
        5: f"Strongly {right}",
    }
    return labels.get(score, "Balanced")


# ── Session Runner ─────────────────────────────────────────────────────────────

def run_interview(questions_data: dict) -> dict:
    """Run the full brand discovery interview. Returns completed session dict."""
    phases = get_phases(questions_data)
    all_questions = questions_data.get("questions", [])
    total_q = len(all_questions)
    q_counter = 0

    session = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "answers": {},
    }

    # Welcome screen
    header("Brand Discovery Session", "◆")
    print(f"  {WHITE}Welcome to your Brand Strategy Meeting.{RESET}")
    print(f"  {DIM}You and the branding expert will go through {total_q} guided questions across{RESET}")
    print(f"  {DIM}{len(phases)} phases to define your brand vision, tone, style, and voice.{RESET}")
    print(f"  {DIM}Your answers become the source of truth for all generated content.{RESET}")
    print()
    print(f"  {DIM}• Required questions are marked {MAGENTA}[required]{RESET}")
    print(f"  {DIM}• Press Enter to skip optional questions{RESET}")
    print(f"  {DIM}• Type freely for open text questions{RESET}")
    print()
    input(f"  {BOLD}{CYAN}Press Enter to begin...{RESET}")

    for phase in phases:
        phase_id = phase["id"]
        phase_questions = get_questions_for_phase(questions_data, phase_id)

        if not phase_questions:
            continue

        phase_header(
            phase_num=phase.get("order", 0),
            phase_name=phase.get("name", ""),
            icon=phase.get("icon", "◆"),
            description=phase.get("description", ""),
        )

        for question in phase_questions:
            q_counter += 1
            q_type = question.get("type", "open_text")
            output_field = question.get("output_field", question["id"])

            print()
            question_prompt(q_counter, total_q, question["question"], question.get("required", False))
            print()

            # Dispatch by type
            if q_type == "single_choice":
                answer = ask_single_choice(question)
            elif q_type == "single_choice_with_other":
                answer = ask_single_choice(question)
            elif q_type == "multi_choice":
                answer = ask_multi_choice(question)
            elif q_type == "multi_choice_with_other":
                answer = ask_multi_choice(question)
            elif q_type == "spectrum_grid":
                answer = ask_spectrum_grid(question)
            else:  # open_text
                answer = ask_open_text(question)

            session["answers"][output_field] = answer

            if answer or answer == 0:
                if isinstance(answer, list):
                    success(f"Saved: {', '.join(answer) if answer else '(skipped)'}")
                elif isinstance(answer, dict):
                    pass  # spectrum grid already showed confirmation per scale
                else:
                    success(f"Saved: {str(answer)[:60]}{'...' if len(str(answer)) > 60 else ''}")
            else:
                info("Skipped.")

        print()
        print(hr("─", 60, GREEN))
        print(f"  {GREEN}✓  Phase complete: {phase['name']}{RESET}")
        print(hr("─", 60, GREEN))

        if phase != phases[-1]:
            input(f"\n  {DIM}Press Enter to continue to the next phase...{RESET}")

    session["completed_at"] = datetime.now(timezone.utc).isoformat()
    return session


# ── Output Generators ──────────────────────────────────────────────────────────

def generate_market_positioning(answers: dict) -> str:
    a = answers
    geo = a.get("geography", "")
    stage = a.get("studio_stage", "")
    price = a.get("price_tier", "")
    differentiators = a.get("differentiators", [])
    diff_text = "\n".join(f"- {d}" for d in (differentiators if isinstance(differentiators, list) else [differentiators]))

    archetype = a.get("brand_archetype", "")
    one_liner = a.get("one_liner", "")
    seo_goal = a.get("seo_goal", "")
    client_type = a.get("client_type", "")
    client_profile = a.get("ideal_client_profile", "")
    exclusions = a.get("exclusions", "")
    success_goal = a.get("success_goal", "")
    competitors_ref = a.get("competitor_references", [])
    comp_text = ", ".join(competitors_ref) if isinstance(competitors_ref, list) else str(competitors_ref)

    return f"""---
version: "1.0"
generated_by: brand-consultant
generated_at: "{datetime.now(timezone.utc).isoformat()}"
status: "active"
---

# Sovereign — Market Positioning

## Studio Overview

**One-liner:** {one_liner or "_(not yet defined)_"}

**Studio Stage:** {stage}

**Geographic Focus:** {geo}

**Price Tier:** {price}

**Brand Archetype:** {archetype}

---

## Ideal Client

**Client Type:** {client_type}

**Client Profile:**
{client_profile or "_(not yet defined)_"}

---

## Differentiators

{diff_text or "_(not yet defined)_"}

---

## What We Are NOT

{exclusions or "_(not yet defined)_"}

---

## Competitive Context

Brands we observe (not imitate): {comp_text or "_(none listed)_"}

---

## Content & SEO Focus

**Primary SEO Goal:** {seo_goal or "_(not yet defined)_"}

---

## Success Vision

{success_goal or "_(not yet defined)_"}

---

*Generated by /brand command — Sovereign Universal AI Workspace v3.2*
"""


def generate_style_rules(answers: dict) -> str:
    a = answers
    voice_words = a.get("voice_words", [])
    voice_text = ", ".join(voice_words) if isinstance(voice_words, list) else str(voice_words)

    spectrum = a.get("brand_spectrum", {})
    formality = spectrum.get("formality", 3)
    seriousness = spectrum.get("seriousness", 3)
    expertise = spectrum.get("expertise", 3)
    tradition = spectrum.get("tradition", 3)
    expressiveness = spectrum.get("expressiveness", 3)

    emotional_goals = a.get("emotional_goals", [])
    emotional_text = "\n".join(f"- {g}" for g in (emotional_goals if isinstance(emotional_goals, list) else [emotional_goals]))

    cta_style = a.get("cta_style", "")
    language_rules = a.get("language_rules", [])
    rules_text = "\n".join(f"- {r}" for r in (language_rules if isinstance(language_rules, list) else [language_rules]))

    prohibited = a.get("prohibited_language", "")
    vocab = a.get("preferred_vocabulary", "")

    topics = a.get("content_topics", [])
    topics_text = "\n".join(f"- {t}" for t in (topics if isinstance(topics, list) else [topics]))

    def formality_label(score):
        labels = {1: "Very Formal", 2: "Formal", 3: "Balanced", 4: "Conversational", 5: "Casual"}
        return labels.get(score, "Balanced")

    def seriousness_label(score):
        labels = {1: "Very Serious", 2: "Serious", 3: "Balanced", 4: "Warm/Light", 5: "Playful"}
        return labels.get(score, "Balanced")

    def expertise_label(score):
        labels = {1: "Expert-led", 2: "Expert-leaning", 3: "Balanced", 4: "Client-leaning", 5: "Client-led"}
        return labels.get(score, "Balanced")

    def tradition_label(score):
        labels = {1: "Traditional", 2: "Classic-leaning", 3: "Balanced", 4: "Modern-leaning", 5: "Contemporary"}
        return labels.get(score, "Balanced")

    def expression_label(score):
        labels = {1: "Very Reserved", 2: "Reserved", 3: "Balanced", 4: "Expressive", 5: "Very Expressive"}
        return labels.get(score, "Balanced")

    return f"""---
version: "1.0"
generated_by: brand-consultant
generated_at: "{datetime.now(timezone.utc).isoformat()}"
status: "active"
---

# Sovereign Brand Voice — Style Rules

## Voice Identity

**Core Voice Words:** {voice_text or "_(not yet defined)_"}

**CTA Style:** {cta_style or "_(not yet defined)_"}

---

## Brand Spectrum Positioning

| Dimension | Score | Label |
|-----------|-------|-------|
| Formality | {formality}/5 | {formality_label(formality)} |
| Tone | {seriousness}/5 | {seriousness_label(seriousness)} |
| Expertise Orientation | {expertise}/5 | {expertise_label(expertise)} |
| Style Tradition | {tradition}/5 | {tradition_label(tradition)} |
| Expressiveness | {expressiveness}/5 | {expression_label(expressiveness)} |

---

## Tone Rules

### T-01 · Formality Level
**Rule:** Write at a {formality_label(formality).lower()} register.
**Rationale:** Spectrum score {formality}/5 positions the brand here.

### T-02 · Emotional Orientation
**Rule:** Content should make clients feel:
{emotional_text or "- Confident in their investment"}

### T-03 · Expertise Balance
**Rule:** {expertise_label(expertise)} — {'Lead with your expertise and authority.' if expertise <= 2 else 'Lead with client outcomes and transformation.' if expertise >= 4 else 'Balance studio expertise with client benefit framing.'}

---

## Language Rules

### L-01 · Preferred Vocabulary
{vocab or "_(not yet defined — run /refine brand voice)_"}

### L-02 · Prohibited Language
{prohibited or "_(not yet defined — run /refine brand voice)_"}

### L-03 · Grammar & Style Rules
{rules_text or "_(not yet defined)_"}

---

## Content Topics (Priority Order)
{topics_text or "_(not yet defined)_"}

---

## Validation Checklist

Before publishing any content, confirm:
- [ ] Voice words present in headline or opening paragraph
- [ ] Formality register matches: {formality_label(formality)}
- [ ] Prohibited language scanned and removed
- [ ] Emotional goal met: reader should feel the intended emotion
- [ ] CTA style consistent: {cta_style or "_(to be defined)_"}
- [ ] Brand Voice gate ≥ 92% (auto-checked by /review)

---

*Generated by /brand command — Sovereign Universal AI Workspace v3.2*
*Compliance threshold: 92% — enforced by voice_validator.py*
"""


def generate_glossary(answers: dict) -> str:
    a = answers
    prohibited = a.get("prohibited_language", "")
    vocab = a.get("preferred_vocabulary", "")
    voice_words = a.get("voice_words", [])

    voice_list = "\n".join(
        f"| {w} | Use in headlines, openings, CTAs | High priority |"
        for w in (voice_words if isinstance(voice_words, list) else [voice_words])
        if w
    )

    return f"""---
version: "1.0"
generated_by: brand-consultant
generated_at: "{datetime.now(timezone.utc).isoformat()}"
status: "active"
---

# Sovereign — Brand Vocabulary Glossary

## Preferred Terms

| Term | Usage Context | Priority |
|------|--------------|----------|
{voice_list or "| _(to be populated)_ | — | — |"}

### Preferred Vocabulary Notes
{vocab or "_(Run /refine brand voice with existing copy to populate this section)_"}

---

## Prohibited Terms & Replacements

{prohibited or "_(Run /refine brand voice to define prohibited language list)_"}

### Universal Prohibitions (all Sovereign content)
| Avoid | Use Instead |
|-------|------------|
| cheap / affordable | investment-minded / value-driven |
| luxury (generic) | refined / considered / elevated |
| basically / just | _(remove entirely)_ |
| we think / we feel | _(state with confidence)_ |
| very / really | _(use a stronger single word)_ |

---

## Service & Category Terms

> Populate after /research competitors reveals industry language patterns.

---

*Generated by /brand command — Sovereign Universal AI Workspace v3.2*
"""


def generate_tone_examples(answers: dict) -> str:
    a = answers
    archetype = a.get("brand_archetype", "The Sage")
    voice_words = a.get("voice_words", [])
    voice_text = ", ".join(voice_words[:3]) if isinstance(voice_words, list) else str(voice_words)
    inspiration = a.get("voice_inspiration", "")
    anti_inspiration = a.get("anti_inspiration", "")
    cta_style = a.get("cta_style", "")
    existing_copy = a.get("existing_copy_sample", "")

    return f"""---
version: "1.0"
generated_by: brand-consultant
generated_at: "{datetime.now(timezone.utc).isoformat()}"
status: "active"
---

# Sovereign — Tone Examples & Reference

## Voice Reference

**Archetype:** {archetype}
**Core Voice Words:** {voice_text or "_(to be defined)_"}

---

## Brand Voice Inspirations

### Brands We Sound Like
{inspiration or "_(not yet specified — run /extract brand voice with inspiration references)_"}

### Brands We Do NOT Sound Like
{anti_inspiration or "_(not yet specified)_"}

---

## Existing Copy Sample

{f'> "{existing_copy}"' if existing_copy else "_(No existing copy provided — run /extract brand voice with your website or materials)_"}

---

## Tone Examples by Content Type

### Hero Headline (Website)
> *(Write in {archetype} voice — {voice_text})*
> *(Populate after /create website pages)*

### Blog Post Opening
> *(Write with {voice_text} register — confident, direct, no filler)*
> *(Populate after /create blog posts)*

### Service Description
> *(Authority-led but client-outcome-focused)*
> *(Populate after /create website pages)*

### CTA Style
**Approach:** {cta_style or "_(to be defined)_"}
**Examples:**
> *(Populate after /create landing pages)*

---

## On-Brand vs Off-Brand Matrix

| On-Brand | Off-Brand |
|----------|-----------|
| Specific, earned confidence | Generic claims ("the best") |
| Client transformation framing | Studio ego-centric copy |
| Precise design language | Vague lifestyle language |
| Direct, purposeful sentences | Filler phrases and hedging |
| {voice_text} register | _(opposite register)_ |

---

*Generated by /brand command — Sovereign Universal AI Workspace v3.2*
*Expand with /extract brand voice once copy assets are available*
"""


def generate_voice_refinement(answers: dict, session: dict) -> str:
    a = answers
    archetype = a.get("brand_archetype", "")
    stage = a.get("studio_stage", "")
    price = a.get("price_tier", "")
    spectrum = a.get("brand_spectrum", {})

    def score_to_descriptor(score, low, high):
        if score <= 2:
            return low
        if score >= 4:
            return high
        return f"balanced {low}/{high}"

    formality = score_to_descriptor(spectrum.get("formality", 3), "formal", "casual")
    seriousness = score_to_descriptor(spectrum.get("seriousness", 3), "serious", "warm")
    expertise = score_to_descriptor(spectrum.get("expertise", 3), "expert-led", "client-led")
    tradition = score_to_descriptor(spectrum.get("tradition", 3), "traditional", "contemporary")
    expression = score_to_descriptor(spectrum.get("expressiveness", 3), "reserved", "expressive")

    voice_words = a.get("voice_words", [])
    voice_text = ", ".join(voice_words) if isinstance(voice_words, list) else str(voice_words)

    diff = a.get("differentiators", [])
    diff_text = "\n".join(f"- {d}" for d in (diff if isinstance(diff, list) else [diff]))

    fears = a.get("client_fears", "")
    client_values = a.get("client_values", [])
    values_text = ", ".join(client_values) if isinstance(client_values, list) else str(client_values)

    return f"""---
version: "1.0"
generated_by: brand-consultant
generated_at: "{datetime.now(timezone.utc).isoformat()}"
status: "active"
refinement_round: 0
---

# Sovereign — Voice Refinement Log

## Session 0 — Brand Discovery Interview
*Source: /brand discovery interview*
*Completed: {session.get('completed_at', '')}*

---

## Brand Voice Synthesis

### Archetype Foundation
**{archetype}** — This archetype shapes every content decision.

### Voice Spectrum Summary
- Formality: **{formality}**
- Tone: **{seriousness}**
- Orientation: **{expertise}**
- Style: **{tradition}**
- Expression: **{expression}**

### Voice Words
{voice_text or "_(not yet defined)_"}

---

## Why This Voice Works for Sovereign

**Studio Stage:** {stage} — Voice should project {
    'emerging authority and focused expertise' if 'early' in str(stage).lower()
    else 'established credibility and selective clientele' if 'established' in str(stage).lower()
    else 'authority and selective positioning'
}.

**Price Tier:** {price} — Tone must justify premium investment without being defensive about price.

---

## Client Psychology Alignment

**What clients value:** {values_text or "_(not specified)_"}

**What clients fear:**
{fears or "_(not specified — consider adding client objections as voice signals)_"}

**Voice response to fear:** Content should preemptively address these anxieties through confident specificity rather than reassurance language.

---

## Differentiators → Voice Signals

{diff_text or "_(not specified)_"}

> Each differentiator should become a recurring content theme — told through work, not claimed directly.

---

## Next Refinement Steps

1. Run `/extract brand voice from [your website/materials]` to refine against real copy
2. Run `/create website pages` — first draft will apply this voice profile
3. Run `/review` — brand voice gate will score compliance at ≥ 92%
4. Add failed examples back here for continuous refinement

---

*Generated by /brand command — Sovereign Universal AI Workspace v3.2*
*Each /refine brand voice run appends a new session to this file*
"""


# ── File Writers ───────────────────────────────────────────────────────────────

def write_output_files(session: dict) -> dict:
    """Generate and write all brand output files. Returns paths dict."""
    answers = session.get("answers", {})
    BRAND_VOICE_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    files_written = {}

    # market-positioning.md
    mp_path = REFERENCE_DIR / "market-positioning.md"
    mp_path.write_text(generate_market_positioning(answers), encoding="utf-8")
    files_written["market_positioning"] = str(mp_path.relative_to(WORKSPACE_ROOT))

    # style-rules.md
    sr_path = BRAND_VOICE_DIR / "style-rules.md"
    sr_path.write_text(generate_style_rules(answers), encoding="utf-8")
    files_written["style_rules"] = str(sr_path.relative_to(WORKSPACE_ROOT))

    # glossary.md
    gl_path = BRAND_VOICE_DIR / "glossary.md"
    gl_path.write_text(generate_glossary(answers), encoding="utf-8")
    files_written["glossary"] = str(gl_path.relative_to(WORKSPACE_ROOT))

    # tone-examples.md
    te_path = BRAND_VOICE_DIR / "tone-examples.md"
    te_path.write_text(generate_tone_examples(answers), encoding="utf-8")
    files_written["tone_examples"] = str(te_path.relative_to(WORKSPACE_ROOT))

    # voice-refinement.md
    vr_path = BRAND_VOICE_DIR / "voice-refinement.md"
    vr_path.write_text(generate_voice_refinement(answers, session), encoding="utf-8")
    files_written["voice_refinement"] = str(vr_path.relative_to(WORKSPACE_ROOT))

    # brand-session.json (full session record)
    SESSION_LOG.write_text(json.dumps(session, indent=2, default=str), encoding="utf-8")
    files_written["session_log"] = str(SESSION_LOG.relative_to(WORKSPACE_ROOT))

    return files_written


def log_brand_session(session: dict, files_written: dict) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "brand_discovery_completed",
        "questions_answered": len([v for v in session.get("answers", {}).values() if v or v == 0]),
        "files_written": list(files_written.values()),
        "duration_seconds": _session_duration(session),
    }
    WORKFLOW_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(WORKFLOW_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def _session_duration(session: dict) -> int:
    try:
        start = datetime.fromisoformat(session["started_at"])
        end = datetime.fromisoformat(session["completed_at"])
        return int((end - start).total_seconds())
    except Exception:
        return 0


# ── Completion Summary ─────────────────────────────────────────────────────────

def show_completion_summary(session: dict, files_written: dict) -> None:
    answers = session.get("answers", {})
    answered = len([v for v in answers.values() if v or v == 0])
    total = len(answers)

    header("Brand Discovery Complete", "✓")
    print(f"  {GREEN}{answered}/{total} questions answered{RESET}")
    print(f"  {DIM}Duration: {_session_duration(session)}s{RESET}")
    print()
    print(f"  {BOLD}Files generated:{RESET}")
    for label, path in files_written.items():
        print(f"  {GREEN}✓{RESET}  {DIM}{path}{RESET}")
    print()
    print(hr("─", 60, DIM))
    print(f"  {BOLD}{CYAN}Suggested Next Step:{RESET}")
    print()
    print(f"  {WHITE}/research competitors{RESET}")
    print(f"  {DIM}→ Discover and register your competitive landscape{RESET}")
    print()
    print(f"  {DIM}Or if you have existing copy:{RESET}")
    print(f"  {WHITE}/extract brand voice from [your source]{RESET}")
    print(f"  {DIM}→ Refine voice rules with real examples{RESET}")
    print()
    print(hr("═", 60, CYAN))
    print()


# ── Main Entry Point ───────────────────────────────────────────────────────────

def run_brand_consultation() -> dict:
    """Main entry point: load questions → interview → generate files."""
    questions_data = load_questions()
    session = run_interview(questions_data)

    header("Generating Brand Files", "⟳")
    print(f"  {DIM}Synthesizing your answers into brand documents...{RESET}")
    print()

    files_written = write_output_files(session)
    log_brand_session(session, files_written)
    show_completion_summary(session, files_written)

    return {
        "status": "success",
        "files_written": files_written,
        "session": session,
    }


if __name__ == "__main__":
    try:
        result = run_brand_consultation()
        sys.exit(0)
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Session interrupted. Partial answers not saved.{RESET}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n  {YELLOW}ERROR: {e}{RESET}\n")
        raise
