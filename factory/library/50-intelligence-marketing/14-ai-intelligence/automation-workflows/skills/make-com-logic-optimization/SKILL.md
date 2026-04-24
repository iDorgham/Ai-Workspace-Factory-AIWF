# ⚡ Make.com Logic Optimization (Omega-tier)


## Purpose
Enforce professional standards for designing high-efficiency scenarios in Make.com. This skill focuses on **Instruction Bundling**, **Filter Efficiency**, and **JSON Data Mapping** to reduce operation consumption and maximize stability.

---

## Technique 1 — Operation Economy

### Scenario Bundling
- **Rule**: Minimize "Search" modules by using **Data Stores** or **JSON Collections**.
- **Protocol**: If a scenario requires multiple searches for the same data point, cache the initial result in a `Variable` and reference it throughout the scenario.

### The "Filter-First" Rule
- **Rule**: Always place **Filters** after triggers but *before* high-cost operations (e.g., GPT nodes, CRM Writes).
- **Validation**: Ensure no operation executes unless a specific "Required Data" field is present.

---

## Technique 2 — Robust JSON Mapping

### Data Purity
- **Rule**: Use the `parseJSON()` and `toJSON()` functions to sanitize complex strings before passing them to external APIs.
- **Protocol**: Map only the specific keys required for the next module; avoid passing the "Whole Object" to reduce payload bloat.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Direct Error Silencing** | Shadow Failures | All scenarios must have an "Error Handler" path (e.g., Ignore vs. Resume vs. Break). |
| **Hard-Coded Values** | Unscalable Logic | Use **Connections** and **Variables** to allow for "Stage vs. Production" environments. |
| **Complex Logic in Filters** | Debugging Nightmare | Move heavy logic to a "Tools: Set variable" node before the filter. |

---

## Success Criteria (Make.com QA)
- [ ] Operation count is minimized (target < 5 per standard lead sync).
- [ ] All "Search" results are checked for `Exists: true` before downstream use.
- [ ] Scenario is segmented into "Bridges" (separate scenarios) for very high volumes.
- [ ] Error handler active in every critical data-write node.
