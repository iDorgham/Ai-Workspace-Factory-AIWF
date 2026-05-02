# Content Brief — C-09-DEVTO
**Dev.to: spec_density_gate_v2 Deep-Dive**

| Field | Value |
|-------|-------|
| piece_id | C-09-DEVTO |
| channel | dev_to |
| pillar | Density |
| persona | Pragmatic Dev |
| publish_day | 10 |
| word_count_target | 1600 words |
| primary_keyword | AI spec density gate |
| secondary_keywords | SDD methodology, AI planning framework, spec-driven development |
| cli_adapter | claude |
| law_151_flag | false |
| status | briefed |

## Hook
"I wrote a script that blocks git commits when your AI spec is too thin. Here's why that matters."

## Proof Points
1. The 6 gates: minimum_file_count, required_top_level_files, c4_diagrams, required_subdirectories, tasks_minimum, phase_spec_valid
2. Exit codes: 0 = pass, 1 = warn (draft), 2 = hard block (non-draft) — integrates with pre-commit and CI
3. Real density gate output with reasoning_hash — deterministic, auditable

## Structure
1. The problem: AI specs degrade within 48 hours of first commit
2. What spec density means (files + structure + tasks + C4)
3. The 6 gates — each explained with example pass/fail
4. Integration: pre-commit hook + GitHub Actions step
5. The reasoning hash — why every gate run is deterministic and traceable
6. Using it with 7 CLI adapters
7. Full script link

## Front Matter (Dev.to)
```
---
title: "I built a git gate that blocks commits when your AI specs are too thin"
tags: [ai, devops, architecture, productivity]
canonical_url: https://github.com/AIWF
cover_image: [density_gate_diagram.png]
---
```

## CTA
"The full spec_density_gate_v2.py is in the AIWF repo. Drop a ⭐ if you find it useful."
