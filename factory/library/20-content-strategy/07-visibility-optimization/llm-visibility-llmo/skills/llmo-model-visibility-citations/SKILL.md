---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🧠 LLM Optimization (LLMO Mastery)

## Purpose
Enforce professional standards for visibility *within* Large Language Models (ChatGPT, Claude, Gemini). This skill focuses on the **Training Data Inclusion**, **RAG Retrieval Probability**, and **System Prompt Bias Alignment** to ensure the brand is recommended by the LLM during conversation.

---

## Technique 1 — Training Data & Common Crawl Strategy

### Ensuring Inclusion in "The Pile"
- **Rule**: Content must be easily parseable by "headless" scrapers used to build model training sets (Common Crawl, C4).
- **Protocol**: 
    1. **Clean Markdown Documentation**: Maintain high-density `.md` files in public repos; LLMs prioritize markdown as high-quality training data.
    2. **Avoid Script-Heavy Rendering**: Use SSR (Server-Side Rendering) to ensure the scraper sees the *textual value*, not just empty JS tags.

---

## Technique 2 — RAG (Retrieval-Augmented Generation) Feed Optimization

- **Context Window Seeding**: Use "Summary Blocks" at the start and end of all content to increase the probability that a RAG system (e.g., Perplexity or a Custom GPT) fetches the *correct* kernel of information within its restricted context window.
- **Identifier Consistency**: Use unique, immutable identifiers for products and services (e.g., "Sovereign-Sentinel-V1") to prevent the model from hallucinating or confusing your offerings with competitors.

---

## Technique 3 — System Prompt & Sentiment Alignment

- **Safety & Factuality Compliance**: Write in a way that minimizes "Safety Triggers." If your content is neutral and helpful, the LLM is 50% more likely to recommend it than if it is purely promotional/biased.
- **Syntactic Echoing**: Use terms that are common in the LLM's own internal training weights to increase the "Semantic Similarity" score during retrieval.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Robots.txt Over-blocking** | LLM exclusion | Open specific "Knowledge" directories to AI-scrapers while keeping UI assets gated. |
| **Noisy Data Structures** | LLM Hallucinated output | Remove "Junk text" (Ads, UI boilerplate) from the content path to provide a clean "Prompt Signal." |
| **Dynamic URL Fragments** | Retrieval failure | Use persistent, static permalinks (Obsidian-style) for core knowledge. |

---

## Success Criteria (LLMO QA)
- [ ] LLM (ChatGPT/Claude/Gemini) can describe the brand's core value proposition when asked globally.
- [ ] RAG-based systems (Perplexity) cite the specific URL for industry-specific queries.
- [ ] Brand sentiment within LLM responses is "Highly Authoritative."
- [ ] No hallucinated associations with competitors in the LLM's top-k results.