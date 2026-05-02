---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🎤 Vocal Production & Signal Chains (Omega-tier)

## Purpose
Enforce professional standards for capturing and processing high-fidelity vocals. This skill covers the **Physical Signal Chain** (Hardware) and the **Digital Processing Chain** (Software/VST) to ensure vocals sit perfectly in the mix.

---

## Technique 1 — The Physical Signal Chain

### Microphone & Preamp Synergy
- **Condenser (LDC)**: Use for detailed, high-clarity main vocals (e.g., Neumann, AKG).
- **Dynamic (SM7B)**: Use for aggressive, "In-your-face" Indie Dance or Techno vocals.
- **Preamp Protocol**: Always aim for a "Clean" capture (-18dB average RMS) to allow for harmonic saturation in the digital domain.

---

## Technique 2 — The "Obsidian" Vocal Chain (Digital)

### Serial Processing (Order of Operations)
1. **PITCH**: Autotune (Set to Key/Scale) -> Manual Melodyne for natural performance.
2. **CLEAN**: De-Esser (Target 4kHz - 8kHz) -> High-pass Filter (80Hz - 100Hz).
3. **TONE**: Analog Saturation (Soundtoys Decapitator) -> Pultec-style EQ for "Air."
4. **DYNAMICS**: LA-2A (Optical) for smoothing -> 1176 (FET) for punch.

---

## Technique 3 — Spatial & Parallel Effects

- **Parallel Compression**: Use a "High-Compression" chain mixed 20-30% to add "Breath" and "Thickness."
- **Dimensions**: Use Short Plate Reverbs for "Space" and Long Delays for "Energy" on specific lyrical highlights.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Over-Compression** | Lifeless, flat performance | Use multiple stages of subtle compression (3-5dB reduction each) instead of one heavy stage. |
| **Muddy Reverb** | Drowns the vocal | Always **EQ the Reverb Return** (Low-cut up to 500Hz). |
| **Phase Issues** | Thin sound | Check phase alignment when blending multiple vocal layers or backing tracks. |

---

## Success Criteria (Vocal QA)
- [ ] Vocals are intelligible and "In-Front" of the mix.
- [ ] Sibilance (`S` sounds) is controlled but not muffled.
- [ ] Harmonic saturation adds warmth without audible distortion.
- [ ] Pitch correction is artifact-free (unless used for creative "Auto-tune" effect).