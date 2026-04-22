---
name: agent-governance
description: |
  Patterns and techniques for adding governance, safety, and trust controls to AI agent systems. Use this skill when:
  - Building AI agents that call external tools (APIs, databases, file systems)
  - Implementing policy-based access controls for agent tool usage
  - Adding semantic intent classification to detect dangerous prompts
  - Creating trust scoring systems for multi-agent workflows
  - Building audit trails for agent actions and decisions
  - Enforcing rate limits, content filters, or tool restrictions on agents
---

# Agent Governance Patterns

Patterns for adding safety, trust, and policy enforcement to AI agent systems.

## Overview

Governance patterns ensure AI agents operate within defined boundaries — controlling which tools they can call, what content they can process, how much they can do, and maintaining accountability through audit trails.

```
User Request → Intent Classification → Policy Check → Tool Execution → Audit Log
                     ↓                      ↓               ↓
              Threat Detection         Allow/Deny      Trust Update
```

## When to Use

- **Agents with tool access**: Any agent that calls external tools (APIs, databases, shell commands)
- **Multi-agent systems**: Agents delegating to other agents need trust boundaries
- **Production deployments**: Compliance, audit, and safety requirements
- **Sensitive operations**: Financial transactions, data access, infrastructure management

## Pattern 1: Governance Policy

```python
from dataclasses import dataclass, field
from enum import Enum

class PolicyAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REVIEW = "review"

@dataclass
class GovernancePolicy:
    name: str
    allowed_tools: list[str] = field(default_factory=list)
    blocked_tools: list[str] = field(default_factory=list)
    blocked_patterns: list[str] = field(default_factory=list)
    max_calls_per_request: int = 100
    require_human_approval: list[str] = field(default_factory=list)

    def check_tool(self, tool_name: str) -> PolicyAction:
        if tool_name in self.blocked_tools:
            return PolicyAction.DENY
        if tool_name in self.require_human_approval:
            return PolicyAction.REVIEW
        if self.allowed_tools and tool_name not in self.allowed_tools:
            return PolicyAction.DENY
        return PolicyAction.ALLOW
```

## Pattern 2: Audit Trail

Log every agent action with timestamp, tool name, inputs, outputs, and policy decision for compliance and debugging.

## Pattern 3: Trust Scoring

Assign trust scores to agents and tools. Higher trust = more permissions. Reduce trust on policy violations.
