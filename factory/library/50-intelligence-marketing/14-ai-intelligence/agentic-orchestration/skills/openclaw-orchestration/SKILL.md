# 🦀 OpenClaw Orchestration (Autonomous Intelligence)


## Purpose
Direct the deployment of OpenClaw (https://openclaw.ai/) for autonomous web crawling, data synthesis, and agentic task execution. This skill provides the protocols for managing the Claw's resources and ensuring high-density data extraction without triggering bot-detection.

---

## Technique 1 — Claw Resource Management

### Stealth Crawling Protocols
- **Rule**: Every crawl session must utilize rotating user-agents and localized proxies to avoid IP blacklisting.
- **Protocol**: Set `RateLimit` to a maximum of **5 requests per second** per domain to maintain a "Human-Like" footprint.

### Data Synthesis Logic
- **Semantic Filtering**: Use OpenClaw's integrated LLM hooks to filter extracted HTML into structured JSON in real-time.
- **Deduplication**: Implement a `ContentHash` check before saving to the Vector DB to prevent redundant data ingestion.

---

## Technique 2 — Agentic Task Execution

### The "Claw-Agent" Handover
- **Context**: Passing extracted intelligence to a reasoning agent.
- **Protocol**: OpenClaw must output a `ContextSlicer` compatible markdown fragment for immediate ingestion by @Cortex or @AIOps.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Aggressive Polling** | IP Blacklist / Cloudflare Wall | Implement exponential backoff and randomized jitters. |
| **Raw HTML Ingestion** | Context window bloat | Always utilize a `Purification Node` to strip non-semantic tags (JS/CSS). |
| **Unhinged Crawling** | Resource leakage | Set a strict `DepthLimit` (max 3) and `DomainWhitelist`. |

---

## Success Criteria (OpenClaw QA)
- [ ] Crawl payload is > 90% structured data (JSON/Markdown).
- [ ] Zero 403/429 errors encountered during 5-minute stress-test.
- [ ] Integration with `@AIOps` for autonomous goal-setting verified.
- [ ] Content is correctly indexed in the `14-04: Intel-Infra` Vector DB.
