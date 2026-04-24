---
type: Generic
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# `/tutorial` — Interactive AIWF Command System Instructor
# Library Component: 12-meta-engine/meta-orchestration/v7-orchestration/
# Version: 7.0.0 | Reasoning Hash: sha256:tutorial-v7-2026-04-23
# ============================================================

## Synopsis

```
/tutorial
/tutorial --start=do|plan|dev|test|fix|deploy
/tutorial --from=step-N
/tutorial --project="your idea"
```

## Description

Launches **AIWF Instructor Mode** — an interactive, step-by-step walkthrough of the complete AIWF v7.0.0 workflow. The instructor follows the user through each command, explains concepts, validates understanding with checkpoints, and adjusts the pace based on responses.

Unlike `/guide` (which appears at the end of every response), `/tutorial` is a full **teaching session** that the user initiates when they want to learn or onboard onto the system.

---

## Instructor Behavior Protocol

When `/tutorial` is invoked, the Master Guide switches into **Instructor Mode** with these behaviors:

1. **Never skip ahead** — complete each step before moving to the next.
2. **Always explain the "why"**, not just the "what".
3. **Use the user's actual project** if provided via `--project=`, or use a running example.
4. **Ask checkpoint questions** after each step to confirm understanding.
5. **Save progress** — if session ends, `/tutorial --from=step-N` resumes.
6. **Log the session** → `docs/00-guides/{date}_tutorial-session.md` with notes and user answers.
7. **Never overwhelm** — one concept per step, maximum 3 code examples per step.

---

## Tutorial Flow (8 Steps)

### STEP 0 — Welcome & Setup Check
```
Instructor says:
"Welcome to AIWF v7.0.0! I'm your instructor for this session.
Before we start, let me check your workspace is ready...

Checking:
✅ .ai/ directory present
✅ v7 command system loaded
✅ docs/ categories present

Do you have a project idea in mind? (Optional — I can use a demo project if not.)
Type your idea or press Enter to use the demo: 'Red Sea resort booking platform'"
```

### STEP 1 — The Idea Phase (`/do`)
```
Instructor says:
"Step 1: Every project starts with an idea.
The /do command transforms your idea into a structured PRD.

📚 WHY: A structured PRD with REQ-IDs is the foundation. Without it,
we have no way to trace requirements all the way to tests. No traceability = no auto-merge.

Let's try it. Run this command:

  /do "{user's idea or demo idea}" [--region=redsea]

▶️ Now it's your turn. Run the command above."

[Wait for user to run /do]

Checkpoint: "What REQ-IDs were generated? How many requirements does your PRD have?"
```

### STEP 2 — The Plan Phase (`/plan`)
```
Instructor says:
"Step 2: Now we turn your PRD into a complete technical blueprint.
The /plan command generates spec.yaml, architecture diagrams, database schema, and contracts.

📚 WHY: spec.yaml is our single source of truth — like a building permit.
No /dev can proceed without it. The Spec Architect builds it, Contract Guardian enforces it.

Run:
  /plan --from=plan/00-prd/prd.md

▶️ Your turn."

[Wait for user to run /plan]

Checkpoint: "Did all 4 validation gates pass? If not, what failed and what does /fix suggest?"
```

### STEP 3 — The Approval Gate (`spec.yaml`)
```
Instructor says:
"Step 3: Before we can build, the spec needs approval.

📚 WHY: This is Omega Gate v2. It prevents building the wrong thing.
It's a one-time checkpoint — once approved, /dev can run freely for this phase.

Look at your plan/01-{slug}/spec.yaml file.
Find the 'approved_by' field. It says 'pending_omega'.

To approve:
  Change it to: approved_by: 'Dorgham-Approved'
  Then run:    /git commit -m 'spec: approve phase 1'

▶️ Your turn — approve the spec."

Checkpoint: "Why do you think we require explicit approval before building?"
```

