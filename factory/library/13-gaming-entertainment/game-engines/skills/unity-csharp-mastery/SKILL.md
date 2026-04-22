# 🎮 Unity & C# Mastery (Omega-tier)

## Purpose
Enforce senior-level architectural standards for Unity development. This skill focuses on high-performance C# (Job System, Burst) and decoupled architecture (ECS) to ensure games remain scalable and maintainable.

---

## Technique 1 — High-Performance C# (DOD)

### The Job System & Burst Compiler
- **Rule**: All heavy mathematical computations (Pathfinding, Flocking, Particle Physics) must use **C# Jobs**.
- **Optimization**: Mark all job structs with `[BurstCompile]` and use `NativeArray<T>` for zero-GC memory management.
- **Safety**: Do not access managed objects (Strings, GameObjects) inside a Job.

### Memory Hygiene
- **Zero-Allocation update**: Ensure `Update()` loops produce 0B of Garbage Collection (GC) per frame.
- **Pooling**: Use `UnityEngine.Pool` for all frequently instantiated/destroyed objects (Bullets, VFX).

---

## Technique 2 — Architectural Patterns

### Entity-Component-System (ECS)
- **Constraint**: Use ECS for entities where count > 5,000.
- **Pattern**: Data lives in `IComponentData`; Logic lives in `SystemBase` or `ISystem`.

### ScriptableObject-Driven Design
- **Rule**: Use `ScriptableObjects` for global state, configuration, and event bus systems to avoid `Singleton` bloat.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **GameObject.Find()** | High O(n) overhead | Cache references in `Awake()` or use Dependency Injection. |
| **Large Update() Loops** | CPU Spikes | Use `Coroutine` or `Task` with appropriate intervals. |
| **String-Based Tags** | Unsafe / Slow | Use LayerMasks or specialized `Enum` identifiers. |

---

## Success Criteria (Unity QA)
- [ ] No GC allocations in the hot path (`Update`, `FixedUpdate`).
- [ ] Profiler shows "V-Sync" as the main bottleneck (target achieved 60/120fps).
- [ ] All heavy systems are Jobified and Burst-Compiled.
- [ ] Dependencies are managed via ScriptableObjects or DI frameworks (Zenject/Sextant).