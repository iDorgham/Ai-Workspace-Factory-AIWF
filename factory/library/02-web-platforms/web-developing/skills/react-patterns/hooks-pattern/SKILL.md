# ⚓ React Hooks Pattern

## Purpose
Enforce professional standards for stateful logic reuse. This skill focuses on extracting complex component logic into custom hooks to simplify components and ensure pure, testable functional patterns.

---

## Technique 1 — Custom Hook Extraction
- **Rule**: Any logic that spans more than 3 `useEffect` or `useState` calls must be extracted.
- **Protocol**: 
    1. Create a function prefixed with `use`.
    2. Encapsulate all related state, effects, and handlers.
    3. Return a stable object or array of values/functions.

---

## Technique 2 — Stable Dependency Management
- **Memoization**: Use `useCallback` and `useMemo` specifically for props passed to memoized children to prevent render cascades.
- **Ref Stability**: Use `useRef` for values that need to persist across renders but do not trigger UI updates.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Exhaustive Deps Lies** | Stale closures / bugs | Never disable lint rules for dependency arrays; solve the stability problem with `useCallback`. |
| **Logic-Heavy Components** | Impossible to test | Components should be "View Only"; all state orchestration belongs in Hooks. |
| **Conditional Hook Calls** | React Render Crash | Always call hooks at the top level; never inside if-statements or loops. |

---

## Success Criteria (Hooks QA)
- [ ] No "lint-disable" on any Hook dependency arrays.
- [ ] Complex state logic is 100% extracted into custom hooks.
- [ ] `useCallback` is used for all functions passed to deep child components.
- [ ] Components remain < 100 lines of code.