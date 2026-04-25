# Regional Compliance — Phase 01: Discovery

**Law:** Egypt Law 151/2020 on Personal Data Protection  
**Phase:** 01 — Discovery  
**Planning Type:** content  
**Compliance Status:** PENDING — complete before phase activates  
**Reasoning Hash:** sha256:aiwf-v21-launch-content-01-discovery-2026-04-25  

---

## 1. Data Residency Assessment

| Data Type | Storage Location | Processing Location | Law 151 Compliant | Notes |
|-----------|-----------------|---------------------|-------------------|-------|
| Audience persona definitions | `.ai/plan/content/` (Egypt server) | Egypt | ✅ Yes | Anonymised; no real individuals |
| Content audit scores | `.ai/plan/content/` (Egypt server) | Egypt | ✅ Yes | Document metadata only |
| Competitor research data | `.ai/plan/content/` (Egypt server) | Egypt | ✅ Yes | Publicly available data; no PII |
| Egyptian user demographic signals | Egypt only | Egypt | ✅ Yes | Must NOT be sent to foreign LLM APIs without anonymisation |

**Key Rule:** When using multi-CLI adapters (Gemini, GPT-based tools) to generate content
about Egyptian users, all personal data must be anonymised or synthesised before being
included in prompts sent to non-Egypt-hosted APIs.

---

## 2. MENA Adaptations

- **Arabic Language:** Required for MENA Pioneer persona; English-first with Arabic-adapted variant
- **RTL Layout:** Applicable to Arabic content output (Phase 04)
- **Local Payment Methods:** Not applicable in discovery phase
- **Cultural Sensitivity Review:** Required before any Arabic content is published (Phase 04/05)

---

## 3. Geofencing Rules

```yaml
geofence:
  primary_region: egypt
  allowed_regions: [egypt, uae, ksa, jordan, kuwait]
  blocked_regions: [any_non_approved_offshore]
  enforcement: OMEGA_GATE_V3
  persona_data_scope: anonymised_only_for_external_llms
```

---

## 4. Compliance Checklist

- [ ] All audience personas are synthetic composites — no real individual's data
- [ ] Persona storage confirmed in `.ai/plan/content/` (Egypt-hosted AIWF)
- [ ] Any Egyptian demographic signals anonymised before inclusion in external LLM prompts
- [ ] Arabic content scope decision documented (English-first confirmed)
- [ ] OMEGA Gate v3 sovereignty certificate generated on phase activation

---

## 5. Decision: Arabic Content Scope

**Decision:** English-first, Arabic-adapted  
**Rationale:** MENA Pioneer persona reads English; Arabic adaptation is a differentiation layer,
not the primary channel. Producing full Arabic content from Phase 01 would delay launch.
Full Arabic content strategy deferred to a dedicated `seo/` or `branding/` plan type post-launch.

**Arabic deliverables committed for launch:** 3 pieces (1 LinkedIn post, 1 GitHub README section, 1 community post)
