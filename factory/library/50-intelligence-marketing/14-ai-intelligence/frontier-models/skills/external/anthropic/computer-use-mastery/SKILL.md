# 💻 Anthropic Computer Use Mastery


## Purpose
Enforce standards for letting AI agents interact directly with computer interfaces (GUI). This skill governs the logic of screenshot analysis, coordinate mapping, and reliable mouse/keyboard interaction via the Anthropic "Computer Use" API.

---

## Technique 1 — Visual Context Sampling
- **Rule**: Agents must verify the UI state via a fresh screenshot before every non-trivial action.
- **Protocol**: 
    1. Take a full-screen or region-specific screenshot.
    2. Analyze element coordinates using the model's visual reasoning.
    3. Calculate precise pixel offsets to avoid clicking "Dead Zones."

---

## Technique 2 — The "Safe-Fail" Interaction Loop
- **Rule**: Every mouse click or drag must be verified for semantic success.
- **Protocol**: 
    1. Perform the action (e.g., click "Submit").
    2. Wait 500ms-1s for DOM/UI updates.
    3. Take a follow-up screenshot to confirm the expected UI transition (e.g., "Success Message" visibility).

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Coordinate Drift** | Missed clicks / Data corruption | Always re-sync coordinates after scrolling or window resizing. |
| **Infinite UI Loops** | Token exhaustion | Implement a 5-step "Stuck" detection logic; escalate if the UI doesn't transition. |
| **Ignoring Network Latency** | Timing mismatches | Always use a `wait_for_pixel_change` or `wait_for_element` logic before the next action. |

---

## Success Criteria (Computer Use QA)
- [ ] 0% "Dead Clicks" across 10-step UI automation.
- [ ] Agent correctly identifies and recovers from "Modal Obstructions."
- [ ] High-accuracy coordinate mapping (+/- 2 pixels).
- [ ] Secure execution: No interactions with unauthorized "Forbidden Zones" (e.g., system settings).
