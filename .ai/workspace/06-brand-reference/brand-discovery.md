# Brand Discovery — Agent Contract & Interview Protocol
# ======================================================
# Owner: brand-agent / brand-consultant sub-agent
# Trigger: /brand command
# ======================================================

## Purpose

The `/brand` command initiates a structured brand discovery session — a professional-grade consultation interview that collects the foundational inputs required to generate:

- `content/sovereign/reference/market-positioning.md` — niche, clients, USPs, pricing tier
- `content/sovereign/reference/brand-voice/style-rules.md` — tone rules, language rules, compliance validators
- `content/sovereign/reference/brand-voice/glossary.md` — preferred vocabulary + prohibited terms
- `content/sovereign/reference/brand-voice/tone-examples.md` — on-brand vs off-brand reference
- `content/sovereign/reference/brand-voice/voice-refinement.md` — iterative refinement log (session 0)

**These files are prerequisites for `/create`, `/polish`, and the brand voice quality gate (≥ 92%).**

---

## Sub-Agent: brand-consultant

### Identity
- **Script:** `.ai/scripts/brand/brand_consultant.py`
- **Question Bank:** `.ai/templates/brand-discovery/questions.json`
- **Mode:** Interactive CLI interview (28 questions, 7 phases)
- **Run Duration:** Typically 10–25 minutes

### Input
```json
{
  "trigger": "/brand",
  "questions_source": ".ai/templates/brand-discovery/questions.json",
  "session_user": "workspace operator"
}
```

### Output Contract
```json
{
  "status": "success | error | interrupted",
  "files_written": {
    "market_positioning": "content/sovereign/reference/market-positioning.md",
    "style_rules": "content/sovereign/reference/brand-voice/style-rules.md",
    "glossary": "content/sovereign/reference/brand-voice/glossary.md",
    "tone_examples": "content/sovereign/reference/brand-voice/tone-examples.md",
    "voice_refinement": "content/sovereign/reference/brand-voice/voice-refinement.md",
    "session_log": "logs/brand-session-[timestamp].json"
  },
  "session": {
    "started_at": "<ISO 8601>",
    "completed_at": "<ISO 8601>",
    "answers": { "<output_field>": "<value>" }
  }
}
```

### Files Owned (brand-consultant is the SOLE writer of these)
| File | Notes |
|------|-------|
| `content/sovereign/reference/market-positioning.md` | Overwritten on each `/brand` run (versioned as `_v2.md` if exists) |
| `content/sovereign/reference/brand-voice/style-rules.md` | Overwritten on each `/brand` run |
| `content/sovereign/reference/brand-voice/glossary.md` | Overwritten on each `/brand` run |
| `content/sovereign/reference/brand-voice/tone-examples.md` | Overwritten on each `/brand` run |
| `content/sovereign/reference/brand-voice/voice-refinement.md` | Session 0 base; `/refine brand voice` appends new sessions |
| `logs/brand-session-[timestamp].json` | Full answer record for re-runs or debugging |

---

## Interview Protocol

### Structure
- **Total Questions:** 28
- **Question Types:** `single_choice`, `single_choice_with_other`, `multi_choice`, `multi_choice_with_other`, `open_text`, `spectrum_grid`
- **Required Questions:** 18 (hard required — user cannot skip)
- **Optional Questions:** 10 (press Enter to skip)

### Phase Map

| Phase | ID | Name | Questions | Purpose |
|-------|----|------|-----------|---------|
| 1 | `foundation` | Brand Foundation | Q1–Q4 | Core identity anchors |
| 2 | `audience` | Target Audience | Q5–Q8 | Client psychology |
| 3 | `personality` | Brand Personality | Q9–Q11 | Archetype + spectrum |
| 4 | `positioning` | Market Positioning | Q12–Q15 | Competitive differentiation |
| 5 | `voice` | Voice & Language | Q16–Q20 | Tone rules + vocabulary |
| 6 | `content` | Content Strategy | Q21–Q23 | Topics + formats + SEO |
| 7 | `reference` | Reference Material | Q24–Q28 | Inspiration + existing copy |

### Spectrum Grid (Q11)

The spectrum grid presents 5 brand personality scales, each scored 1–5:

| Scale | Left Pole (1) | Right Pole (5) |
|-------|--------------|----------------|
| Formality | Formal | Casual |
| Tone | Serious | Playful |
| Expertise Orientation | Expert-led | Client-led |
| Style Tradition | Traditional | Contemporary |
| Expressiveness | Reserved | Expressive |

Scores feed directly into `style-rules.md` tone rule thresholds.

---

## Validation Rules

1. **Required fields:** brand-consultant enforces required fields — will re-prompt until answered.
2. **max_selections:** Multi-choice questions enforce selection limits.
3. **Interruption:** If the user interrupts (Ctrl+C), no files are written and session is not logged.
4. **Re-run behavior:** If output files already exist, brand-consultant creates versioned backups (`_v2.md`, `_v3.md`) before overwriting.

---

## Downstream Integration

After `/brand` completes:

| Command | What It Uses |
|---------|-------------|
| `/extract brand voice from [source]` | Reads `voice-refinement.md` as baseline; refines `style-rules.md` |
| `/refine brand voice` | Appends session N+1 to `voice-refinement.md` |
| `/create *` | Loads `style-rules.md` + `glossary.md` before generating any content |
| `/review` | Brand Voice gate scores against `style-rules.md` rules (≥ 92%) |
| `/research competitors` | Uses `market-positioning.md` to identify competitor tier |

---

## Error Handling

| Error | Action |
|-------|--------|
| `questions.json` missing | HALT — print path, exit 1 |
| File write failure | Retry 3× → log to `workflow.jsonl` → skip file, continue |
| Brand voice gate fails after content creation | `/refine brand voice` → re-run `/review` |
| Duplicate run (files exist) | Version existing files (`_v2`, `_v3`) before overwriting |
| User interrupts mid-session | Exit cleanly — no partial files written |

---

## Suggested Follow-up After `/brand`

```
💡 Suggested Next Step: /research competitors
   → Then: /extract brand voice from [source]
   → Then: /create website pages
```

---

*Owner: brand-agent*
*Sub-agent: brand-consultant*
*Version: 1.0*
*Workspace: Sovereign Universal AI Workspace v3.2*
