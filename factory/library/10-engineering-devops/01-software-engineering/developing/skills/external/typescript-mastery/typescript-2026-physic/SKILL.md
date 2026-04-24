---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🔷 TypeScript 2026 Type-Safety Physics

## Purpose
Enforce standards for high-density, type-safe development. This skill focuses on advanced TS patterns (Generics, Discriminated Unions, Branding) and the elimination of `any` to ensure the runtime stability and developer-velocity of the Sovereign Factory.

---

## Technique 1 — Discriminated Unions for State Management
- **Rule**: Never use broad types for complex state; use Discriminated Unions to ensure logic completeness.
- **Protocol**: 
    1. Define a literal `status` field (e.g., `'idle' | 'loading' | 'success' | 'error'`).
    2. Define unique payloads for each status.
    3. Use exhaustive `switch` statements to handle every state, preventing unhandled edge cases.

---

## Technique 2 — Branded Types (Nominal Typing)
- **Rule**: Use branding to prevent "Primitive Obsession" and ensure domain-specific strings (IDs, Emails) aren't mixed.
- **Protocol**: 
    1. Define a unique symbol or property (e.g., `_brand: 'UserId'`).
    2. Cast primitive values to the branded type through a validation function.
    3. Ensure APIs strictly require the branded type, preventing accidental use of a standard String.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **"any" or "unknown" abuse** | Silent runtime crashes | Use `zod` for parsing unknown inputs; use `Satisfies` or `Infers` for structural typing. |
| **Treated types as Documentation** | Lying to the compiler | Ensure types reflect reality; if a field can be nullable, mark it `?` properly. |
| **Monolithic interface definitions** | Rigidity / Bloat | Decompose large interfaces into functional "Mixins" or small atomic pieces. |

---

## Success Criteria (TypeScript QA)
- [ ] `strict: true` is enabled in all `tsconfig.json` files.
- [ ] 0% usage of `any` across the production codebase.
- [ ] 100% classification of external API responses via Zod schemas.
- [ ] Complex generics are documented with usage examples.