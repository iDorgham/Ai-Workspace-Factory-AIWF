---
name: phoenix-evals
description: Build and run evaluators for AI/LLM applications using Phoenix.
license: Apache-2.0
compatibility: Requires Phoenix server. Python skills need phoenix and openai packages; TypeScript skills need @arizeai/phoenix-client.
metadata:
  author: oss@arize.com
  version: "1.0.0"
  languages: "Python, TypeScript"
---

# Phoenix Evals

Build evaluators for AI/LLM applications. Code first, LLM for nuance, validate against humans.

## Quick Reference

| Task | Files |
| ---- | ----- |
| Setup | setup-python (`references/setup_python.md`), setup-typescript (`references/setup_typescript.md`) |
| Decide what to evaluate | evaluators-overview (`references/evaluators_overview.md`) |
| Choose a judge model | fundamentals-model-selection (`references/fundamentals_model_selection.md`) |
| Use pre-built evaluators | evaluators-pre-built (`references/evaluators_pre_built.md`) |
| Build code evaluator | evaluators-code-python (`references/evaluators_code_python.md`), evaluators-code-typescript (`references/evaluators_code_typescript.md`) |
| Build LLM evaluator | evaluators-llm-python (`references/evaluators_llm_python.md`), evaluators-llm-typescript (`references/evaluators_llm_typescript.md`), evaluators-custom-templates (`references/evaluators_custom_templates.md`) |
| Batch evaluate DataFrame | evaluate-dataframe-python (`references/evaluate_dataframe_python.md`) |
| Run experiment | experiments-running-python (`references/experiments_running_python.md`), experiments-running-typescript (`references/experiments_running_typescript.md`) |
| Create dataset | experiments-datasets-python (`references/experiments_datasets_python.md`), experiments-datasets-typescript (`references/experiments_datasets_typescript.md`) |
| Generate synthetic data | experiments-synthetic-python (`references/experiments_synthetic_python.md`), experiments-synthetic-typescript (`references/experiments_synthetic_typescript.md`) |
| Validate evaluator accuracy | validation (`references/validation.md`), validation-evaluators-python (`references/validation_evaluators_python.md`), validation-evaluators-typescript (`references/validation_evaluators_typescript.md`) |
| Sample traces for review | observe-sampling-python (`references/observe_sampling_python.md`), observe-sampling-typescript (`references/observe_sampling_typescript.md`) |
| Analyze errors | error-analysis (`references/error_analysis.md`), error-analysis-multi-turn (`references/error_analysis_multi_turn.md`), axial-coding (`references/axial_coding.md`) |
| RAG evals | evaluators-rag (`references/evaluators_rag.md`) |
| Avoid common mistakes | common-mistakes-python (`references/common_mistakes_python.md`), fundamentals-anti-patterns (`references/fundamentals_anti_patterns.md`) |
| Production | production-overview (`references/production_overview.md`), production-guardrails (`references/production_guardrails.md`), production-continuous (`references/production_continuous.md`) |

## Workflows

**Starting Fresh:**
observe-tracing-setup (`references/observe_tracing_setup.md`) → error-analysis (`references/error_analysis.md`) → axial-coding (`references/axial_coding.md`) → evaluators-overview (`references/evaluators_overview.md`)

**Building Evaluator:**
fundamentals (`references/fundamentals.md`) → common-mistakes-python (`references/common_mistakes_python.md`) → evaluators-{code|llm}-{python|typescript} → validation-evaluators-{python|typescript}

**RAG Systems:**
evaluators-rag (`references/evaluators_rag.md`) → evaluators-code-* (retrieval) → evaluators-llm-* (faithfulness)

**Production:**
production-overview (`references/production_overview.md`) → production-guardrails (`references/production_guardrails.md`) → production-continuous (`references/production_continuous.md`)

## Reference Categories

| Prefix | Description |
| ------ | ----------- |
| `fundamentals-*` | Types, scores, anti-patterns |
| `observe-*` | Tracing, sampling |
| `error-analysis-*` | Finding failures |
| `axial-coding-*` | Categorizing failures |
| `evaluators-*` | Code, LLM, RAG evaluators |
| `experiments-*` | Datasets, running experiments |
| `validation-*` | Validating evaluator accuracy against human labels |
| `production-*` | CI/CD, monitoring |

## Key Principles

| Principle | Action |
| --------- | ------ |
| Error analysis first | Can't automate what you haven't observed |
| Custom > generic | Build from your failures |
| Code first | Deterministic before LLM |
| Validate judges | >80% TPR/TNR |
| Binary > Likert | Pass/fail, not 1-5 |
