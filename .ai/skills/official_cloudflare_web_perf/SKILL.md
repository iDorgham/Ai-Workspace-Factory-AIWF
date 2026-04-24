---
name: web-perf
description: Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (LCP, INP, CLS) and supplementary metrics (FCP, TBT, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps. Use when asked to audit, profile, debug, or optimize page load performance, Lighthouse scores, or site speed.
---

# Web Performance Audit

## FIRST: Verify MCP Tools Available

Try calling `navigate_page` or `performance_start_trace`. If unavailable, STOP—the chrome-devtools MCP server isn't configured.

Ask the user to add this to their MCP config:

```json
"chrome-devtools": {
  "type": "local",
  "command": ["npx", "-y", "chrome-devtools-mcp@latest"]
}
```

## Key Guidelines

- **Be assertive**: Verify claims by checking network requests, DOM, or codebase
- **Quantify impact**: Use estimated savings from insights
- **Be specific**: Say "compress hero.png (450KB) to WebP" not "optimize images"
- **Prioritize ruthlessly**: A site with 200ms LCP and 0 CLS is already excellent

## Workflow

1. Navigate to the target URL: `navigate_page(url: "<target-url>")`
2. Start a performance trace: `performance_start_trace(autoStop: true, reload: true)`
3. Analyze Core Web Vitals: `performance_analyze_insight(insightSetId: "...", insightName: "LCPBreakdown")`
4. Check network requests: `list_network_requests(resourceTypes: ["Script", "Stylesheet"])`
5. Take accessibility snapshot: `take_snapshot(verbose: true)`

## Common Insight Names

| Metric | Insight Name |
|--------|--------------|
| LCP | `LCPBreakdown` |
| CLS | `CLSCulprits` |
| Render Blocking | `RenderBlocking` |
