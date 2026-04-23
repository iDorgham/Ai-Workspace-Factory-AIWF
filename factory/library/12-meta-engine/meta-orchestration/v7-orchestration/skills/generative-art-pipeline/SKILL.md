# 🎨 SKILL: Generative Art Pipeline (v1.0.0)
# Library Component: 12-meta-engine/meta-orchestration/v7-orchestration/skills/generative-art-pipeline/SKILL.md
# Version: 1.0.0 | Reasoning Hash: sha256:art-skill-2026-04-23
# ============================================================

## Overview

The Generative Art Pipeline enables the factory to autonomously produce visual assets (logos, UI illustrations, hero images, marketing banners) and integrate them directly into the codebase. It uses a multi-model approach (DALL-E 3, Midjourney, Stable Diffusion) via API.

---

## 🛠️ Pipeline Flow

### 1. Intent Analysis (`/art "prompt"`)
- **Agent**: T1 Spec Architect.
- **Task**: Analyzes the project's `design.md` and `style.css` to determine the "Visual Language" (Color palette, typography, mood).
- **Output**: Enhanced system prompt including style tokens (e.g., "minimalist SaaS, glassmorphism, primary color #0070f3").

### 2. Model Selection
- **Logic**:
  - Logos/Icons → DALL-E 3 (Precision).
  - Hero/Illustrations → Midjourney (Aesthetic).
  - Rapid UI Prototyping → Stable Diffusion (Speed/Local).

### 3. Generation & Iteration
- **Task**: Trigger API call.
- **Validation**: Chaos Validator checks for "Visual Drift" (Does the image contrast with existing UI?).
- **Refinement**: If drift detected, triggers variation with adjusted prompt.

### 4. Auto-Provisioning
- **Agent**: T1 Deployment Specialist.
- **Task**:
  - Downscales/Optimizes image (WebP/SVG).
  - Places in `public/assets/{type}/{date}_{slug}.webp`.
  - **Code Injection**: Updates `tailwind.config.js` or `style.css` with new asset variable.

---

## 📋 Commands

```bash
/art "modern hero image for a dive center" --region=redsea
/art logo "AIWF" --style=minimalist
/art ui-asset "feature card background" --variations=4
```

---

## 🌊 Regional Awareness (`--region=redsea|egypt`)

When active, the pipeline injects cultural and aesthetic tokens:
- **Red Sea**: High contrast, turquoise/azure palettes, underwater light diffraction patterns, tourism-focused imagery.
- **Egypt**: Modern calligraphy integration, heritage-tech fusion, desert-gold accents.

---

## 🔗 SDD Integration

Every asset generated is tagged with a `REQ-ID`.
- **Example**: `REQ-UI-004: Hero Section Illustration`.
- **Traceability**: `docs/05-reports/{date}_asset-manifest.json` tracks every generated image, prompt used, and target file.

---

*Skill version: 1.0.0*
*Library path: 12-meta-engine/meta-orchestration/v7-orchestration/skills/generative-art-pipeline/SKILL.md*
*Last updated: 2026-04-23T13:35:26+02:00*
