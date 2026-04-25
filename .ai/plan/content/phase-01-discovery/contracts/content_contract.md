# Content Contract — Phase 01: Discovery

**Contract Type:** Content / Brand Voice  
**Reasoning Hash:** sha256:aiwf-v21-launch-content-01-discovery-2026-04-25  

---

## Content Standards

```yaml
content_contract:
  id: "content-aiwf-v21-launch-discovery"
  planning_type: "content"

  brand_voice:
    tone: "authoritative-yet-accessible"
    personality:
      - "Sovereign and confident — this is built for builders who don't compromise on control"
      - "Precise and dense — no fluff, no clichés, every sentence earns its place"
      - "MENA-aware — acknowledges regional reality without being parochial"
      - "Systems-first — speaks in architectures, not features"
    forbidden_phrases:
      - "game-changing"
      - "revolutionary"
      - "disruptive"
      - "cutting-edge"
      - "seamless"
      - "leverage" (as a verb)
    preferred_language:
      - "sovereign" over "secure"
      - "governance" over "control"
      - "factory" over "framework"
      - "orchestration" over "management"

  quality_gates:
    seo_score_min: 85
    brand_voice_score_min: 92
    readability_score_min: 65
    originality_max: 15
    image_seo: 100

  format_rules:
    heading_structure: "H1 → H2 → H3 (no skipping)"
    cta_required: true
    arabic_version_required: "partial — 3 MENA-specific pieces in Phase 04"
    max_word_count_blog: 2000
    max_word_count_linkedin: 1300
    max_word_count_x_thread: 280_per_post
```

---

## Content Pillars (Discovery Phase)

| Pillar | Theme | Key Messages | Audience |
|--------|-------|--------------|----------|
| Sovereignty | AIWF is the only AI factory built for data residency by default | "Your AI stack, your jurisdiction" | All personas |
| Density | Plans that are production-ready before a single line of code | "12 spec files before you touch /dev" | Pragmatic Dev + Sovereign Builder |
| MENA-First | Law 151/2020 is not a constraint — it's a feature | "Built in Egypt. Certified for the region." | MENA Pioneer |
| Multi-LLM | One plan, seven CLI brains executing in parallel | "Claude + Gemini + Qwen. Governed." | AI Director |
