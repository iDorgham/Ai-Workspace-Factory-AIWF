# Bug Report: [Short title]

> **ID:** [BUG-NNN or GitHub #]
> **Severity:** [critical | high | medium | low]
> **Status:** [triage | confirmed | in-progress | fixed | wontfix | duplicate]
> **Reported:** [YYYY-MM-DD]
> **Reporter:** [name / channel]
> **Environment:** [prod | staging | local | CI]

---

## Summary

[One sentence: what is wrong vs expected]

---

## Expected vs actual

| | |
|--|--|
| **Expected** | [Correct behavior] |
| **Actual** | [What happens instead] |

---

## Reproduction steps

1. [Step]
2. [Step]
3. [Observe error]

**Repro rate:** [always | intermittent ~X%]

---

## Environment details

- **App / URL:** [version or commit SHA]
- **Browser / OS / device:** [if relevant]
- **User role / tenant:** [if multi-tenant]
- **Feature flags:** [if any]

---

## Evidence

- Screenshots / screen recording: [links]
- Logs / trace IDs: [paste or link]
- Network: [failed request, status code]

---

## Impact

- **Users affected:** [scope]
- **Workaround:** [yes/no — describe]
- **Data integrity / security:** [yes/no — notes]

---

## Suggested area (optional)

- [ ] UI / frontend
- [ ] API / backend
- [ ] Database / migration
- [ ] Auth / permissions
- [ ] Infra / CI
- [ ] Unknown

---

## Triage notes

**Likely owner:** @QA + @[Frontend|Backend|Security]
**Related contract:** `packages/shared/src/contracts/[domain].ts` — [if applicable]
**Duplicate of:** [ID or none]

---

*Template: bug-report | Used by: @QA, triage workflows | After fix: link PR + add regression test*
