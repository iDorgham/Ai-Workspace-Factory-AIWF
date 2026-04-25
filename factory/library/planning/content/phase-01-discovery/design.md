# Design Document — Phase 01: Discovery

**Planning Type:** content  
**Reasoning Hash:** sha256:aiwf-v21-launch-content-01-discovery-2026-04-25  

---

## 1. System Context

See `c4-context.mmd`. Three audience archetypes reach the AIWF content system through
distinct channels: founders via LinkedIn thought leadership, developers via GitHub technical
docs, and MENA developers via Arabic-adapted community content. All three must be served
from a single coherent content architecture — differentiated by format and depth, unified
by brand voice and sovereignty positioning.

---

## 2. Container Architecture

See `c4-containers.mmd`. Discovery is handled by four modular components:

- **Audience Research Module** — produces persona definitions and format preferences
- **Content Audit Module** — scans existing AIWF assets and scores each against quality gates
- **Competitor Map** — brainstorm_agent surveys LangChain, CrewAI, and AutoGen positioning
- **Channel Priority Matrix** — weighs audience fit × reach × production cost per channel

All outputs land in `.ai/plan/content/phase-01-discovery/` and are validated by the Law 151
compliance gate before the phase activates.

---

## 3. Data Flow

```
workspace_docs (docs/, .ai/, README)
  → [content_audit scans + scores]
  → discovery_store/domain_model.md#content-asset-inventory

brainstorm_agent (competitive signals)
  → [competitor analysis]
  → discovery_store/domain_model.md#competitor-content-map

spec_architect_v2 (persona synthesis)
  → [audience research]
  → discovery_store/domain_model.md#audience-personas

discovery_store
  → [compliance_check validates personal data handling]
  → phase APPROVED → blocks phase-02-blueprint
```

---

## 4. Key Design Decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| Persona count | 2–3 minimal vs 4–6 comprehensive | 4 personas | Covers all primary acquisition paths without over-segmenting |
| Competitor scope | Adjacent tools only vs full market | 3 direct + positioning map | Enough to differentiate; avoid analysis paralysis in discovery |
| Arabic content scope | Full Arabic vs English-first | English-first, Arabic-adapted for MENA channel | Resources constraint; MENA Pioneer reads EN; Arabic is differentiation, not primary |
| Channel sequencing | GitHub → then all others | GitHub first (P1), then LinkedIn + X simultaneously | Developer credibility gates all other content trust |

---

## 5. Design Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Persona assumptions not validated by real users | Medium | High | Flag as hypotheses; mark for validation in Phase 05 |
| Competitor analysis stale within 30 days | High | Low | Date-stamp all competitor entries; refresh at Phase 04 |
| Arabic content scope creep delaying launch | Medium | Medium | Strictly cap at 3 MENA-specific pieces in Phase 04 |
