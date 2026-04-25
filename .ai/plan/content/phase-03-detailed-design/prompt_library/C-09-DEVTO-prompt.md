# CLI Prompt: Dev.to Deep-Dive — C-09-DEVTO

**Task:** T-C03-01 — Generate Dev.to article on spec_density_gate_v2
**Works with:** Claude (primary), Gemini (fallback)

---

```
AIWF v21.0.0 Content Generation Request

Planning Type: content
Piece ID: C-09-DEVTO
Channel: Dev.to
Pillar: Density
Persona: Pragmatic Dev

Write a 1600-word Dev.to article with the following structure:

Front matter:
---
title: "I built a git gate that blocks commits when your AI specs are too thin"
tags: [ai, devops, architecture, productivity]
canonical_url: https://github.com/[AIWF_REPO]
---

Section 1 — The Problem (200 words)
AI specs degrade within 48 hours of first commit. Why. What the symptoms look like. What happens downstream.

Section 2 — What Spec Density Means (250 words)
Define: minimum file count, required structure, mandatory tasks, C4 diagrams.
Include the 7 required top-level files by name.

Section 3 — The 6 Gates (400 words)
For each gate: name, what it checks, example pass output, example fail output.
Gates: minimum_file_count, required_top_level_files, c4_diagrams, required_subdirectories, tasks_minimum, phase_spec_valid.

Section 4 — Integration (250 words)
Pre-commit hook setup (2 commands).
GitHub Actions step (show the YAML snippet from aiwf-industrial-pipeline.yml).
Exit codes: 0 = pass, 1 = warn, 2 = hard block.

Section 5 — The Reasoning Hash (200 words)
Why every gate run produces a deterministic sha256 hash.
How this enables audit trails across 7 CLI adapters.

Section 6 — CTA (100 words)
Open source. Link to repo. Star ask. Arabic community invite.

Brand voice: authoritative-yet-accessible. No hype adjectives. Numbers over adjectives.
Forbidden: game-changing, revolutionary, seamless, disruptive.

Reasoning Hash: sha256:aiwf-v21-launch-content-03-C09-devto-2026-04-25
```
