---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🎚️ Mixing & Mastering Mastery (Omega-tier)

## Purpose
Enforce professional standards for technical mixing and mastering. This skill focuses on the **Physics of the Low-End**, **Track Energy Management (RMS/LUFS)**, and the **"Analog" Feel** in a digital environment.

---

## Technique 1 — The Kick & Bass Physics

### Low-End Octave Separation
- **Rule**: The Kick and Sub-Bass cannot occupy the same frequency peak.
- **Protocol**: If the Kick peak is at **50Hz**, the Sub-Bass fundamental must be at **80Hz - 100Hz** (or vice versa).
- **Sidechaining**: Use aggressive sidechain triggers (e.g., ShaperBox or Ableton Compressor) to duck the Bass by 100% for the duration of the Kick's transient.

---

## Technique 2 — Analog Heat & Saturation

- **Group Processing**: Apply subtle tape saturation (e.g., U-he Satin or Arturia Tape MELLO-FI) to the Drum and Synth groups to "Glue" the sounds together.
- **Harmonic Distortion**: Use Soundtoys Decapitator or Radiator to add "Weight" to thin digital synths.

---

## Technique 3 — Master Chain (Energy Control)

1. **CLEAN**: Linear Phase EQ to cut anything below 20Hz (unheard energy) and above 20kHz.
2. **COMPRESS**: Glue Compressor (Slow Attack, Auto Release) with max 1-2dB of reduction.
3. **TONE**: Pultec-style "Smile" (Slight boost at 60Hz and 12kHz).
4. **LIMIT**: Pro-L2 or equivalent. Target **-8 to -6 LUFS** for club-ready Techno/Indie Dance.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Mixing in Solo** | Disjointed mix | Always mix components in the context of the whole track. |
| **Over-Saturated Low-End** | Mud / Loss of Headroom | Use multi-band compression to control the low-frequency energy (below 150Hz). |
| **Phase Cancellation** | Weak, hollow sound | Regularly check the mix in **MONO** to ensure no critical layers disappear. |

---

## Success Criteria (Engineering QA)
- [ ] Kick and Bass are clearly defined in the sub-region.
- [ ] Mono-compatibility verified.
- [ ] Dynamic range is preserved (no "Sausage" waveform).
- [ ] Master output peaks at -1.0dB True Peak.