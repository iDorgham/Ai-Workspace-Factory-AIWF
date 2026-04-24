# ⚖️ Litigation Orchestrator
> **Skill Category:** Legal Brokerage Operations
> **Jurisdictions:** UAE (Dubai Courts), Egypt (Cairo Judicial Districts)

## Purpose
Automate the litigation lifecycle using the **"Evidence-First"** protocol. This skill ensures all case filings are indexed, hashed for chain-of-custody, and submitted punctually via national digital portals.

---

## 🛠️ Operational Techniques

### 1. Court-Ready Case Indexing
- **Physics**: Assign a unique SHA-256 hash to every evidence node (PDF, JPG, Audio) upon ingestion.
- **Taxonomy**:
  - `EVID-LIT-[CLIENT]-[DATE]-[HASH]`
  - Map evidence strictly to the Statement of Claim (SOC) paragraphs.
- **Workflow**: `/legal CaseIndex [workspace_path]` scans the research folder and generates a `court_evidence_index.json`.

### 2. Digital Hearing Automation
- **Portal Compliance**: Automate the formatting of memorandums for the **Dubai Courts E-Litigation** portal and **Egypt Digital Justice** portals.
- **Deadline Logic**: Enforce a "Minus-48" rule. All filings must be ready and validated 48 hours before the hearing date.
- **Alert Physics**: Trigger the Sentinel agent if a hearing MEMO is missing 72 hours before the date.

---

## 🛡️ Governance & Anti-Patterns
- **Anti-Pattern**: Using generic timestamps.
- **Correction**: Use the system-locked `TIME-OMEGA` timestamp for all hashing operations to prevent tamper challenges in court.

## Success Criteria
- [ ] 100% of evidence nodes possess a valid cryptographic hash.
- [ ] Memorandums are valid against the [Jurisdiction-Checklist](file:///factory/library/11-industry-verticals/legal-brokerage/templates/memorandum_checklist.md).
