# 🛰️ SPEC: Neural Fabric (v14.0)
**Phase:** 9 | **Status:** DRAFT | **Reasoning Hash:** sha256:v14-spec-2026-04-23

---

## 1. Executive Summary
Phase 9 moves the factory logic directly into the neural weights of local, fine-tuned LLMs. This achieves deterministic, sub-second code synthesis.

---

## 2. Requirements (REQ-NEURAL)

### [REQ-NEURAL-001] — Local Neural Nodes
- **AC**: Support for Llama.cpp and MLX backends on local hardware.
- **AC**: Latency for a standard component synthesis MUST be < 500ms.

### [REQ-NEURAL-002] — Latent Synthesis Engine
- **AC**: Autonomous generation of "Candidate Projects" in the latent space before human commitment.

---

## 3. Architecture
- **Neural Runner**: `factory/core/neural_runner.py`.
- **Weight Registry**: `factory/knowledge/model_registry.json`.
