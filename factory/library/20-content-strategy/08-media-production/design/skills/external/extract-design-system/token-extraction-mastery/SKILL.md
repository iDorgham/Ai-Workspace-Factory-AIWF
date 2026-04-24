---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 📐 Design System Extraction (Tokens)

## Purpose
Enforce standards for deconstructing complex UI designs into reusable design tokens. This skill focuses on identifies recurring patterns in colors, typography, and spacing to automate the creation of a consistent configuration (e.g., `tailwind.config.js` or CSS variables).

---

## Technique 1 — Pattern Recognition (Visual Audit)
- **Rule**: Before coding, perform a visual audit of the high-fidelity design to identify the "Base Tokens."
- **Protocol**: 
    1. Extract the 5 primary brand colors (Primary, Secondary, Accent, Neutral, Surface).
    2. Define the typography scale (H1-H6, Body, Label).
    3. Isolate recurring spacing units (4px, 8px, 12px, 16px, 24px, 32px).
    4. Group these into a `tokens.json` manifest.

---

## Technique 2 — Syncing Truth (Code Generation)
- **Rule**: Design tokens in code must be the "Single Source of Truth."
- **Protocol**: 
    1. Generate Tailwind-compatible JSON from the token manifest.
    2. Inject JSON into the configuration layer.
    3. Use the mapping to ensure every component uses `@theme` or utility-safe values.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)
| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Magic Numbers** | Inconsistent spacing | Replace all arbitrary values (e.g., `padding: 17px`) with the nearest token (e.g., `p-4` or `16px`). |
| **Shadow Divergence** | Inconsistent depth | Define 3 elevations (Sm, Md, Lg) and use them exclusively. |
| **Isolated Styles** | Maintenance nightmare | Every new component MUST inherit from existing tokens; never declare local `:root` variables in component CSS. |

---

## Success Criteria (Extraction QA)
- [ ] 0 Hard-coded hex values in the application logic.
- [ ] Token manifest matches the Figma/Design handoff exactly.
- [ ] Changing a single token (e.g., `--primary`) updates the entire application UI.
- [ ] Arabic typography tokens are specifically defined for RTL readability.