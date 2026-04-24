---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🧬 Bilingual Semantic Authority (RE-Specialized)

## Purpose
Dominate high-value search intent in bilingual markets. This skill provides the "Omega-tier" SEO mapping required for luxury segments (Real Estate, Fintech) where competition is fierce and bilingual (AR/EN) parity is a ranking requirement.

---

## Technique 1 — Dubai Real Estate Keyword Clusters (2024)

### Cluster: "Off-Plan Luxury" (High Transaction Volume)
- **Primary EN**: "Dubai Off-plan property", "New launches Dubai", "Buy apartment Dubai Creek".
- **Primary AR**: "عقارات قيد الإنشاء دبي", "مشاريع دبي الجديدة", "شقق للبيع دبي".
- **Semantic LSI**: "ROI", "DLD Approved", "Escrow protection", "Post-handover payment plan".

### Cluster: "Ultra-High-Net-Worth" (Low Volume, High Value)
- **Primary EN**: "Luxury penthouses Palm Jumeirah", "Mansions for sale Emirates Hills".
- **Primary AR**: "بنتهاوس فاخر نخلة جميرا", "فلل للبيع تلال الإمارات".
- **Intent**: Informational ("Current Dubai luxury price per sqft") → Transactional ("Private viewing").

---

## Technique 2 — Arabic Voice Search Intent (Ammiya)

Modern MENA users primarily search via voice on mobile. This requires mapping "Ammiya" (Dialect) intent into technical meta-tags.

| Voice Query (Ammiya) | Technical Intent Mapping | Semantic Target |
| :--- | :--- | :--- |
| "شقق قريبة من المترو" | `near:metro_station` | Commuter Accessibility |
| "عقارات تصلح للجنسية" | `query:golden_visa_eligible` | Investor Citizenship |
| "أفضل استثمار في دبي" | `category:high_yield_roi` | Financial Advisory |

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Direct Translation** | Zero semantic search flow | Transcreate: Match regional intent, not just literal words. |
| **Ignoring Hreflang** | Search cannibalization | Map `rel="alternate" hreflang="ar-ae"` (UAE specific). |
| **Fusha-Only Keywords** | High bounce rate | Use Fusha for authority, but Ammiya slugs for organic "long-tail" voice queries. |

---

## Success Criteria (SEO Authority)
- [ ] Schema markup (JSON-LD) includes `Specialty: RealEstateAgent`.
- [ ] Hreflang tags validated for recursive `ar-ae` / `en-ae` parity.
- [ ] Topic clusters mapped to "Off-plan" and "Luxury" silos.