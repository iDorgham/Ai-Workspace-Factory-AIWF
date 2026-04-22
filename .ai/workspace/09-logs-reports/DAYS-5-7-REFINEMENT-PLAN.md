# Days 5-7: Refinement Phase — Planning & Roadmap

**Date:** 2026-04-13  
**Phase:** Refinement & Production Hardening  
**Status:** PLANNING

---

## Overview

Days 5-7 transition from mock tool execution to production-ready integration. The foundation (Phase 2a CLI parsing + Phase 1 tool routing) is solid. This phase focuses on actual tool adapters, cost tracking, health monitoring, and production hardening.

---

## Architecture Transition

### Current State (Days 1-4)
```
User Input
    ↓
Flag Parsing (Phase 2a)
    ↓
Tool Routing (Phase 1)
    ↓
Mock Tool Execution ← DETERMINISTIC FOR TESTING
    ↓
workflow.jsonl (logging)
```

### Target State (Days 5-7)
```
User Input
    ↓
Flag Parsing (Phase 2a)
    ↓
Tool Routing (Phase 1)
    ↓
Actual Tool Adapters ← REAL TOOLS (Claude, Gemini, Copilot, Codex)
    ↓
Cost Tracking (budget awareness)
    ↓
Health Monitoring (tool availability, latency)
    ↓
Error Recovery (retry logic, graceful degradation)
    ↓
workflow.jsonl + tool-performance.jsonl (comprehensive logging)
```

---

## Day 5: Tool Adapter Integration

### Goal
Replace mock tool execution with real tool adapters for Claude, Gemini, Copilot, and Codex.

### Tasks

#### Task 5.1: Claude Adapter (4 hours)
**Deliverables:**
- `.ai/scripts/adapters/[tool]-adapter.py` — Claude-specific implementation
- `tests/day-5-claude-adapter-tests.json` — 5 test cases
- `.ai/scripts/test-[tool]-adapter.py` — Test runner

**Implementation:**
- Inherit from base ToolAdapter class
- Implement `execute(command)` method
- Handle Claude API calls (use Anthropic SDK)
- Implement token counting
- Cost calculation (input/output tokens)
- Error handling (rate limits, context overflow)
- Performance tracking (latency, success rate)

**Test Cases:**
1. Simple command execution
2. Long context handling
3. Rate limit handling
4. API error recovery
5. Performance metrics capture

#### Task 5.2: Gemini Adapter (4 hours)
**Deliverables:**
- `.ai/scripts/adapters/[tool]-adapter.py` — Gemini-specific implementation
- `tests/day-5-gemini-adapter-tests.json` — 5 test cases
- `.ai/scripts/test-[tool]-adapter.py` — Test runner

**Implementation:**
- Inherit from base ToolAdapter class
- Implement `execute(command)` method
- Handle Gemini API calls (use Google SDK)
- Image processing support (multimodal)
- Token counting
- Cost calculation
- Error handling (API errors, timeouts)
- Performance tracking

**Test Cases:**
1. Text-only execution
2. Multimodal (image) execution
3. Vision-specific commands
4. Rate limit recovery
5. Performance metrics

#### Task 5.3: Copilot Adapter (4 hours)
**Deliverables:**
- `.ai/scripts/adapters/[tool]-adapter.py` — Copilot-specific implementation
- `tests/day-5-copilot-adapter-tests.json` — 5 test cases
- `.ai/scripts/test-[tool]-adapter.py` — Test runner

**Implementation:**
- Inherit from base ToolAdapter class
- Implement `execute(command)` method
- Handle Copilot API calls (MS SDK)
- Code-specific optimizations
- Token counting
- Cost calculation
- Error handling
- Performance tracking

**Test Cases:**
1. Code generation
2. Code review
3. Documentation generation
4. API error handling
5. Performance tracking

#### Task 5.4: Codex Adapter (4 hours)
**Deliverables:**
- `.ai/scripts/adapters/[tool]-adapter.py` — Codex-specific implementation
- `tests/day-5-codex-adapter-tests.json` — 5 test cases
- `.ai/scripts/test-[tool]-adapter.py` — Test runner

