# Skill: Content Synthesis (v1.0.0)

## Overview
The **Content Synthesis** skill enables agents to generate high-fidelity industrial content by merging structural specs (`sitemap`, `navigation`) with creative specs (`brand-voice`, `seo`).

## Sovereign Protocols
- **P-001**: Always reference `brand-voice-manifest.spec.yaml` before generation.
- **P-002**: Enforce SEO keywords from `seo-optimization.spec.yaml`.
- **P-003**: Output must be section-based and mapped in `content_manifest.json`.

## Implementation Logic
1. **Analyze Topology**: Load sitemap and navigation specs.
2. **Inject Personality**: Apply brand voice constraints.
3. **Optimize Discovery**: Inject semantic SEO layers.
4. **Final Assembly**: Generate physical markdown files in the target workspace.

## Automation
Invoke via `python3 factory/core/content_engine.py`.
Verify via `python3 factory/core/content_validator.py`.