### STEP 4 — Build Phase (`/dev`)
```
Instructor says:
"Step 4: Now we build! /dev implements the code for phase 1.

📚 WHY: /dev is Library-First — it pulls existing components from factory/library/
before generating anything new. This prevents duplication and enforces standards.

Watch the silent Git automation:
- A branch 'phase/1-{slug}' will be created automatically
- Commits will include #sdd-trace:REQ-001 tags
- Everything is logged to .ai/logs/github_auto.log

Run:
  /dev --phase=1

▶️ Your turn."

[Wait for /dev]

Checkpoint: "What branch was created? Look in .ai/logs/github_auto.log — what did Git automation do?"
```

### STEP 5 — Test Phase (`/test`)
```
Instructor says:
"Step 5: Validate everything before merging.

📚 WHY: We need 100% contract coverage to be eligible for auto-merge.
This means every acceptance criterion has a passing test.

Run:
  /test --phase=1

▶️ Your turn."

[Wait for /test]

Checkpoint: "Look at docs/05-reports/ — what does contract-coverage.json show?
Is coverage at 100%? If not, run /fix --auto-fix and re-test."
```

### STEP 6 — Fix (if needed) (`/fix`)
```
Instructor says:
"Step 6: If tests failed, /fix diagnoses and repairs.

📚 WHY: Healing Bot v2 works predictively — it doesn't just fix symptoms,
it traces failures back to spec.yaml acceptance criteria and patches at the source.

If you had failures in Step 5, run:
  /fix --auto-fix

If coverage is already 100%, skip to Step 7.

▶️ Your turn (or skip if all tests passed)."
```

### STEP 7 — Deploy to Preview (`/deploy --preview`)
```
Instructor says:
"Step 7: Deploy! But notice — we choose when to deploy.

📚 WHY: /deploy is EXPLICIT ONLY. Git auto-merge does NOT trigger deployment.
This is the most important safety rule in AIWF. Accidental production deploys
can happen when Git and deployment are coupled. We decouple them by design.

Run:
  /deploy --preview

▶️ Your turn."

[Wait for /deploy --preview]

Checkpoint: "What URL was generated? Open it and check the preview."
```

### STEP 8 — Wrap Up & Next Steps
```
Instructor says:
"🎉 Congratulations! You've completed the full AIWF v7.0.0 workflow:

  ✅ Step 1: /do       — Idea → PRD
  ✅ Step 2: /plan     — PRD → Full Blueprint
  ✅ Step 3: Approval  — Omega Gate v2
  ✅ Step 4: /dev      — Build with Library-First + Silent Git
  ✅ Step 5: /test     — Validate with contract coverage
  ✅ Step 6: /fix      — Repair if needed
  ✅ Step 7: /deploy   — Explicit deployment to preview

Your tutorial session has been saved to:
  docs/00-guides/{date}_tutorial-session.md

When you're ready for production:
  /deploy --prod --confirm

For regional projects:
  Add --region=egypt|redsea|mena to /do, /plan, /dev, /test, /deploy

For more detail on any command:
  Read docs/00-guides/AIWF-Guide.md

What would you like to explore next?"
```

---

## Flags

| Flag | Effect |
| :--- | :--- |
| `--project="idea"` | Use a specific project idea throughout the tutorial |
| `--start=do\|plan\|dev\|test\|fix\|deploy` | Start at a specific command step |
| `--from=step-N` | Resume from a saved step (N = 0-8) |
| `--fast` | Skip checkpoint questions, faster pace |
| `--region=egypt\|redsea\|mena` | Add regional context throughout the tutorial |

---

## Session Log Format

At the end of each tutorial session, the instructor writes:
`docs/00-guides/{YYYY-MM-DD}_tutorial-session.md`

```markdown
# Tutorial Session — {date}
**Steps completed**: {N}/8
**Project used**: {idea}
**Region**: {region or none}

## Checkpoint Answers
- Step 1: {user's answer about REQ-IDs}
- Step 2: {user's answer about validation gates}
...

## Commands Run
- /do "{idea}"
- /plan --from=...
- /dev --phase=1
...

## Next Steps Suggested
...
```

---

*Command version: 7.0.0*
*Library path: 12-meta-engine/meta-orchestration/v7-orchestration/tutorial.md*
*Last updated: 2026-04-23T13:14:08+02:00*
*Reasoning Hash: sha256:tutorial-v7-2026-04-23*
