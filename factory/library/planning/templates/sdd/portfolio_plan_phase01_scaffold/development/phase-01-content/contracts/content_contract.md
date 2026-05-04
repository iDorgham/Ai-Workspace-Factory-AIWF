# Content contract — quality + brand (phase 01)

**Contract type:** Content / brand voice  
**Planning type:** content  
**Reasoning hash:** sha256:portfolio-website-content-phase01-2026-05-04  

---

## Content standards

```yaml
content_contract:
  id: "portfolio-content-v1"
  planning_type: "content"

  brand_voice:
    tone: "TBD — align with client workshop"
    personality: ["TBD", "TBD"]
    forbidden_phrases: ["TBD"]

  quality_gates:
    seo_score_min: 85
    brand_voice_score_min: 92
    readability_score_min: 65
    originality_max: 15
    image_seo: 100

  format_rules:
    heading_structure: "H1 → H2 → H3 (no skipping)"
    cta_required: true
    arabic_version_required: "yes"

  law_151_content:
    personal_data_in_content: "yes_if_forms"
    data_subject_consent_required: "yes_where_tracking"
```

---

## Image specs

- Alt text required; decorative images use empty alt with `role="presentation"` pattern per HTML spec.  
- Max dimensions and formats per hosting/CDN choice (document in PRD).

---

## Approval workflow

1. Draft in CMS → editor review  
2. Brand voice + SEO gates from table above  
3. Publish only from `APPROVED` state (see state_contract.md)
