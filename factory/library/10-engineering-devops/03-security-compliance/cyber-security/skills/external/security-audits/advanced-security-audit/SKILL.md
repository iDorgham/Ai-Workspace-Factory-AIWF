---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🛡️ Advanced Security Audit (Trail of Bits)

## Purpose
Enforce standards for high-level security verification and vulnerability research. This skill focuses on the "Offensive Security" mindset—identifying architectural flaws, cryptographic weaknesses, and logic errors before they can be exploited.

---

## Technique 1 — Structural Vulnerability Discovery
- **Rule**: Audit the "Business Logic" first; most critical failures occur in the implementation of domain-specific rules rather than syntax.
- **Protocol**: 
    1. Map the entire data-flow of sensitive information (PII, tokens, keys).
    2. Identify "Privileged Transitions" where authentication or authorization is required.
    3. Attempt to bypass guards using state-manipulation or edge-case input.
    4. Document every "Finding" with a severity score and a concrete remediation plan.

---

## Technique 2 — Automated Fuzzing & Invariant Testing
- **Rule**: Use Echidna (for smart contracts) or similar fuzzers to test for property violations at scale.
- **Protocol**: 
    1. Define the system "Invariants" (e.g., "Total supply never exceeds X", "User balance never goes below zero").
    2. Run continuous fuzzing for 1M+ iterations with random data.
    3. If an invariant is broken, trace the specific path and inputs that caused the failure.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Silent Failures** | Blind-spot vulnerabilities | Ensure the system crashes or logs an error loudly if an invariant is violated. |
| **Complexity Overload** | "Can't audit" stall | Simplify critical logic paths to making them human-auditable and formally verifiable. |
| **Trusting Untrusted Input** | XSS / SQLi / Logic Injection | ALWAYS sanitize and validate all external input through a strict whitelist schema. |

---

## Success Criteria (Security QA)
- [ ] 100% of "High" and "Critical" findings are remediated.
- [ ] Fuzzing runs for critical modules show 0 invariant violations over 12 hours.
- [ ] Cryptographic implementations are verified against industry-standard libraries (no "Roll Your Own").
- [ ] Audit reports include clear, actionable remediation code snippets.