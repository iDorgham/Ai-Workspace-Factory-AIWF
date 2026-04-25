# Design Document — Phase 05: Validation & Handoff

**Reasoning Hash:** sha256:aiwf-v21-launch-content-05-validation-handoff-2026-04-25

---

## 1. KPI Measurement Architecture

Three checkpoints run after publication:
- **Day 7:** Early signal check — is any channel significantly over/under-performing?
- **Day 14:** Mid-point — adjust distribution if needed (boost underperforming pieces)
- **Day 30:** Final measurement against all SMART objectives from Phase 01

---

## 2. Retrospective Framework

The retro answers four questions:
1. **What hit the targets?** (SMART objectives: GitHub stars, MENA content, LinkedIn, README clarity)
2. **What missed and why?** (Attribution: wrong persona assumption, wrong channel, wrong timing)
3. **What would we change in the blueprint?** (Phase 02 improvements for next content plan)
4. **Persona update:** Were the 4 personas accurate? Any new persona signals discovered?

---

## 3. Mirror Sync + Plan Closure

```
factory/library/planning/content/aiwf-v21-launch-content-strategy/
  ├── phase-01-discovery/   (full mirror)
  ├── phase-02-blueprint/   (full mirror)
  ├── phase-03-detailed-design/ (full mirror)
  ├── phase-04-tasks-contracts/ (full mirror)
  └── phase-05-validation-handoff/ (full mirror)

_manifest.yaml update:
  content_plans:
    - slug: "aiwf-v21-launch-content-strategy"
      status: "completed"
      closed: "2026-05-23"
```

---

## 4. Lessons to Feed Forward

KPI results must be written to `.ai/logs/ledgers/tool_performance.jsonl` (content section)
so brainstorm_agent has real signal data for the next plan's F5 pattern detection.
