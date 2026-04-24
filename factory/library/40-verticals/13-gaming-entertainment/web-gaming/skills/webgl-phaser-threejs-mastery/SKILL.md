---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🌐 Web Gaming & Interactive Mastery (WebGL)

## Purpose
Enforce professional standards for browser-based gaming and interactive 3D experiences. This skill covers **Phaser** (2D) and **Three.js** (3D) to maximize performance across desktop and mobile browsers.

---

## Technique 1 — Three.js & WebGL Optimization

### Draw Call Reduction
- **Rule**: Minimize draw calls by using `BufferGeometry` and `InstancedMesh` for repeated assets (e.g., forest trees, asteroid fields).
- **Protocol**: Batch textures into **Texture Atlases** to reduce GPU state changes.

### Texture Compression
- **Rule**: Do not serve raw PNG/JPG for heavy 3D assets.
- **Correction**: Use **KTX2 / Basis Universal** compression for GPU-native texture decoding without CPU overhead.

---

## Technique 2 — Phaser (2D Games)

### Physics & Collision
- **Arcade Physics**: Use for simple 2D games with square/circle hitboxes.
- **Matter.js**: Use for complex 2D physics with non-uniform polygons.

### Sound Management
- **Rule**: Audio must be user-triggered (Browser Autoplay Policy).
- **Implementation**: Cache audio assets in `Preload()` to avoid clicking/lag during gameplay.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **High Polygon Count** | Tab Crashes / Lag | Keep mobile target poly-count < 100k per scene. |
| **No "Loss of Context" Handling** | Black screen on resume | Implement `webglcontextlost` and `webglcontextrestored` listeners. |
| **Heavy Main Thread** | Input lag | Move non-rendering logic (Pathfinding, Worker-heavy math) to **Web Workers**. |

---

## Success Criteria (Web Gaming QA)
- [ ] Render loop achieves solid 60FPS on mid-range mobile browsers.
- [ ] Asset bundle size is optimized (Initial load < 5MB).
- [ ] Responsive design works for Portrait/Landscape orientations.
- [ ] GPU memory usage verified via `three-perf` or browser devtools.