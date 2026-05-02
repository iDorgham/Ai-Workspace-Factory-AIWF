---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🕵️ Intelligence Extraction (Intel)

## Purpose
Enforce standards for high-performance data mining and business intelligence extraction. This skill focuses on the "Semantic Parsing" model—where agents identify critical market shifts, competitor moves, and regulatory changes from unstructured web data to provide actionable executive intel.

---

## Technique 1 — Multi-Source Semantic Aggregation
- **Rule**: Never rely on a single source for critical intelligence; always verify news or data points across at least 3 disparate sources (e.g., Official Gov Portal, Industry News, Social Sentiment).
- **Protocol**: 
    1. Define the "Indicator" (e.g., "New real estate regulations in Dubai").
    2. Scrape official gazettes, major news outlets (The National, Al Arabiya), and specialized industry boards.
    3. Use @Cortex to synthesize conflicting reports into a single "Confidence Score."

---

## Technique 2 — Entity-Relationship Mapping (ERM)
- **Rule**: Map the relationships between people, companies, and projects to identify hidden market influence loops.
- **Protocol**: 
    1. Extract key entities from unstructured articles.
    2. Map "Associations" (e.g., "Company X is a subsidiary of Group Y", "Person Z is a board member of both").
    3. Store results in a graph-compatible format (JSON-LD or direct Graph DB injection).

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Scraping "Dead" Data** | False intel / Cost waste | Check the "Recency" of every data source; ignore sources without a verified timestamp within the last 30 days. |
| **Ignoring Local Context** | Misinterpreted trends | Use localized agents (AR/EN) to ensure cultural and regulatory nuances (e.g., "Sharia compliance") are not missed. |
| **Over-Extraction (Noise)** | Information overload | Filter results through the "Executive Utility" lens: "Does this affect a planned or active project?". |

---

## Success Criteria (Intel QA)
- [ ] 0% critical market shifts missed within the monitoring scope.
- [ ] 95% + Accuracy in entity-relationship extraction.
- [ ] Intel reports are delivered in a "High-Density Executive Summary" format.
- [ ] Arabic regulatory changes are translated and contextualized within 1 hour of discovery.