# ⚛️ React Design Patterns (Patterns.dev)

## Purpose
Enforce industry-standard design patterns for React applications as defined by Patterns.dev. This skill focuses on code reusability, performance optimization, and clean architectural separation of concerns (SoC). It ensures that every React component added to the Sovereign Factory follows world-class engineering standards.

---

## Technique 1 — HOC & Render Props (Cross-Cutting Concerns)
- **Rule**: Use High-Order Components (HOC) or Render Props to share logic between multiple components without duplicating code.
- **Protocol**: 
    1. Identify shared logic (e.g., authentication checks, data fetching, logging).
    2. Encapsulate the logic in an HOC (e.g., `withAuth`) or a Render Prop component (e.g., `UserData`).
    3. Wrap or inject the logic into the target "Presentational" component.
    4. Benefit: Keeps the UI code clean and allows the "Logic" to be tested and maintained in isolation.

---

## Technique 2 — Compound Components (Implicit State)
- **Rule**: Use the Compound Component pattern for complex UI sets (e.g., Tabs, Accords, Dropdowns) to allow users more control over the rendered structure while maintaining internal state consistency.
- **Protocol**: 
    1. Create a parent "Context" provider.
    2. Create child sub-components (e.g., `Tabs.Trigger`, `Tabs.Content`).
    3. Use `React.Children.map` or Context to pass required state (active index, handlers) implicitly.
    4. Benefit: Eliminates "Prop Drilling" and provides a clean, declarative API.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Fat Components** | Reduced maintainability | Break down components that exceed 200 lines into smaller, atomic sub-components. |
| **Over-Using Context** | "Re-render Hell" | Use Context only for global data (Theme, Auth); use local state or specialized stores (Zustand) for tactical data. |
| **Prop Drilling (Depth > 3)** | Brittle data flow | Use the Compound Component pattern or a global store to pass data to deep children. |

---

## Success Criteria (React QA)
- [ ] 100% of complex UI elements (Tabs, Modals) use the Compound Component pattern.
- [ ] "Logic-heavy" components are split into a "Container" (logic) and "Presentational" (UI) pair.
- [ ] Memoization (`useMemo`, `useCallback`) is applied to prevent unnecessary re-renders in large lists.
- [ ] Component architecture passes the standard "Patterns.dev" quality audit.