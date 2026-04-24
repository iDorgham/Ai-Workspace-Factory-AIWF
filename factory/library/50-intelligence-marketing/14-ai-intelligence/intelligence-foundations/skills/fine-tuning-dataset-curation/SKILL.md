---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🧪 Fine-Tuning & Dataset Curation (Omega-tier)


## Purpose
Enforce professional standards for curating high-fidelity datasets and executing model fine-tuning (SFT/RLHF) pipelines. This skill ensures that AI models are specialized for unique domain knowledge (e.g., UAE Legal, Medical, or Sovereign Factory Specs) without catastrophic forgetting.

---

## Technique 1 — Dataset Purity & Formatting

### The JSONL Pipeline
- **Rule**: All training data must be stored in `.jsonl` format with specific `System`, `User`, and `Assistant` roles.
- **Deduplication**: Run a **Cosine Similarity** check on the dataset before training to remove redundant examples that dilute the model's focus.
- **Anonymization**: PII (Personally Identifiable Information) must be scrubbed using automated RegEx and LLM-validation nodes before training.

---

## Technique 2 — Fine-Tuning Protocols (SFT/DPO)

### SFT (Supervised Fine-Tuning)
- **Goal**: Teach the model a new "Style" or "Instruction Format."
- **Batch Size**: 4-8 for smaller datasets; 16-32 for large scale.
- **Learning Rate**: Use `2e-5` for stable feature absorption.

### DPO (Direct Preference Optimization)
- **Goal**: Align the model with "Human-Preferred" outputs without a heavy reward model.
- **Protocol**: Provide "Chosen" vs. "Rejected" response pairs to refine the model's value alignment.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Over-Fitting** | Hallucinations on non-training data | Use a diverse "Hold-out" test set and monitor loss curves. |
| **Low-Quality Context** | "Garbage In, Garbage Out" | Manually verify a 10% random sample of the dataset for accuracy. |
| **Catastrophic Forgetting** | Loss of general logic | Use a "Low-Rank Adaptation" (LoRA) or QLoRA approach for efficiency. |

---

## Success Criteria (Fine-Tuning QA)
- [ ] Training loss curve shows smooth convergence.
- [ ] Validation accuracy > 85% on out-of-sample data.
- [ ] Model adherence to "Sovereign Formatting Rules" is 100%.
- [ ] Dataset includes regional edge-cases (e.g., Bilingual code-switching).
