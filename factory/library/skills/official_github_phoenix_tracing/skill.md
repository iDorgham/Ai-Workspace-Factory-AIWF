---
name: phoenix-tracing
description: OpenInference semantic conventions and instrumentation for Phoenix AI observability. Use when implementing LLM tracing, creating custom spans, or deploying to production.
license: Apache-2.0
compatibility: Requires Phoenix server. Python skills need arize-phoenix-otel; TypeScript skills need @arizeai/phoenix-otel.
metadata:
  author: oss@arize.com
  version: "1.0.0"
  languages: "Python, TypeScript"
---

# Phoenix Tracing

Comprehensive guide for instrumenting LLM applications with OpenInference tracing in Phoenix. Contains reference files covering setup, instrumentation, span types, and production deployment.

## When to Apply

Reference these guidelines when:

- Setting up Phoenix tracing (Python or TypeScript)
- Creating custom spans for LLM operations
- Adding attributes following OpenInference conventions
- Deploying tracing to production
- Querying and analyzing trace data

## Reference Categories

| Priority | Category        | Description                    | Prefix                     |
| -------- | --------------- | ------------------------------ | -------------------------- |
| 1        | Setup           | Installation and configuration | `setup-*`                  |
| 2        | Instrumentation | Auto and manual tracing        | `instrumentation-*`        |
| 3        | Span Types      | 9 span kinds with attributes   | `span-*`                   |
| 4        | Organization    | Projects and sessions          | `projects-*`, `sessions-*` |
| 5        | Enrichment      | Custom metadata                | `metadata-*`               |
| 6        | Production      | Batch processing, masking      | `production-*`             |
| 7        | Feedback        | Annotations and evaluation     | `annotations-*`            |

## Quick Reference

### 1. Setup (START HERE)

- setup-python (`references/setup_python.md`) - Install arize-phoenix-otel, configure endpoint
- setup-typescript (`references/setup_typescript.md`) - Install @arizeai/phoenix-otel, configure endpoint

### 2. Instrumentation

- instrumentation-auto-python (`references/instrumentation_auto_python.md`) - Auto-instrument OpenAI, LangChain, etc.
- instrumentation-auto-typescript (`references/instrumentation_auto_typescript.md`) - Auto-instrument supported frameworks
- instrumentation-manual-python (`references/instrumentation_manual_python.md`) - Custom spans with decorators
- instrumentation-manual-typescript (`references/instrumentation_manual_typescript.md`) - Custom spans with wrappers

### 3. Span Types (with full attribute schemas)

- span-llm (`references/span_llm.md`) - LLM API calls (model, tokens, messages, cost)
- span-chain (`references/span_chain.md`) - Multi-step workflows and pipelines
- span-retriever (`references/span_retriever.md`) - Document retrieval (documents, scores)
- span-tool (`references/span_tool.md`) - Function/API calls (name, parameters)
- span-agent (`references/span_agent.md`) - Multi-step reasoning agents
- span-embedding (`references/span_embedding.md`) - Vector generation
- span-reranker (`references/span_reranker.md`) - Document re-ranking
- span-guardrail (`references/span_guardrail.md`) - Safety checks
- span-evaluator (`references/span_evaluator.md`) - LLM evaluation

### 4. Organization

- projects-python (`references/projects_python.md`) / projects-typescript (`references/projects_typescript.md`) - Group traces by application
- sessions-python (`references/sessions_python.md`) / sessions-typescript (`references/sessions_typescript.md`) - Track conversations

### 5. Enrichment

- metadata-python (`references/metadata_python.md`) / metadata-typescript (`references/metadata_typescript.md`) - Custom attributes

### 6. Production (CRITICAL)

- production-python (`references/production_python.md`) / production-typescript (`references/production_typescript.md`) - Batch processing, PII masking

### 7. Feedback

- annotations-overview (`references/annotations_overview.md`) - Feedback concepts
- annotations-python (`references/annotations_python.md`) / annotations-typescript (`references/annotations_typescript.md`) - Add feedback to spans

### Reference Files

- fundamentals-overview (`references/fundamentals_overview.md`) - Traces, spans, attributes basics
- fundamentals-required-attributes (`references/fundamentals_required_attributes.md`) - Required fields per span type
- fundamentals-universal-attributes (`references/fundamentals_universal_attributes.md`) - Common attributes (user.id, session.id)
- fundamentals-flattening (`references/fundamentals_flattening.md`) - JSON flattening rules
- attributes-messages (`references/attributes_messages.md`) - Chat message format
- attributes-metadata (`references/attributes_metadata.md`) - Custom metadata schema
- attributes-graph (`references/attributes_graph.md`) - Agent workflow attributes
- attributes-exceptions (`references/attributes_exceptions.md`) - Error tracking

## Common Workflows

- **Quick Start**: setup-{lang} → instrumentation-auto-{lang} → Check Phoenix
- **Custom Spans**: setup-{lang} → instrumentation-manual-{lang} → span-{type}
- **Session Tracking**: sessions-{lang} for conversation grouping patterns
- **Production**: production-{lang} for batching, masking, and deployment

## How to Use This Skill

**Navigation Patterns:**

```bash
# By category prefix
references/setup-*              # Installation and configuration
references/instrumentation-*    # Auto and manual tracing
references/span-*               # Span type specifications
references/sessions-*           # Session tracking
references/production-*         # Production deployment
references/fundamentals-*       # Core concepts
references/attributes-*         # Attribute specifications

# By language
references/*-python.md          # Python implementations
references/*-typescript.md      # TypeScript implementations
```

**Reading Order:**
1. Start with setup-{lang} for your language
2. Choose instrumentation-auto-{lang} OR instrumentation-manual-{lang}
3. Reference span-{type} files as needed for specific operations
4. See fundamentals-* files for attribute specifications

## References

**Phoenix Documentation:**

- [Phoenix Documentation](https://docs.arize.com/phoenix)
- [OpenInference Spec](https://github.com/Arize-ai/openinference/tree/main/spec)

**Python API Documentation:**

- [Python OTEL Package](https://arize-phoenix.readthedocs.io/projects/otel/en/latest/) - `arize-phoenix-otel` API reference
- [Python Client Package](https://arize-phoenix.readthedocs.io/projects/client/en/latest/) - `arize-phoenix-client` API reference

**TypeScript API Documentation:**

- [TypeScript Packages](https://arize-ai.github.io/phoenix/) - `@arizeai/phoenix-otel`, `@arizeai/phoenix-client`, and other TypeScript packages
