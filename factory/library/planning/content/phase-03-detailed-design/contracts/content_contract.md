# Content Contract — Phase 03: Detailed Design
**Reasoning Hash:** sha256:aiwf-v21-launch-content-03-detailed-design-2026-04-25

---

## Quality Gate Thresholds

```yaml
seo_score_min: 85
brand_voice_score_min: 92
readability_score_min: 65       # Flesch-Kincaid
originality_max: 15             # % similarity to existing content
image_seo_score_min: 100        # alt text, file name, caption required
```

## Brand Voice Rules

**Tone:** authoritative-yet-accessible — technical depth without academic distance

**Forbidden language:**
- game-changing, revolutionary, disruptive, seamless, cutting-edge
- leverage (as verb), ecosystem (overused), unlock potential
- Any superlative without a concrete data point

**Preferred language:**
- sovereign, governance, factory, orchestration, density, spec, gate
- "builds in" not "adds on"
- "enforces" not "encourages"
- Numbers over adjectives ("12 files" not "many files")

## Channel Word Count Contracts

| Channel | Min | Target | Max |
|---------|-----|--------|-----|
| github | 800 | 1200 | 1500 |
| linkedin | 800 chars | 1100 chars | 1300 chars |
| x (single) | 180 | 240 | 280 |
| dev_to | 1200 | 1600 | 2000 |
| arabic_mena | 500 | 700 | 900 |

## CTA Placement Rules

| Channel | CTA Position | Link Placement |
|---------|-------------|----------------|
| linkedin | Final paragraph | First comment only (never body) |
| x | Final post in thread | Bio or reply |
| github | End of section | Inline href |
| dev_to | Final paragraph | Inline + canonical |
| arabic_mena | Final line | Direct link acceptable |

## Law 151/2020 Handling

Pieces with `law_151_flag: true` (C-07-AR-LI, C-08-AR-MENA) must:
1. Route through anonymisation step before Qwen adapter receives prompt
2. Remove all Egyptian user identifiers, location data, personal attributes
3. Log anonymisation event in tool_performance.jsonl with `error_code: null`
4. Never send raw persona research data to external LLM
