---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 💰 Game Economy & Monetization (Digital ROI)

## Purpose
Design and implement profitable, sustainable game economies. This skill covers **IAP (In-App Purchases)**, **Ad-Monetization**, and **Web3 Digital Identity (Skins/NFTs)** while maintaining player trust and regulatory compliance.

---

## Technique 1 — In-App Purchases (IAP) & Retention

### Transactional Psychology
- **Rule**: Implement "Sunk Cost" and "Daily Rewards" loops to maximize LTV (Lifetime Value).
- **The "Obsidian" Hub**: Create a centralized shop-front that handles multi-currency transactions (Soft currency vs. Hard currency).

### Regional Payments (MENA)
- **Gateways**: Integrate **PayTab**, **HyperPay**, and **Apple Pay** for the GCC market.
- **Compliance**: Ensure "Loot Box" mechanics comply with regional gambling regulations.

---

## Technique 2 — Ad-Monetization Strategy

### Ad-Network Orchestration
- **Rule**: Use **Mediation Layers** (AppLovin MAX, IronSource) to floor-price bids across multiple networks.
- **Ad-Types**:
    - **Rewarded Video**: High retention, low friction.
    - **Banners/Interstitials**: Use sparingly to avoid churn.

---

## Technique 3 — Web3 Skins & Identity

### Digital Ownership
- **Standard**: Use **ERC-6551** (Token Bound Accounts) to allow "Skins" to own other assets (e.g., a Character NFT owning a Sword NFT).
- **Interoperability**: Design metadata schemas that allow assets to be ported across different games within the same ecosystem.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Pay-to-Win (P2P)** | Post-launch churn | Balance economy to ensure "Skill" is the primary progress gate. |
| **Unprotected IAP** | Revenue loss | Implement **Receipt Validation** on the Server-side (Apple/Google APIs). |
| **Web3 "Wall"** | High bounce rate | Use "Custodial Wallets" for seamless onboarding; don't force MetaMask on start. |

---

## Success Criteria (Monetization QA)
- [ ] Economy simulation shows sustainable "Sink-to-Source" ratio.
- [ ] Receipt validation active and verified for all IAP.
- [ ] Ad-Mediation successfully serving 95%+ fill rate.
- [ ] Web3 identity system supports gasless transactions (Meta-transactions).