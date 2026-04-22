# ⚡ Agent Computational Velocity Protocol (Omega-Tier)


## Purpose
Enforce maximum computational efficiency for LLM Agents operating within the Sovereign Workspace. This skill reduces **Token Bloat** and minimizes **First-Time-to-Byte (TTFB) Latency**, effectively making agents run faster, cheaper, and with higher precision.

---

## Technique 1 — Context Pruning (The "Need-to-Know" Rule)

### The "Over-Context" Anti-Pattern
- **Issue**: Feeding an agent 50 files when it only needs the `SKILL.md` causes massive latency spikes and "Attention Sink" (the agent forgets the primary instruction).
- **Protocol**: 
  - Never parse the entire `factory/library/` directory. 
  - Use specific metadata pointers: `dependencies: [skill-a, skill-b]` to execute localized RAG (Retrieval-Augmented Generation) limited to a maximum of 3 files per task.

---

## Technique 2 — JSON-First Terminal Output

- **The Protocol**: Remove all conversational padding from agent outputs (e.g., "Certainly! I will now do X."). 
- **System Injection**: To force high-speed processing, append this to the agent's baseline routing logic:
  > `CRITICAL SYSTEM RULE: Output strictly the `<COMMAND>` or `<JSON>` required for execution. Zero conversational filler. Maximize token efficiency.`
- **Result**: Inference speed increases by up to 40% as the model stops predicting unnecessary linguistic tokens.

---

## Technique 3 — Tool Concurrency (Parallel Execution)

- **Issue**: Agents executing commands sequentially (e.g., Check file -> Wait -> Edit file -> Wait) causes massive operational drag.
- **Protocol**: Stack non-dependent tools in a single execution Turn. For instance, when scaffolding an industry vertical, `write_to_file` should generate 3 templates concurrently rather than running a single IO operation per LLM call.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **"Read All" Parsing** | 30+ second latency | Use `view_file` with precise `StartLine`/`EndLine` parameters to index only the modified blocks. |
| **Monolithic Prompts** | Agent "hallucinates" task | Break large executions into sequential "Task Modules" in `task.md`, updating the context window at each step. |
| **Politeness Tokens** | Wasted computation | Strip all "Hello" and "Please" logic from internal scripts (`audit_library.py`, CLI routers); they are machines, communicate via strictly-typed variables. |

---

## Success Criteria (Velocity QA)
- [ ] Agent responds to simple operations in < 3 seconds.
- [ ] Context window usage for standard tasks does not exceed 15% of the model's maximum limit.
- [ ] Tool calls are parallelized whenever logically possible.
- [ ] Outputs are stripped of unnecessary conversational padding.
