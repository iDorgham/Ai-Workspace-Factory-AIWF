---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🎭 Playwright E2E Interaction Physics

## Purpose
Enforce standards for reliable, end-to-end (E2E) testing using Playwright. This skill focuses on the "User-Centric" testing model—verifying actual UI flows (Login, Checkout, Onboarding) rather than implementation details. It ensures low-flake, high-stability automation across Chromium, WebKit, and Firefox.

---

## Technique 1 — Locators over Selectors (Stability)
- **Rule**: Never use CSS or XPath selectors for interactive elements; always use Playwright's **User-Facing Locators**.
- **Protocol**: 
    1. Use `getByRole` (e.g., `role="button", name="Submit"`) to ensure accessibility is also tested.
    2. Use `getByText` or `getByLabel` for inputs.
    3. Use `getByTestId` only as a last resort for complex, non-semantic containers.
    4. Benefit: Tests become resilient to structural changes in the HTML.

---

## Technique 2 — Auto-Waiting & Network Interception
- **Rule**: Rely on Playwright's "Auto-Waiting" instead of manual `sleep()` or `timeout()` calls.
- **Protocol**: 
    1. Perform actions (click, fill) and let Playwright wait for the element to be visible/enabled.
    2. Use `route()` to mock flakey external APIs (e.g., Stripe, Google Maps) during E2E runs.
    3. Set `unroute` or specific assertions to ensure a real API call was attempted when testing integration.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Flakey Timeouts** | Unreliable CI results | Increase "SlowMo" for debugging; use `waitForResponse` or `waitForURL` instead of arbitrary time delays. |
| **Testing Implementation Details** | Brittle tests | Focus on the "Output" (e.g., "Is the message visible?") rather than the "State" (e.g., "Is the variable true?"). |
| **Ignoring Screenshots/Videos** | Invisible failures | Always configure local test-reports to capture video and traces on the first failure. |

---

## Success Criteria (Playwright QA)
- [ ] 0 "Manual Sleeps" found in the test codebase.
- [ ] 100% of critical paths (User Journey) are covered by E2E tests.
- [ ] Tests run successfully in "Headless" mode on CI nodes.
- [ ] Parallel execution setup reduces full-suite time (e.g., < 10 mins).
- [ ] RTL specific interaction (e.g., Drawer opening from the left in AR) is verified.