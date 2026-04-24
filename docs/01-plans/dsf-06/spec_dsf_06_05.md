# 📐 spec_dsf_06_05: Recursive Skill Synthesis

Implements the automated synthesis of complex industrial skills from multi-agent interaction logs and architectural mutations.

## 📋 Narrative
Manual skill creation is a bottleneck. We implement **Recursive Skill Synthesis**, where the `RecursiveEvolutionEngine` analyzes successful materialization patterns and automatically codifies them into reusable skills. This allows the factory to "learn" new architectural patterns—such as a new vertical adaptation or sync protocol—and make them available for all future shards.

## 🛠️ Key Details
- **Logic**: Pattern Recognition + Manifest Synthesis.
- **Location**: `.ai/skills/`.
- **Feature**: Skill auto-promotion to `factory/library/`.

## 📋 Acceptance Criteria
- [ ] New complex skill synthesized and promoted to library.
- [ ] 0 manual code required for skill manifestation.
- [ ] Verified dependency resolution for synthesized skills.

## 🛠️ spec.yaml
```yaml
phase_id: dsf-06
evolution_hash: sha256:dsf-v20-06-05-o5p6q7
acceptance_criteria:
  - skill_synthesis_autonomy_verified
  - library_promotion_pass
  - dependency_resolution_verified
test_fixture: tests/singularity/skill_synth_audit.py
regional_compliance: LAW151-MENA-SKILL-SOVEREIGNTY
```