**Implementation:**
- Inherit from base ToolAdapter class
- Implement `execute(command)` method
- Handle Codex API calls (OpenAI SDK)
- Code generation specialization
- Token counting
- Cost calculation
- Error handling
- Performance tracking

**Test Cases:**
1. Code completion
2. Bug fixing
3. Code explanation
4. Error recovery
5. Performance metrics

#### Task 5.5: Base ToolAdapter Class (2 hours)
**Deliverables:**
- `.ai/scripts/adapters/[tool]-adapter.py` — Abstract base class
- `.ai/scripts/adapters/[adapter-interface].md` — Documentation

**Implementation:**
```python
class ToolAdapter(ABC):
    def __init__(self, tool_name, api_key, config):
        self.tool_name = tool_name
        self.api_key = api_key
        self.config = config
        
    @abstractmethod
    def execute(self, command: str) -> Dict:
        """Execute command via tool API"""
        pass
    
    def count_tokens(self, text: str) -> int:
        """Count tokens for cost calculation"""
        pass
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate API cost"""
        pass
    
    def handle_error(self, error: Exception) -> Dict:
        """Handle tool-specific errors"""
        pass
    
    def track_performance(self, execution_time: float, success: bool):
        """Track latency and success rate"""
        pass
```

#### Task 5.6: Adapter Integration with ToolRouter (2 hours)
**Deliverables:**
- Updated `.ai/scripts/tool-router.py` — Use real adapters instead of mocks
- `.ai/scripts/test-[integration]-with-adapters.py` — Integration tests

**Changes:**
- Replace mock execution with real adapter calls
- Load adapters from adapter registry
- Handle adapter availability at runtime
- Error recovery using fallback chain

### Testing Strategy

**Day 5 Total Tests:** 20 tests (5 per adapter)

```
Claude Adapter Tests (5):
├─ Simple execution ✓
├─ Long context ✓
├─ Rate limit handling ✓
├─ Error recovery ✓
└─ Performance tracking ✓

Gemini Adapter Tests (5):
├─ Text execution ✓
├─ Multimodal execution ✓
├─ Vision commands ✓
├─ Rate limit recovery ✓
└─ Performance tracking ✓

Copilot Adapter Tests (5):
├─ Code generation ✓
├─ Code review ✓
├─ Documentation ✓
├─ Error handling ✓
└─ Performance tracking ✓

Codex Adapter Tests (5):
├─ Code completion ✓
├─ Bug fixing ✓
├─ Explanation ✓
├─ Error recovery ✓
└─ Performance tracking ✓
```

**Expected Pass Rate:** 100% (20/20)

---

## Day 6: Cost Tracking & Budget Management

### Goal
Implement real cost tracking, budget enforcement, and cost-aware routing decisions.

### Tasks

#### Task 6.1: Cost Tracking System (3 hours)
**Deliverables:**
- `.ai/scripts/[cost-tracker].py` — Cost calculation engine
- `.ai/cost-configuration.json` — Per-tool pricing

**Implementation:**
```
Per-Tool Costs:
├─ Claude: $0.003 input / $0.009 output (per 1K tokens)
├─ Gemini: $0.0005 input / $0.0015 output
├─ Copilot: $0.002 input / $0.006 output
└─ Codex: $0.002 input / $0.006 output

Cost Calculation:
input_cost = (input_tokens / 1000) * input_price
output_cost = (output_tokens / 1000) * output_price
total_cost = input_cost + output_cost
```

**Features:**
- Real-time cost tracking
- Per-command cost logging
- Cumulative cost tracking per session
- Tool cost comparison

#### Task 6.2: Budget Management (2 hours)
**Deliverables:**
- `.ai/scripts/[budget-manager].py` — Budget enforcement engine
- `tests/day-6-budget-tests.json` — Test cases

**Implementation:**
- Session budget setting
- Per-command budget checking
- Warn at 70% threshold
- Block execution at 100% threshold
- Cost projection

**Test Cases:**
1. Budget initialization
2. Cost within budget
3. Cost warning (70%)
4. Budget exceeded (block)
5. Multi-command tracking

#### Task 6.3: Cost-Aware Routing (3 hours)
**Deliverables:**
- Updated `.ai/scripts/tool-router.py` — Cost-aware mode
- `.ai/scripts/[cost-optimizer].py` — Cost optimization engine

