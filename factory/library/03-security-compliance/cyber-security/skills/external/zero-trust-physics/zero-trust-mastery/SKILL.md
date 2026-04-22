# 🔒 Zero-Trust Security Physics

## Purpose
Enforce a "Never Trust, Always Verify" architecture across the Sovereign Factory. This skill focuses on the logic of micro-segmentation, identity-based access control, and ensuring that no component—internal or external—has implicit trust within the network.

---

## Technique 1 — Identity-Based Micro-segmentation
- **Rule**: Every internal service (e.g., API, DB, Media Processor) must verify the identity and permissions of the requester for every single request.
- **Protocol**: 
    1. Implement JWT or mutual-TLS (mTLS) for inter-service communication.
    2. Define granular scopes for all service-tokens (e.g., `media:read`, `users:write`).
    3. Block any request that does not carry a valid, short-lived identity token.
    4. Remove all dependency on "IP-based" or "VPN-only" trust.

---

## Technique 2 — Just-In-Time (JIT) Privilege Escalation
- **Rule**: Admin-level privileges must be granted only when requested and for a limited time-window.
- **Protocol**: 
    1. Implement a "Request for Access" workflow for high-risk operations.
    2. Grant temporary, scoped IAM roles upon approval.
    3. Revoke access automatically after 1 hour or task completion.
    4. Log all JIT sessions to the immutable security audit tail.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Implicit Internal Trust** | Lateral movement (Breach spread) | Treat internal traffic as potentially hostile; always authenticate service-to-service calls. |
| **Eternal API Keys** | Permanent compromise | Rotate all programmatic keys regularly (e.g., every 90 days) and use OIDC where possible. |
| **Broad Admin Roles** | Excessive blast-radius | Break down "Admin" into "BillingAdmin", "SecurityReader", "AppOperator" etc. |

---

## Success Criteria (Zero-Trust QA)
- [ ] 100% of internal endpoints require valid authentication tokens.
- [ ] 0 "Hard-coded" secrets in internal configuration files.
- [ ] Mutual TLS (mTLS) is enabled for high-risk data conduits.
- [ ] Least Privilege principle is verified for 100% of service accounts.
- [ ] Monitoring shows 100% visibility into internal traffic flows.