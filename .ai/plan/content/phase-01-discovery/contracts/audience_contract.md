# Audience Contract — Phase 01: Discovery

**Contract Type:** Audience / Persona Definition  
**Reasoning Hash:** sha256:aiwf-v21-launch-content-01-discovery-2026-04-25  

---

## Persona Usage Rules

```yaml
audience_contract:
  id: "aiwf-v21-audience-contract"
  version: "1.0.0"
  personas_count: 4

  usage_rules:
    - "All content must speak to at least 1 primary persona"
    - "GitHub content targets Pragmatic Dev first, Sovereign Builder second"
    - "LinkedIn targets Sovereign Builder + AI Director"
    - "X threads target Pragmatic Dev + AI community broadly"
    - "Arabic content targets MENA Pioneer exclusively"

  persona_validation:
    - "Each persona definition must include a 'signal source' — not invented"
    - "Personas are synthetic composites — no real individuals"
    - "Reviewed and updated at Phase 05 close with any new signals"

  law_151_rules:
    - "Egyptian persona demographic data is anonymised before external LLM prompts"
    - "No real Egyptian user PII may be stored outside Egypt"
```

---

## Persona Quick Reference

| ID | Name | Primary Channel | Primary Message | Pain Point Addressed |
|----|------|----------------|-----------------|---------------------|
| P1 | Sovereign Builder | LinkedIn | "Govern your entire AI stack, not just the model" | Vendor lock-in |
| P2 | Pragmatic Dev | GitHub | "From spec to code in one sovereign pipeline" | Integration friction |
| P3 | MENA Pioneer | MENA communities | "Law 151/2020 compliance built in, not bolted on" | Compliance anxiety |
| P4 | AI Director | LinkedIn / white papers | "Multi-LLM governance with a single OMEGA Gate" | Multi-LLM governance chaos |
