---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🎮 Unreal Engine & C++ Mastery (Omega-tier)

## Purpose
Enforce professional standards for Unreal Engine (UE5) development. This skill focuses on high-performance C++ integration, Nanite/Lumen optimization, and Blueprint/C++ hybrid architecture.

---

## Technique 1 — High-Performance C++ (UObject/AActor)

### Header Hygiene & Compilation Speed
- **Rule**: Minimize `#include` in headers; use **Forward Declarations** whenever possible.
- **Protocol**: Use the `UProperty()`, `UFunction()`, and `UClass()` macros to ensure the Unreal Header Tool (UHT) and Garbage Collector (GC) track object references correctly.

### Memory Management (Smart Pointers)
- **TSharedPtr / TWeakPtr**: Use for non-UObject classes to avoid circular dependencies and leaks.
- **TArray Buffer Allocation**: Use `TArray::Reserve()` before large loops to prevent redundant memory re-allocations.

---

## Technique 2 — UE5 Specialized Rendering

### Nanite & Lumen Optimization
- **Nanite**: Use virtualized geometry for high-poly assets (>1M triangles). Ensure "Nanite-Enable" is checked in the Mesh Editor.
- **Lumen**: Use Hardware Ray Tracing for "Cine-Serious" lighting. Monitor the `stat lumen` overlay for triangle-trace costs.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Logic in Tick()** | Severe frame drop | Use Timers or Event-driven logic via Delegates. |
| **Hard Asset References** | High loading times / Bloat | Use `TSoftObjectPtr` and `TSoftClassPtr` for asynchronous loading. |
| **Blueprint-Only Logic** | Unscalable / Slow | Move "Math-Heavy" or "Loop-Heavy" logic to C++ (Expose via `BlueprintCallable`). |

---

## Success Criteria (Unreal QA)
- [ ] Profiler (`insights`) shows no single-frame stalls > 16.6ms (target 60fps).
- [ ] No hard-coded asset paths; all refs are `TSoftObjectPtr`.
- [ ] Shaders are compiled and cached (no "Compiling Shaders" popups during play).
- [ ] "Rule of Three" followed: Logic (C++) -> Variable exposure (BP) -> Visuals (Level).