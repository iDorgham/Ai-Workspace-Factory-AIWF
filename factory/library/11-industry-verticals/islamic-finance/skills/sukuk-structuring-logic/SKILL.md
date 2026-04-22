# 🏗️ Sukuk Structuring Logic
> **Skill Category:** Structured Finance / Investment Physics
> **Domains:** Asset-Backed Sukuk, Musharaka, Ijarah-wa-Iqtina

## Purpose
Govern the technical creation and management of Sukuk (Islamic Bonds) and other asset-backed investment instruments. This skill ensures that all investment certificates represent ownership of an underlying tangible asset.

---

## 🛠️ Operational Techniques

### 1. Asset-Backing Verification (Asset-vs-Bond)
- **Physics**: Enforce a mandatory "Underlying Asset Hash" for every Sukuk issuance.
- **Auditing**: Verify that the asset value covers 100% of the certificate issuance (Asset-Basing vs Asset-Backing logic).
- **Workflow**: `/sharia Sukuk-Draft` scaffolds the prospectus with mandatory asset-node links.

### 2. Profit-Loss Sharing (Musharaka)
- **Logic**: Implement "Pro-Rata-Omega" calculation for investment yields based on actual asset performance, not fixed percentages.
- **Governance**: Ensure that the "Purchase Undertaking" matches Sharia-standard pricing models (no face-value guarantees for equity Sukuk).

---

## 🛡️ Governance & Anti-Patterns
- **Anti-Pattern**: Issuing Sukuk without a clear transfer of beneficial ownership.
- **Correction**: Use the "Trust-Deed-Physics" protocol—all issuance MUST involve a Special Purpose Vehicle (SPV) with verifiable asset ownership.

## Success Criteria
- [ ] 100% of Sukuk stubs are linked to a verified, physical or digital asset node.
- [ ] Profit distribution matches actual asset yield stubs.
