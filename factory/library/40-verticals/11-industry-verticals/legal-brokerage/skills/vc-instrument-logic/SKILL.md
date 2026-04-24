# 🚀 VC Instrument Logic
> **Skill Category:** Venture Physics / Contract Drafting
> **Jurisdictions:** DIFC, ADGM, Delaware (Mena Flip), Cairo (SV Style)

## Purpose
Enforce the technical physics of venture capital instruments. This skill focuses on the auditing and drafting of **SAFE (Simple Agreement for Future Equity)** and **SAFT (Simple Agreement for Future Tokens)** instruments within the MENA ecosystem.

---

## 🛠️ Operational Techniques

### 1. Venture Physics Auditing
- **Valuation Physics**: Audit instruments for Valuation Cap and Discount Rate consistency. Detect and flag "Overlapping SAFE" risks.
- **TGE-Readiness**: For SAFTs, verify mandatory clauses: "Token Generation Event" triggers, Token Lock-ups/Vesting, and "Network Launch" definitions.
- **Pro-Rata Rights**: Automate the calculation of pro-rata allocation for subsequent funding rounds.

### 2. Bilingual VC Assembly
- **AR/EN Side-by-Side**: Generate venture instruments in dual-column format to satisfy both Cairo GAFI standards and DIFC judicial review.
- **Governing Law Routing**: Standardize routing to "DIFC Courts" or "ADGM Courts" for venture disputes, even for Mainland entities, via opt-in clauses.
- **Workflow**: `/legal-draft SAFE` triggers the assembly of a post-money SAFE instrument.

---

## 🛡️ Governance & Anti-Patterns
- **Anti-Pattern**: Using standard U.S. Y-Combinator SAFEs without local jurisdictional modification.
- **Correction**: Inject the "DIFC-ADGM Override" clause to ensure local enforceability of equity conversion.

## Success Criteria
- [ ] 100% of SAFEs include a clarified "Valuation Cap" and "Governing Law" block.
- [ ] SAFT instruments are verified for Token/Equity conversion parity.
- [ ] Bilingual text passes the OMEGA-LEGAL semantic check.
