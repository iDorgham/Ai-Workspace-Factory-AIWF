---
description: Run performance and quality benchmarks across the workspace.
cluster: developing
category: commands
display_category: Commands
id: commands:developing/commands/benchmark
version: 10.0.0
domains: [engineering-core]
sector_compliance: pending
---
# /benchmark

Invokes specialized audit subagents to score the current workspace against performance, accessibility, and brand invariants.

## Usage
`/benchmark [--scope full|ui|api] [--target mobile|desktop]`

## Tasks
1. Execute `perf-auditor` for Core Web Vitals.
2. Run `brand-guidelines-auditor` for aesthetic compliance.
3. Pulse the `security-scanner-wrapper` for high-risk vulnerabilities.
4. Output a `benchmark-report.md`.

## Constraints
- Must be run on a consistent environment (e.g., staging).
- Results must be compared against the last `benchmark-report.md` to identify regressions.
