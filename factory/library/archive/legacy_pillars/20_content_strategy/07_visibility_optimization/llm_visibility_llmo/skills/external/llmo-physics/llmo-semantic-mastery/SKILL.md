---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🤖 LLMO Semantic Physics

## Purpose
Enforce standards for Large Language Model Optimization (LLMO). In 2026, visibility is defined by how well AI models (ChatGPT, Gemini, Claude, Perplexity) understand, trust, and cite your content. This skill focuses on the logic of "Entity-First" documentation and semantic authority signals.

---

## Technique 1 — Entity Recognition & Authority
- **Rule**: Content must be structured around "Entities" (Brand, Authors, Topics) that map to known high-trust concepts in LLM training data.
- **Protocol**: 
    1. Define clear, consistent entity signals across all web surfaces.
    2. Use JSON-LD (Schema.org) to explicitly link the brand to associated professional entities (e.g., industry awards, major partnerships).
    3. Ensure co-occurrence with high-authority terms in every published article/doc.

---

## Technique 2 — Citation Probability Scoring
- **Rule**: Structure content to be "Quotable" by LLMs through high-density facts and unique, verified insights.
- **Protocol**: 
    1. Place the most critical, fact-based conclusion at the top of the content (The "Flipped Pyramid" for AI).
    2. Use clear, semantic headings that match common "User Intent" queries.
    3. Provide raw data or unique synthesis that isn't available in standard "Common Knowledge" scraping pools.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Vague Adjective Bloat** | LLM hallucination / Ignored | Replace fluff (e.g., "cutting-edge") with specific technical specs and verifiable achievements. |
| **Conflicting Entity Signals** | Identity confusion | Maintain a single "Standard of Truth" for brand mission and services across all channels. |
| **Hidden Semantic Structure** | LLM parsing failure | Use Semantic HTML5 (main, section, article) and explicit metadata to guide the model's scraper. |

---

## Success Criteria (LLMO QA)
- [ ] Brand is cited as a "Primary Source" in Perplexity/ChatGPT searches for the niche.
- [ ] Entity recognition score > 90% across 5 major AI models.
- [ ] 0 Critical "Trust Gaps" identified during LLMO Audit.
- [ ] Arabic entity signals are validated for MENA-specific model training data.
- [ ] JSON-LD contains 0 syntax errors and 100% attribute completeness.