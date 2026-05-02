---
name: claude-api
description: "Build, debug, and optimize Claude API / Anthropic SDK apps. Apps built with this skill should include prompt caching. Also handles migrating existing Claude API code between Claude model versions. TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`; user asks for the Claude API, Anthropic SDK, or Managed Agents; user adds/modifies/tunes a Claude feature (caching, thinking, compaction, tool use, batch, files, citations, memory) or model (Opus/Sonnet/Haiku) in a file; questions about prompt caching / cache hit rate in an Anthropic SDK project."
license: Complete terms in LICENSE.txt
---

# Building LLM-Powered Applications with Claude

This skill helps you build LLM-powered applications with Claude.

## Before You Start

Scan the target file for non-Anthropic provider markers — `import openai`, `langchain_openai`, `OpenAI(`, `gpt-4`, etc. If you find any, stop and tell the user that this skill produces Claude/Anthropic SDK code.

## Output Requirement

When the user asks you to add, modify, or implement a Claude feature, your code must call Claude through:

1. **The official Anthropic SDK** for the project's language (`anthropic`, `@anthropic-ai/sdk`, etc.). This is the default whenever a supported SDK exists.
2. **Raw HTTP** — only when the user explicitly asks for cURL/REST/raw HTTP.

Never mix the two. Never fall back to OpenAI-compatible shims.

## Defaults

Unless the user requests otherwise:

- Use Claude Opus 4.7 via model string `claude-opus-4-7`
- Default to adaptive thinking (`thinking: {type: "adaptive"}`) for anything remotely complicated
- Default to streaming for any request that may involve long input, long output, or high `max_tokens`

## Language Detection

Before reading code examples, determine which language the user is working in by looking at project files:
- `*.py`, `requirements.txt`, `pyproject.toml` → **Python**
- `*.ts`, `*.js`, `package.json` → **TypeScript/JavaScript**
- `*.go`, `go.mod` → **Go**
- `*.java`, `pom.xml` → **Java**
