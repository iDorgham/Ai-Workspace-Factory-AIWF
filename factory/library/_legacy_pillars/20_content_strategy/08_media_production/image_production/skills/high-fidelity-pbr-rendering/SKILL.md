---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🧊 High-Fidelity PBR Rendering Standards

## Purpose
Enforce physical accuracy in architectural and product visualization. PBR (Physically Based Rendering) is the "Omega-tier" requirement for luxury real estate and premium retail assets, ensuring light interacts with materials (marble, gold, glass, desert sand) exactly as it does in the real world.

---

## Technique 1 — The Luxury Material Stack (PBR)

### Material Constants (Non-Metal)
- **Dielectric Reflectivity**: Clamp between 2% and 5% (F0 = 0.04).
- **Roughness Mapping**: Use 16-bit displacement maps to avoid "stepping" artifacts in high-end stone textures (e.g., Calacatta Marble).
- **Anisotropy**: Required for brushed metals and silk fabrics (common in Jumeirah-style interiors).

### Metal Constants (Gold & Brass)
- **Base Color (Albedo)**: [Hex: #FFD700] but must be adjusted for indirect lighting. 
- **Metallic**: Set to 1.0.
- **Micro-Detail**: Gold assets must have a subtle `Imperfection Map` at 0.05 opacity to prevent "CGI-plastic" look.

---

## Technique 2 — Regional Lighting (MENA Context)

### The "Golden Hour" Algorithm
Dubai-specific lighting (Outdoor):
- **Sun Intensity**: 120,000 Lux (Simulating noon glare) vs. 80,000 Lux (Global default).
- **Sun Color Temperature**: 5500K (Daylight) → 2800K (Sunset).
- **HDRI Calibration**: Use `Dubai Horizon` or `Desert Plateau` maps at 32-bit depth for accurate sky-lighting on glass towers.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Pure Black Shadows** | Unnatural look | Use Multi-Bounce Global Illumination (Lumen/Native Raytracing). |
| **Perfect Surfaces** | "Fake" appearance | Add "Micro-Fingerprints" or "Dust" maps to Roughness channel (0.02 opacity). |
| **Over-Saturated Albedo** | Light-leaks | Ensure no Albedo value is > 243 (8-bit) to avoid energy conservation breach. |

---

## Success Criteria (Visual QA)
- [ ] No Moire patterns on thin surfaces.
- [ ] Energy conservation verified (Specular + Diffuse ≤ 1.0).
- [ ] 16-bit Normal/Displacement maps used for all luxury textures.
- [ ] "Dubai Golden Hour" lighting profile applied.