**Implementation:**
```
Cost-Aware Mode:
├─ Low Cost: Use cheapest tool that solves problem
├─ Balanced: Balance cost + quality
├─ Quality First: Use best tool regardless of cost
└─ Smart: Adaptive based on budget remaining

Routing Decision:
Tool Selection = Rank(quality) + Cost(weight) + Budget(constraint)
```

**Features:**
- Cost-aware tool selection
- Budget-constrained routing
- Cost vs. quality trade-off display
- Projected cost per command

#### Task 6.4: Logging & Analytics (2 hours)
**Deliverables:**
- Enhanced `logs/tool-performance.jsonl` — Cost data
- `.ai/scripts/[cost-report].py` — Cost reporting

**Log Entry Format:**
```json
{
  "timestamp": "2026-04-13T10:30:00Z",
  "command": "/create blog-posts",
  "tool": "copilot",
  "input_tokens": 1250,
  "output_tokens": 3400,
  "input_cost": 0.00375,
  "output_cost": 0.02040,
  "total_cost": 0.02415,
  "session_total_cost": 0.15230,
  "budget_remaining": 4.84770
}
```

#### Task 6.5: Cost Reporting (2 hours)
**Deliverables:**
- `logs/cost-report-[timestamp].json` — Session cost summary
- `.ai/scripts/[generate-cost-report].py` — Report generator

**Report Format:**
```json
{
  "session_date": "2026-04-13",
  "budget_allocated": 5.00,
  "total_spent": 0.15230,
  "budget_remaining": 4.84770,
  "budget_percent_used": 3.05%,
  "commands_executed": 8,
  "average_cost_per_command": 0.01904,
  "by_tool": {
    "copilot": {"cost": 0.08200, "commands": 3},
    "gemini": {"cost": 0.04100, "commands": 2},
    "qwen": {"cost": 0.02930, "commands": 3}
  },
  "cost_trend": "stable"
}
```

### Testing Strategy

**Day 6 Total Tests:** 15 tests

```
Cost Tracking (5):
├─ Cost calculation ✓
├─ Token counting ✓
├─ Multi-tool tracking ✓
├─ Cumulative cost ✓
└─ Cost logging ✓

Budget Management (5):
├─ Budget initialization ✓
├─ Within budget ✓
├─ Warning threshold ✓
├─ Exceeded budget ✓
└─ Multi-command tracking ✓

Cost-Aware Routing (3):
├─ Low cost mode ✓
├─ Balanced mode ✓
└─ Smart mode ✓

Cost Reporting (2):
├─ Report generation ✓
└─ Trend analysis ✓
```

**Expected Pass Rate:** 100% (15/15)

---

## Day 7: Health Monitoring & Production Hardening

### Goal
Add tool health monitoring, advanced error recovery, and production hardening.

### Tasks

#### Task 7.1: Health Monitoring System (3 hours)
**Deliverables:**
- `.ai/scripts/[health-monitor].py` — Tool health tracking
- `.ai/health-status.json` — Current health state

**Implementation:**
```
Health Metrics Per Tool:
├─ Availability (% uptime)
├─ Latency (avg response time)
├─ Success Rate (% successful requests)
├─ Error Rate (% failed requests)
└─ Cost Efficiency (cost per output)

Health Status Levels:
├─ HEALTHY: 95%+ available, <5% errors
├─ DEGRADED: 80-95% available, 5-15% errors
├─ UNAVAILABLE: <80% available, >15% errors
└─ OFFLINE: 0% available, all errors
```

**Features:**
- Real-time health monitoring
- Tool availability detection
- Latency tracking
- Success rate tracking
- Health-based routing decisions

#### Task 7.2: Advanced Error Recovery (3 hours)
**Deliverables:**
- `.ai/scripts/[error-recovery].py` — Error recovery engine
- `tests/day-7-recovery-tests.json` — Error scenarios

**Implementation:**
```
Error Recovery Strategies:
├─ Immediate Fallback: Try next tool in chain
├─ Exponential Backoff: Retry with increasing delay
├─ Circuit Breaker: Temporarily disable unhealthy tools
├─ Graceful Degradation: Use lower-quality but stable tool
└─ Request Simplification: Reduce context/tokens on error
```

