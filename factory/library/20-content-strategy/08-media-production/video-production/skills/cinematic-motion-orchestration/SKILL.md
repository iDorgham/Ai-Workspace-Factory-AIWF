---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🎞️ Cinematic Motion & AI Orchestration (AI-Cine)

## Purpose
Direct high-fidelity cinematic video using AI generation engines (Sora, Runway Gen-2/3, Kling). This skill provides the "Director's Protocol" for creating the **Obsidian-tier** visual content required for luxury real estate, replacing traditional expensive drone/dolly shots with stabilized AI cinematography.

---

## Technique 1 — AI Cinematic Prompting (Real Estate)

### Camera Movement Tokens
- **Drone Orbit**: `[Cinematic drone orbit shot of a glass tower in Dubai at sunset, 4k, extreme detail, architectural photography, hyper-realistic, 24fps]`
- **The "Reveal"**: `[Low-angle dolly shot into a marble penthouse, sunlight filtering through tall windows, dust motes, 35mm lens, shallow depth of field, slow motion, 8k resolution]`

### Material Consistency Check
- **Temporal Consistency**: Ensure glass reflections do not "morph" during the 10-second shot. 
- **Method**: Use **Base-Image Reference** and fixed seed-variation (≤0.05) across frame sequences.

---

## Technique 2 — Regional Color Grading (Dubai Cine)

Luxury content in the MENA region requires a specific color palette that signals "Premium".

| Component | Target Hue | Tone Profile |
| :--- | :--- | :--- |
| **Sky** | Deep Azure / Royal Blue | Polarized, graduated ND filter effect. |
| **Skin/Sand** | Warm Ochre | Sunkissed, "Golden Hour" highlight roll-off. |
| **Material** | Gold / Silver | High-specular bounce, desaturated mid-tones. |

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **AI "Wobble"** | Cheap CGI look | Use `Flow-Matching` or `Frame-Interpolation` tools (Runway) for stabilization. |
| **Jittery Arabic Text** | Readability loss | Overlay 2D High-res Arabic typography (Amiri) post-generation; do not burn into AI prompt. |
| **Flat Lighting** | Poor depth | Use `Lighting Reference` (IBL) based on "Dubai Golden Hour" HDRI. |

---

## Success Criteria (AI-Cine)
- [ ] Shot length ≥ 5 seconds with zero artifact morphing.
- [ ] Color Grade matches "Luxury Cinematic" profile (Warm shadows, cool highlights).
- [ ] Camera movement follows "Parallax" rules (Front/Middle/Back planes).
- [ ] Arabic motion-titles are High-Density SVGs, not AI-generated text.