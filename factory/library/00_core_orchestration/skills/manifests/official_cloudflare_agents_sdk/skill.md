---
name: agents-sdk
description: Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks, MCP servers, chat applications, voice agents, or browser automation. Covers Agent class, state management, callable RPC, Workflows, durable execution, queues, retries, observability, and React hooks. Biases towards retrieval from Cloudflare docs over pre-trained knowledge.
---

# Cloudflare Agents SDK

Your knowledge of the Agents SDK may be outdated. **Prefer retrieval over pre-training** for any Agents SDK task.

## Retrieval Sources

Cloudflare docs: https://developers.cloudflare.com/agents/

| Topic | Docs URL |
|-------|----------|
| Getting started | https://developers.cloudflare.com/agents/getting-started/quick-start/ |
| Agent class | https://developers.cloudflare.com/agents/api-reference/agents-api/ |
| State | https://developers.cloudflare.com/agents/api-reference/store-and-sync-state/ |
| Chat agents | https://developers.cloudflare.com/agents/api-reference/chat-agents/ |
| MCP server | https://developers.cloudflare.com/agents/api-reference/mcp-agent-api/ |
| Durable execution | https://developers.cloudflare.com/agents/api-reference/durable-execution/ |

## Quick Start

```typescript
import { Agent } from 'agents';

export class MyAgent extends Agent {
  async onRequest(request: Request): Promise<Response> {
    return new Response('Hello from agent!');
  }
}
```

## Key Concepts

- **Agent class**: Extends `Agent` or `AIChatAgent` for chat-based agents
- **State**: Use `setState()` and `validateStateChange()` for persistent state
- **Callable methods**: Use `@callable` decorator for RPC methods
- **Scheduling**: Use `schedule()` and `scheduleEvery()` for timed tasks
- **WebSockets**: Implement `onConnect()`, `onMessage()`, `onClose()` hooks