**Test Cases:**
1. API timeout recovery
2. Rate limit recovery
3. Context overflow recovery
4. Token limit recovery
5. Tool unavailability recovery

#### Task 7.3: Tool Health Routing (2 hours)
**Deliverables:**
- Updated `.ai/scripts/tool-router.py` — Health-aware mode
- `.ai/scripts/[health-aware-ranker].py` — Dynamic ranking

**Implementation:**
```
Health-Aware Ranking:
Base Rank × Health Multiplier = Effective Rank

Example:
├─ Copilot (Base: 1, Health: HEALTHY 1.0) → Rank: 1.0
├─ Gemini (Base: 2, Health: DEGRADED 0.7) → Rank: 1.4
└─ Codex (Base: 3, Health: HEALTHY 1.0) → Rank: 3.0

Result: Route to Copilot (still rank 1, despite Gemini being unavailable)
```

#### Task 7.4: Circuit Breaker Pattern (2 hours)
**Deliverables:**
- `.ai/scripts/[circuit-breaker].py` — Circuit breaker implementation
- `tests/day-7-circuit-breaker-tests.json` — Test cases

**Implementation:**
```
States:
├─ CLOSED: Tool is healthy, requests flow normally
├─ OPEN: Tool is unhealthy, requests fail fast
└─ HALF_OPEN: Testing if tool recovered

Transitions:
├─ CLOSED → OPEN: After N consecutive failures
├─ OPEN → HALF_OPEN: After timeout duration
└─ HALF_OPEN → CLOSED: If test request succeeds
```

#### Task 7.5: Comprehensive Testing (3 hours)
**Deliverables:**
- `tests/day-7-integration-tests.json` — 15 integration tests
- `.ai/scripts/[run-day-7-tests].py` — Full test runner

**Test Scenarios:**
1. Healthy tool execution
2. Degraded tool fallback
3. Offline tool bypass
4. Multiple tool failures
5. Health recovery
6. Circuit breaker open/close
7. Error recovery with backoff
8. Cost tracking with health
9. Health reporting
10. Combined (cost + health routing)

#### Task 7.6: Production Hardening (2 hours)
**Deliverables:**
- `.ai/scripts/[production-config].py` — Production settings
- `logs/[production-readiness-checklist].md` — Verification

**Hardening Focus:**
- API key management (environment variables, secrets)
- Timeout handling
- Connection pooling
- Rate limit compliance
- Logging & monitoring
- Error tracking
- Performance optimization
- Security (no secrets in logs)

### Testing Strategy

**Day 7 Total Tests:** 15 tests

```
Health Monitoring (3):
├─ Availability tracking ✓
├─ Latency tracking ✓
└─ Success rate tracking ✓

Error Recovery (5):
├─ Timeout recovery ✓
├─ Rate limit recovery ✓
├─ Context overflow recovery ✓
├─ Token limit recovery ✓
└─ Tool unavailability recovery ✓

Health-Aware Routing (3):
├─ Healthy tool selection ✓
├─ Degraded tool fallback ✓
└─ Offline tool bypass ✓

Circuit Breaker (2):
├─ State transitions ✓
└─ Recovery detection ✓

Integration (2):
├─ End-to-end with health ✓
└─ End-to-end with cost ✓
```

**Expected Pass Rate:** 100% (15/15)

---

## Days 5-7 Summary

### Deliverables Count

| Category | Day 5 | Day 6 | Day 7 | Total |
|----------|-------|-------|-------|-------|
| Adapter Implementations | 4 | — | — | 4 |
| Cost System | — | 3 | — | 3 |
| Health System | — | — | 4 | 4 |
| Test Runners | 5 | 2 | 1 | 8 |
| Test Cases | 20 | 15 | 15 | 50 |
| Documentation | 3 | 2 | 2 | 7 |

**Total Files:** 26+ files  
**Total Code:** 4000+ lines  
**Total Tests:** 50 tests  

### Expected Results

**Day 5:** 20/20 tests PASS (100%)  
**Day 6:** 15/15 tests PASS (100%)  
**Day 7:** 15/15 tests PASS (100%)  

**Overall:** 50/50 tests PASS (100%)

---

## Success Criteria

