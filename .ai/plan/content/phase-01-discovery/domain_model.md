# Domain Model — Phase 01: Discovery

**Planning Type:** content  
**Reasoning Hash:** sha256:aiwf-v21-launch-content-01-discovery-2026-04-25  

---

## 1. Audience Personas

| Persona | Role | Region | Pain Point | AIWF Use Case | Preferred Format |
|---------|------|--------|------------|---------------|-----------------|
| **The Sovereign Builder** | AI-native founder, 28–42 | Egypt / Gulf | Vendor lock-in; data residency risk | Full AIWF deployment for client products | Long-form technical posts, architecture diagrams |
| **The Pragmatic Dev** | Senior engineer, 26–38 | Global (EN) | Integration friction; poor AI tooling docs | AIWF library + adapters for their stack | GitHub README, code examples, short tutorials |
| **The MENA Pioneer** | Tech lead / CTO, 30–45 | MENA | Law 151/2020 compliance anxiety; limited local tooling | AIWF as sovereign infrastructure for MENA clients | Arabic + English; webinars; community posts |
| **The AI Director** | Head of AI / CTO, 35–50 | Regional enterprise | Governance gaps; multi-LLM chaos | AIWF OMEGA Gate + tripartite planning as governance layer | Executive summaries; case studies; white papers |

---

## 2. Content Asset Inventory (Audit Baseline)

| Asset | Path | Type | Quality Signal | Gap |
|-------|------|------|---------------|-----|
| Main README | README.md | Overview | Unknown — needs audit | Developer onboarding clarity |
| PRD 2026-04-24 | .ai/plan/development/00_prd/ | Internal spec | High density; not public | No public-facing version |
| Dashboard | .ai/dashboard/index.md | Status | 0 strategic patterns | Not suitable for external content |
| Fix Plans | docs/01-plans/*.md | Governance | SDD-quality, internal | Not adapted for audience consumption |
| Health Audit | .ai/logs/health_audit_report.md | Internal | 85/100; internal only | Public health story not told |

---

## 3. Competitor Content Map

| Competitor | Positioning | Primary Channel | Strength | Weakness vs AIWF |
|-----------|-------------|-----------------|----------|-----------------|
| LangChain | "Framework for LLM apps" | GitHub + docs site | Massive ecosystem, great tutorials | No sovereignty; no Law 151; US-centric |
| CrewAI | "Multi-agent collaboration" | X + GitHub | Active community; founder-led voice | No MENA; no governance layer; no SDD |
| AutoGen | "Conversational agent framework" | GitHub + papers | Research credibility | Academic tone; no production governance |

**AIWF Differentiation:** Sovereign by default. Law 151/2020 native. SDD methodology. Multi-CLI orchestration. OMEGA Gate. Egyptian-built.

---

## 4. Channel Priority Matrix

| Channel | Audience Fit | Reach | Production Cost | Priority | Content Type |
|---------|-------------|-------|-----------------|----------|--------------|
| GitHub README + Docs | Developer (P1) | High | Low | **P1** | Technical overview, quick-start |
| LinkedIn | Founder + Director | Medium-High | Medium | **P2** | Thought leadership, case studies |
| X (Twitter) | Developer + AI community | High | Low | **P2** | Short announcements, architecture threads |
| Dev.to / HackerNews | Senior Dev | Medium | Medium | **P3** | Deep-dive technical posts |
| Arabic MENA Community | MENA Pioneer | Medium | High | **P3** | Arabic-adapted content, compliance guides |

---

## 5. Content Objectives (SMART)

| Objective | Metric | Baseline | Target (30d post-launch) | Owner |
|-----------|--------|----------|--------------------------|-------|
| Developer awareness | GitHub stars | Current count | +200 | brainstorm_agent |
| MENA positioning | Arabic content pieces | 0 | 3 | content production team |
| Thought leadership | LinkedIn impressions | 0 | 5,000 | Dorgham (founder voice) |
| Technical credibility | README clarity score | Unknown | SEO ≥85, Readability ≥65 | spec_architect_v2 |

---

## 6. Glossary

| Term | Definition | Slug |
|------|------------|------|
| Sovereign Content | Content produced under AIWF governance with Law 151/2020 compliance | `sovereign_content` |
| Tripartite Planning | AIWF v21 multi-type planning system (development + content + N types) | `tripartite_planning` |
| OMEGA Gate | 12-point sovereignty verification gate that all activations pass through | `omega_gate` |
| MENA Pioneer | Persona for MENA tech leads using AIWF for regional compliance | `mena_pioneer` |
