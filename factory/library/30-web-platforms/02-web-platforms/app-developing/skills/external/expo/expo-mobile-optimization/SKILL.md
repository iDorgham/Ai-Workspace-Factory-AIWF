---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 📱 Expo Mobile Optimization

## Purpose
Enforce standards for high-performance cross-platform mobile apps using the Expo ecosystem. This skill focuses on minimizing app bundle size, optimizing the "Splash-to-Interactive" timeline, and ensuring consistent high-frame-rate (60fps) animations.

---

## Technique 1 — Managed Assets & OTA Physics
- **Rule**: Use EAS (Expo Application Services) for Over-the-Air (OTA) updates and build management.
- **Protocol**: 
    1. Optimize all local images using `expo-image` and `sharp`.
    2. Deliver critical updates via `expo-updates` without requiring App Store re-submissions.
    3. Use selective bundling to exclude unnecessary native modules from the final IPA/APK.

---

## Technique 2 — Viewport-Ready Rendering
- **Rule**: Prioritize "Above-the-Fold" interactive components to reduce Time-To-Interactive (TTI).
- **Protocol**: 
    1. Use `FlatList` with `windowSize` optimization for long lists.
    2. Lazy-load non-critical screens using dynamic imports.
    3. Implement `Skeleton` loaders that match the final UI dimensions to prevent layout jumps.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Monolithic State in Mobile** | Stuttering / Battery drain | Use local state for UI transitions; reserve global state (Zustand/Redux) for truly persistence-level data. |
| **Ignoring Android Low-End Nodes** | 30% user dropout | Test regularly on low-end Android hardware; avoid heavy SVG or blur effects on budget devices. |
| **Syncing Large Native Modules** | Massive bundle size | Only import the specific native sub-modules required for the feature (tree-shaking). |

---

## Success Criteria (Expo QA)
- [ ] Initial App Load is < 3s on medium-tier devices.
- [ ] 60 FPS maintained during complex transitions and list scrolls.
- [ ] 100% of images are webp-optimized and cached locally.
- [ ] OTA updates successfully tested and deployed via EAS.