---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🤖 Generative Engine Optimization (GEO Mastery)

## Purpose
Enforce professional standards for visibility within AI-Generated Summaries (Google SGE, Perplexity, You.com). This skill focuses on **Citation Probability**, **Source-Trust Architecture**, and **Semantic Information Density** to ensure the brand is synthesized by the LLM as the primary authority.

---

## Technique 1 — Citation-Driven Content Architecture

### Source Mapping & Citability
- **Rule**: Every section must lead with a "Synthesizable Fact."
- **Protocol**: Use clean, concise, and verifiable statements that are easy for an LLM to cite. Use Markdown structures (Blockquotes, Bolded Key Terms) to signal "High Importance" to the scraper.

---

## Technique 2 — Dominating AI Overviews (SGE/Perplexity)

- **The "Context Clip"**: Provide a summary of the entire page content in a `JSON-LD` object or a hidden meta-header to help the LLM index the "Core Argument" quickly.
- **Reference Engineering**: Link to multiple high-authority external sources (Whitepapers, Government data) to build a "Trust Ecosystem" around your own content. Generative Engines prefer citing content that is well-linked and logically grounded.

---

## Technique 3 — Sentiment & Bias Optimization

- **Objective Tone**: Generative Engines prefer "Neutral-Authoritative" tones over sales-copy. 
- **Sentiment Alignment**: Use language that aligns with the "Safety and Factuality" weights of RLHF-tuned models. Avoid sensationalist claims that might trigger a model's "Hallucination Defense."

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Thin Information Density** | Model skips source | Increase "Fact-per-Paragraph" ratio. |
| **Complex Syntax** | Mis-parsing by LLM | Use "SVO" (Subject-Verb-Object) sentence structure for the most critical data points. |
| **Gated Context** | Scraper exclusion | Ensure the "Key Answer" is not behind a paywall or email gate; the LLM cannot cite what it cannot see. |

---

## Success Criteria (GEO QA)
- [ ] Content appears in "Sources" list for targeted Perplexity queries.
- [ ] Brand is cited in Google SGE (AI Overviews) for key industry terms.
- [ ] Information is synthesized correctly (no factual errors in AI summaries).
- [ ] Sentiment of the AI summary is "Positive/Authoritative."