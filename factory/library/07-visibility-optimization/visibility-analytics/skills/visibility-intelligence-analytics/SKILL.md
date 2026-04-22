# 📊 Visibility Intelligence Analytics (The Search Engine of the Future)

## Purpose
Enforce professional standards for measuring success in the **Post-Traditional SEO era**. This skill focuses on tracking **AEO, GEO, and LLMO impact** using advanced tools like SearchLabs, Perplexity, and custom LLM benchmarking logic.

---

## Technique 1 — GEO & SGE Verification (SearchLabs)

### AI Overview Tracking
- **The Protocol**: Use the **Google SearchLabs (SGE)** interface to manually verify the synthesized answer for core commercial keywords.
- **Metric: Citation Density (CD)**: Calculate the number of times the brand URL appears in the carousel or the "Sources" dropdown of an AI Overview.
- **Metric: Sentiment Sync**: Use LLM-based analysis (e.g., GPT-4o) to determine if the SGE response represents the brand favorably.

---

## Technique 2 — AEO & Voice Performance Scoring

- **Metric: Zero-Click Share**: Tracking the delta between "Impressions" and "Clicks" — a high impression/low click ratio in Google Search Console (GSC) for the "Answer" snippet indicates AEO success.
- **Voice Recognition (VR) Index**: Testing voice-only triggers (Siri, Alexa, Google) to ensure the brand answer is the "Default Choice" for the category.

---

## Technique 3 — LLMO Benchmarking (The Conversation Loop)

- **Metric: Perplexity Citation Index (PCI)**: Use Perplexity's API (or manual prompt testing) to determine how many times the brand is cited in a thread of 5 related conversational follow-ups.
- **Metric: LLM Brand-Awareness**: Querying models (ChatGPT, Claude) without internet access to determine if the brand is in their pre-training weights (Static LLMO).

---

## 🛠️ Tool Integration Protocols

| Tool | Focus | Dashboard Metric |
| :--- | :--- | :--- |
| **GSC (Search Console)** | Snippets / GSC Overviews | "Knowledge Graph Impression Share" |
| **Perplexity** | Citation Probability | "Link-out Ratio" |
| **SearchLabs** | SGE Placement | "Carousel Position (1-5)" |
| **Custom Python Script** | Sentiment Tracking | "AI-Synthesized Bias Score" |

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Tracking Clicks Only** | Misjudging AEO value | Measure "Impressions on Answer Boxes" instead of just CTR. |
| **Ignoring Conversational Flow** | Fragmented data | Benchmark the LLM across a *sequence* of prompts to see if the brand "Stays in Mind." |
| **Lagging Verification** | Missing AI shifts | Audit the AI overviews weekly; the SGE/GEO environment changes faster than traditional SERPs. |

---

## Success Criteria (Analytics QA)
- [ ] Weekly report includes "Generative Citation Share."
- [ ] GSC data is filtered for "Rich Result" and "Snippet" visibility.
- [ ] Manual Perplexity testing shows brand authority for top-3 ICP queries.
- [ ] Bias analysis shows "Neutral-Authoritative" synthesis by all major models.