### Functionality
- ✅ All 4 real tool adapters working
- ✅ Cost tracking accurate
- ✅ Budget enforcement working
- ✅ Health monitoring active
- ✅ Error recovery successful
- ✅ Circuit breaker functioning
- ✅ Cost-aware routing active
- ✅ Health-aware routing active

### Quality
- ✅ 100% test pass rate
- ✅ Zero data loss in logging
- ✅ No secrets in logs
- ✅ Error messages clear
- ✅ Performance < 2s per command (avg)
- ✅ Cost calculations accurate
- ✅ Documentation complete

### Integration
- ✅ Phase 2a + Phase 1 + Adapters = seamless flow
- ✅ CLI flags work with real tools
- ✅ Fallback chains work with real tools
- ✅ Cost tracking integrated
- ✅ Health monitoring integrated
- ✅ Error recovery integrated

---

## Architecture After Days 5-7

```
User Input (CLI with flags)
    ↓
Phase 2a: CLI Flag Parsing
├─ Tokenize, extract, parse, validate
└─ Error detection
    ↓
Phase 1: Tool Routing with Intelligence
├─ Cost-aware ranking
├─ Health-aware ranking
├─ Command-based selection
└─ Budget constraint checking
    ↓
Real Tool Adapters (4 tools)
├─ Claude (text, context-heavy)
├─ Gemini (multimodal, vision)
├─ Copilot (code generation)
└─ Codex (code completion)
    ↓
Error Recovery & Health Monitoring
├─ Circuit breaker pattern
├─ Exponential backoff
├─ Graceful degradation
└─ Health tracking
    ↓
Cost Tracking & Budget Management
├─ Per-command cost calculation
├─ Session budget enforcement
├─ Cost-trend analysis
└─ Budget-aware routing
    ↓
Comprehensive Logging
├─ workflow.jsonl (commands + routing)
├─ tool-performance.jsonl (metrics)
├─ cost-tracking.jsonl (costs)
└─ health-status.json (current state)
    ↓
Response to User
```

---

## Risk Mitigation

### Risk 1: API Rate Limits
- **Mitigation:** Exponential backoff + circuit breaker
- **Monitoring:** Track rate limit headers
- **Fallback:** Switch to next tool immediately

### Risk 2: Cost Overruns
- **Mitigation:** Budget enforcement at command level
- **Monitoring:** Real-time cost tracking
- **Fallback:** Use cheaper tool if budget low

### Risk 3: Tool Unavailability
- **Mitigation:** Health monitoring + circuit breaker
- **Monitoring:** Continuous health checks
- **Fallback:** Auto-switch to healthy tool

### Risk 4: API Key Exposure
- **Mitigation:** Environment variables only
- **Monitoring:** Audit logs for key access
- **Fallback:** Rotate keys if exposed

### Risk 5: Performance Degradation
- **Mitigation:** Latency tracking + timeouts
- **Monitoring:** Per-tool latency metrics
- **Fallback:** Reduce token count if slow

---

## Timeline

**Day 5 (16 hours):** 4 adapters + integration = 20 tests PASS  
**Day 6 (12 hours):** Cost tracking + budget = 15 tests PASS  
**Day 7 (12 hours):** Health monitoring + hardening = 15 tests PASS  

**Total: 40 hours of work, 50 tests, 26+ files**

---

## What's Ready to Execute

### Prerequisites
- ✅ Phase 2a (flag parsing) — Complete
- ✅ Phase 1 (tool routing) — Complete
- ✅ Test infrastructure — Complete
- ✅ Logging infrastructure — Complete

### Prerequisites for Real Tools
- Claude API key (environment variable: `CLAUDE_API_KEY`)
- Gemini API key (environment variable: `GEMINI_API_KEY`)
- Copilot API key (environment variable: `COPILOT_API_KEY`)
- Codex API key (environment variable: `CODEX_API_KEY`)

---

## Next Steps to Begin

1. **Confirm API keys available** for all 4 tools
2. **Create Task 5.1** (Claude Adapter) with detailed implementation instructions
3. **Set up per-tool test infrastructure**
4. **Begin Day 5 implementation**

---

*Refinement Phase Plan: 3.2.0-Phase1.3a → Phase 1.4a (production)*  
*Created: 2026-04-13*  
*Status: READY TO EXECUTE*
