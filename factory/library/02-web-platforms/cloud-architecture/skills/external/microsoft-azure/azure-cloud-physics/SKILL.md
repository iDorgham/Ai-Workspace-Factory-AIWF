# ☁️ Microsoft Azure Cloud Physics

## Purpose
Enforce the "Enterprise-Grade" architectural standards for Microsoft Azure. This skill governs the logic of Resource Groups, Managed Identities, and Azure OpenAI integration to ensure high-security, highly-scalable regional infrastructures.

---

## Technique 1 — Managed Identity Security (RBAC)
- **Rule**: Never use connection strings or hard-coded secrets; use **Azure Managed Identities**.
- **Protocol**: 
    1. Assign a System-Assigned ID to the App Service/Function.
    2. Grant specific RBAC roles (e.g., Key Vault Secrets User) to the identity.
    3. Use DefaultAzureCredential in code to securely fetch resources without local secrets.

---

## Technique 2 — Regional High Availability (HA)
- **Rule**: Deploy critical assets across **Availability Zones (AZ)** with a Global Load Balancer.
- **Protocol**: 
    1. Distribute VM instances or App Services across 3 zones within a region.
    2. Use Azure Front Door for global L7 load balancing.
    3. Configure Geo-Redundant Storage (GRS) for critical data backups.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **All-in-One Resource Group** | Blast radius/Billing chaos | Organize resource groups by Lifecycle (prod vs staging) and Component (networking vs app). |
| **Publicly Accessible Storage** | Data exposure | Implement Virtual Network (VNet) Service Endpoints or Private Links for all SQL and Storage accounts. |
| **Ignoring Cost Management** | $10k+ bill surprises | Set hard "Budgets" and "Alerts" in Azure Cost Management for every subscription. |

---

## Success Criteria (Azure QA)
- [ ] 0 Secrets/Passwords stored in local environment variables.
- [ ] Architecture is verified as "Multi-AS" (Multiple Availability Zones).
- [ ] Azure Policy is active to prevent unauthorized resource types.
- [ ] Cost-alerts are set at 50%, 75%, and 90% of monthly budget.