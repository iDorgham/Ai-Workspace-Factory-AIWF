---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🤖 LLMO Audit (Large Language Model Optimization) — 2026 Edition

## Purpose
Run a complete audit that measures how well your website/brand/content is **understood, trusted, and cited** by frontier Large Language Models (ChatGPT, Grok, Claude, Gemini, Perplexity, etc.).

---

## Success Criteria
- [ ] **LLMO Health Score** ≥ 88/100
- [ ] Minimum **4 direct LLM citation opportunities** identified
- [ ] Strong **entity recognition** and authority signals across models
- [ ] Zero critical gaps in **training-data-friendly signals**
- [ ] **MENA-specific LLM signals** validated (Arabic entity strength, local trust signals)

---

## 2026 LLMO Ranking Factors Checklist (Weight-based)

### 1. Entity Recognition & Authority (Weight: 97)
- Clear, consistent entity signals for brand, authors, and topics.
- Strong co-occurrence with high-trust entities in training data.

### 2. Citation Probability Score (Weight: 95)
- How likely each LLM is to directly quote or reference you.
- Tested across 6 major models (ChatGPT-4o, Grok-3, Claude-3.5, Gemini-2.0, Perplexity, etc.).

### 3. Training-Data-Friendly Structure (Weight: 94)
- Clean, natural language with zero-fluff answers.
- High information density in first 200 words.
- Unique insights that models cannot easily synthesize elsewhere.

### 4. Structured Data for LLMs (Weight: 93)
- Advanced Schema.org (Speakable, Entity, Citation, FAQPage).
- JSON-LD optimized for LLM parsing.
- Machine-readable author and brand signals.

### 5. Freshness & Version Control (Weight: 92)
- Accurate last-modified timestamps.
- "As of [date]" markers.
- Clear version history for evolving topics.

### 6. Author & Brand Trust Signals (Weight: 90)
- Verified author pages with strong E-E-A-T (Experience, Expertise, Authoritativeness, Trust).
- Consistent bylines and professional profiles.

### 7. MENA-Specific LLM Signals (Weight: 88)
- Strong Arabic entity recognition.
- Local authority signals (UAE, Saudi, Egypt government & business directories).
- Culturally aligned content patterns.
- Bilingual AR/EN signals for dual-language models.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Generic Content** | Model ignores | Inject proprietary data and unique MENA-specific case studies. |
| **Missing Schema** | Parsing failure | Deploy JSON-LD `Citation` and `Entity` markup immediately. |
| **Outdated Info** | Trust score drop | Use "As of [date]" markers to signal freshness to crawlers. |
| **Weak Brand Signals** | Entity confusion | Standardize brand name and founder bio across all 3rd party directories. |

---

## 📋 Strategic LLMO Roadmap (30/60/90 Days)

### Phase 1: Entity Cleanup (Day 1-30)
- Resolve naming inconsistencies across the web.
- Claim and optimize high-authority local business profiles.

### Phase 2: Structural Optimization (Day 31-60)
- Deploy LLM-specific JSON-LD markup.
- Refactor top-performing content into high-density natural language.

### Phase 3: Authority Amplification (Day 61-90)
- Execute PR strategy targeting training-data source sites.
- Expand bilingual Arabic/English entity signals.

---

## Output Format
1. **LLMO Health Score** (0–100) with per-factor breakdown.
2. **Current Citation Status** per model.
3. **Critical Gaps & Quick Wins**.
4. **Exact Markup Fixes** (Copy-paste ready).
5. **Projected Citation Lift** after implementation.