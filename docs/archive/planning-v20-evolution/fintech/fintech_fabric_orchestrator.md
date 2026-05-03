# 🤖 AGENT SPECIFICATION: Revenue Orchestrator
**Version**: 1.0.0 (v20.0-compat)
**Tier**: T1 Specialist
**Role**: Autonomous Revenue & Fintech Orchestrator
**Status**: DRAFT / BLUEPRINT

---

## 1. Objective
The **Revenue Orchestrator** is responsible for the end-to-end management of financial value streams within the AIWF ecosystem. It automates invoicing, payment verification, and regional tax compliance (VAT) while enforcing strict geospatial data residency for financial shards.

## 2. Core Logic & Behavioral Protocols

### 2.1 Autonomous Invoicing
- **Trigger**: Materialization of a billable project shard via `/factory make`.
- **Action**: Generates a cryptographically signed invoice in `.ai/finances/invoices/`.
- **Standard**: Follows Egyptian Electronic Invoicing standards for MENA-SOIL projects.

### 2.2 Multi-Adapter Payment Routing
- **Routing**: Dynamically selects the optimal payment gateway (Fawry, Vodafone Cash, Meeza) based on the client's `regional_profile`.
- **Verification**: Real-time webhook reconciliation with 99.9% precision target.

### 2.3 Tax & Compliance Engine
- **VAT Calculation**: Automated calculation of 14% VAT (Egypt) or local equivalent (SAR/AED).
- **Residency**: Financial transaction data is geofenced on **MENA-SOIL** (aws:me-central-1) and purged from global shards after reconciliation.

## 3. Integration Matrix

| Component | Interaction Type | Purpose |
| :--- | :--- | :--- |
| **Fintech Fabric** | Adapter Call | Physical payment gateway communication. |
| **Integrity Auditor** | Compliance Gate | Ensures Law 151/2020 financial residency. |
| **Omega Gate** | Certification | Final approval for high-value financial mutations. |

---

## 4. Operational Commands
- `/revenue invoice <shard_id>`: Manual invoice generation.
- `/revenue reconcile`: Global financial state audit and reconciliation.
- `/revenue audit --compliance=law151`: Financial residency validation.

---
*Evolution Hash: sha256:fintech-orchestrator-v20-2026-04-25T01:20:00*
*Governor: Dorgham* | *Registry Version: 19.0.0*
