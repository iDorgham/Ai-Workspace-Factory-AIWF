# Content Contract — {{PHASE_NAME}}

**Contract Type:** Content / Brand Voice  
**Planning Type:** {{PLANNING_TYPE}}  
**Reasoning Hash:** {{REASONING_HASH}}  

---

## Content Standards

```yaml
content_contract:
  id: "{{CONTRACT_ID}}"
  planning_type: "{{PLANNING_TYPE}}"

  brand_voice:
    tone: "{{professional|conversational|authoritative|empathetic}}"
    personality: ["{{TRAIT_1}}", "{{TRAIT_2}}"]
    forbidden_phrases: ["{{PHRASE_1}}", "{{PHRASE_2}}"]

  quality_gates:
    seo_score_min: 85
    brand_voice_score_min: 92
    readability_score_min: 65
    originality_max: 15
    image_seo: 100

  format_rules:
    max_word_count: "{{N}}"
    heading_structure: "H1 → H2 → H3 (no skipping)"
    cta_required: true
    arabic_version_required: "{{yes|no}}"

  law_151_content:
    personal_data_in_content: "{{yes|no}}"
    data_subject_consent_required: "{{yes|no}}"
```

---

## Content Pillars (for this phase)

| Pillar | Theme | Key Messages | Target Audience |
|--------|-------|--------------|-----------------|
| {{PILLAR_1}} | {{THEME}} | {{MESSAGES}} | {{AUDIENCE}} |
| {{PILLAR_2}} | {{THEME}} | {{MESSAGES}} | {{AUDIENCE}} |

---

## Approval Workflow

1. Draft → spec_architect_v2 review
2. Brand voice score ≥ 92% → auto-approve
3. Below threshold → human review required
