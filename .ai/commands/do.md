# `/do` — Idea to PRD Command
**Version**: 7.0.0
**Agent**: Master Guide → Spec Architect

---

## Synopsis

```
/do "idea or description" [--region=egypt|redsea|mena] [--from=existing-prd.md] [--dry-run] [--validate]
```

## Description

Transforms a raw idea or description into a structured PRD document with REQ-IDs, acceptance criteria, constraints, and regional notes. The entry point for all new project or feature work in AIWF v7.0.0.

## Behavior

1. **Parse Idea**: Extract domain, primary goal, target users, and implied constraints.
2. **Clarify if Ambiguous**: Ask ≤3 targeted questions if the idea lacks specificity (never more).
3. **Regional Detection**: Auto-detect Egypt/Red Sea/MENA relevance and suggest adaptations (e.g., tourism booking → Fawry integration, Arabic RTL UI, EGP pricing).
4. **Generate PRD**: Write structured `00-prd/prd.md` with:
   - Project title and objective
   - REQ-001, REQ-002... requirement list with acceptance criteria
   - Constraints (technical, legal, regional)
   - Stakeholder list
   - Out-of-scope items
5. **Generate Trace Skeleton**: Output `00-prd/requirements-trace.json` with REQ-ID → phase mapping stubs.
6. **Suggest Next Step**: Recommend `/plan --from=00-prd/prd.md` with appropriate flags.

## Flags

| Flag | Description |
| :--- | :--- |
| `--region=egypt\|redsea\|mena` | Pre-populate regional compliance sections and MENA feature flags. |
| `--from=path/to/prd.md` | Import an existing PRD and enhance/restructure it into AIWF format. |
| `--dry-run` | Show the PRD structure preview without writing files. |
| `--validate` | Run spec-lint on the generated PRD before saving. |

## Output Files

```
plan/00-prd/
├── prd.md                    # Structured PRD with REQ-IDs and acceptance criteria
└── requirements-trace.json   # Trace skeleton: REQ-ID → phase stubs
```

## Examples

```
/do "build a hotel booking platform for Red Sea resorts"
/do "create a legal document management system" --region=egypt
/do --from=AIWF-PRD.md --region=redsea --dry-run
```

---

*Command version: 7.0.0 | Last updated: 2026-04-23*
