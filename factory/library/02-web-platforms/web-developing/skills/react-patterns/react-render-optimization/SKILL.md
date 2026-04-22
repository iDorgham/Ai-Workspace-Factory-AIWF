# 🚀 React Render Optimization

## Purpose
Enforce professional standards for minimizing "Jank" and unnecessary rendering cycles. This skill focuses on state colocation, memoization strategy, and architectural patterns to ensure high-performance React applications.

---

## Technique 1 — State Colocation
- **Rule**: Keep state as close as possible to the component that uses it.
- **Protocol**: 
    1. Identify state currently at the root that is only used by a deep leaf.
    2. Move the state down to the smallest common ancestor.
    3. Use "Children as Props" (Composition) to prevent re-rendering the entire branch when parent state changes.

---

## Technique 2 — Selective Memoization
- **React.memo**: Use ONLY for expensive rendering components that receive stable props (e.g., charts, complex lists).
- **Stabilization**: Always wrap objects and functions passed to `React.memo` components in `useMemo` and `useCallback`.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Global State for Everything** | Massive re-render cascades | Use local state by default; reserve Context/Zustand for truly global data. |
| **Object Literals in Props** | Broken memoization | Never pass `{}` or `[]` directly in JSX; define them with `useMemo`. |
| **Premature Memoization** | Code complexity / overhead | Profile first with React DevTools; only memoize if a component is confirmed to be an expensive bottleneck. |

---

## Success Criteria (Render QA)
- [ ] No re-renders on components whose props haven't changed (verified via DevTools).
- [ ] State is colocated with its primary consumers.
- [ ] List items use stable `key` values (no Array indices).
- [ ] Expensive calculations use `useMemo`.