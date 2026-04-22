# Prompt 06 — Quality gates for [Feature Name]

**Prerequisites:** Implementation merged for this slice.

---

Run the Sovereign gate pipeline in order:

1. `spec:validate`
2. `contract:auto-validate`
3. `compliance`
4. `security:scan` (for sensitive surface)
5. `test`
6. `build`

**Actions:**

- List failures with file paths.
- Fix violations; do not bypass gates without documented approval in `phase_logs/`.

**Output:** pass/fail per gate + link to CI run if applicable.
