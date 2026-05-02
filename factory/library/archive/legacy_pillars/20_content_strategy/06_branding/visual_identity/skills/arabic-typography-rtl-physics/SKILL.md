---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# ✒️ Arabic Typography & RTL Physics (Omega-tier)

## Purpose
Enforce professional standards for Arabic typographic communication and Right-to-Left (RTL) layout architecture. This skill focuses on the **Anatomy of Arabic Characters**, **Contextual Forms**, and **RTL Grid Physics** to ensure high-aesthetic bilingual experiences.

---

## Technique 1 — The Anatomy of Arabic Typography

### Naskh vs. Kufic vs. Modern Geometric
- **Naskh**: Use for long-form reading and high-eligibility body text.
- **Kufic**: Use for structural logos and architectural branding.
- **Modern Geometric**: Use for contemporary, minimalist UI/UX branding.

### Contextual Shaping & Ligatures
- **Rule**: Arabic characters change shape based on their position (Initial, Medial, Final, Isolated).
- **Protocol**: Verify that the chosen font handles **Ligatures** (e.g., Lam-Alif) correctly without overlapping or breaking "Visual Balance."

---

## Technique 2 — RTL Layout & Spacing Physics

### The "Flipped" Grid
- **Alignment**: Primary focus shifts from Left-to-Right to Right-to-Left. 
- **Rule**: Icons, navigation, and text alignment must be mirrored. 
- **Typography Breathing Room**: Arabic characters typically have higher ascenders and descenders. Increase the **Line Height (Leading)** by 20-30% compared to English counterparts to prevent overlapping and visual density.

---

## Technique 3 — Bilingual Harmony (AR/EN Sync)

- **Optical Scaling**: Arabic often looks smaller or thinner than English at the same point size. 
- **Protocol**: Apply "Optical Sizing" — adjust the Arabic font size +1pt to +2pt relative to the English font to maintain "Visual Weight parity."

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Broken Characters** | Unreadable / Disrespectful | Ensure the software (Adobe CC/Figma) has "Middle Eastern" features enabled to avoid disconnected letters. |
| **Tight Leading** | Visual "Noise" | Increase `Line-Height` to allow for the distinct descenders of the Arab script. |
| **Incorrect Mirroring** | Confusing UI | Mirrored layouts should not invert "Directional Icons" (e.g., a "Clock" or "Back arrow" must reflect the actual movement direction). |

---

## Success Criteria (Arabic Design QA)
- [ ] Arabic and English fonts share "Optical Weight."
- [ ] RTL alignment is consistent across the entire grid.
- [ ] Characters are correctly connected (no logic breaks).
- [ ] Leading (spacing) is calibrated for readability.