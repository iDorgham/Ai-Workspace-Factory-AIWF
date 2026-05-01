# Domain model — Content brief & pack routing

**Planning type:** content (content_pillars / brief-driven skill)

---

## Entities

| Entity | Description | Key attributes |
|--------|-------------|----------------|
| `content_brief` | Input to the skill / agent | `tone`, `channel`, `sector`, `asset_type`, `locale`, `word_count`, `cta`, `banned_claims[]`, `legal_sensitivity` |
| `channel` | Surface | `website`, `blog`, `social`, `video`, `email`, `ads`, `legal_ux` |
| `tone` | Maps to `tone_matrix.md` | e.g. `professional_premium`, `official`, `humorous`, `legal_lean` |
| `sector` | Vertical | `fintech`, `hospitality`, `realestate`, `health`, `generic` |
| `pack_asset` | File in skill pack | path under `examples/` or `prompt_library/` |
| `router_hint` | Advisory mapping | `(sector, channel)` → list of `pack_asset` paths |
| `qa_rubric_row` | Masri QA | criterion id, weight, pass example |

## Relationships

- `content_brief` **uses** many `pack_asset` (via `router_hint` + human override).  
- `content_brief` **must satisfy** `qa_rubric_row` set before ship (human or scripted check).  
- `legal_sensitivity != none` **requires** loading `legal_and_contracts_guidance.md` in pack.

## State (phase execution)

| State | Meaning |
|-------|---------|
| `pending` | Phase scaffolded; density gate not yet PASS |
| `gated` | `density_gate_report.json` PASS |
| `promoted` | Files copied to `factory/…`; manifest 1.2.0; rsync done |
