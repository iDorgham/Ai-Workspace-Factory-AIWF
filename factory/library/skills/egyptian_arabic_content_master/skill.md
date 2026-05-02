```json
{
  "skill_id": "egyptian-arabic-content-master",
  "name": "Egyptian Arabic Content Master",
  "version": "1.2.0",
  "description": "Humanized Egyptian Arabic (Masri) for web, blogs, ads, social, video VO/supers, B2B comms, storytelling, and humour—plus channel playbooks, contracts/brief_schema + pack_router_map, evaluation rubric + golden pairs, vertical stubs, and legal-adjacent UX guardrails (not a substitute for counsel). Bilingual prompt templates in prompt_library/en/.",
  "locales": ["ar-eg", "en"],
  "commands": [],
  "agents": [],
  "protocols": [
    "Load main persona from pack: factory/library/skills/egyptian_arabic_content_master/egyptian_arabic_content_master.md",
    "Use tone_matrix.md for tone selection; humour_guidelines.md gates wit; channel_formats.md for surface-specific length and structure",
    "For privacy/terms/marketing summaries use legal_and_contracts_guidance.md; never invent binding clauses",
    "Use prompt_library/ (Arabic) and prompt_library/en/ (English) plus examples/ (video, business, legal plain-language) for few-shots",
    "When brief is structured, validate against contracts/brief_schema.yaml; use contracts/pack_router_map.yaml for advisory example+prompt paths",
    "Score or self-check long assets with evaluation/rubric_masri.md; compare risky lines to evaluation/golden_pairs.jsonl",
    "For sector depth load verticals/<sector>.md when present alongside industry_guidelines.md"
  ],
  "pack_path": "factory/library/skills/egyptian_arabic_content_master/",
  "timestamp": "2026-05-02T18:00:00+03:00"
}
```
