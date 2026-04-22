#!/usr/bin/env python3
"""Runtime status TUI for routing and workflow telemetry."""

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

_scripts = Path(__file__).resolve().parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from paths import REPO_ROOT, logs_dir  # noqa: E402

from rich import box
from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.text import Text
from rich.tree import Tree


WORKSPACE_ROOT = REPO_ROOT
STATE_PATH = WORKSPACE_ROOT / ".ai" / "memory" / "state.json"
WORKFLOW_LOG = logs_dir() / "workflow.jsonl"
TOOL_LOG = logs_dir() / "tool-performance.jsonl"

PIPELINE_STAGES = [
    "setup",
    "research",
    "scrape",
    "create",
    "polish",
    "review",
    "approve",
    "export",
    "archive",
]


def read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open() as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    try:
        with path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    # Ignore malformed lines so one bad entry does not break the dashboard.
                    continue
    except OSError:
        return []
    return rows


def percentile(values, p):
    if not values:
        return 0
    values = sorted(values)
    index = int(round((len(values) - 1) * p))
    return values[index]


def build_metrics():
    state = read_json(STATE_PATH, {})
    workflow_rows = read_jsonl(WORKFLOW_LOG)
    tool_rows = read_jsonl(TOOL_LOG)
    fail_counter = Counter()
    command_stats = defaultdict(lambda: {"runs": 0, "fallbacks": 0, "low_confidence": 0})
    latencies = []

    for row in tool_rows:
        command = row.get("command", "unknown")
        command_stats[command]["runs"] += 1
        if row.get("tool_rank", 1) > 1 or row.get("fallback_from"):
            command_stats[command]["fallbacks"] += 1
        if row.get("failure_type") == "low_confidence_extraction":
            command_stats[command]["low_confidence"] += 1
        latency = row.get("latency_ms")
        if isinstance(latency, (int, float)):
            latencies.append(latency)
        if row.get("failure_type"):
            fail_counter[row["failure_type"]] += 1

    return {
        "state": state,
        "workflow_events": len(workflow_rows),
        "tool_events": len(tool_rows),
        "p50_latency_ms": int(median(latencies)) if latencies else 0,
        "p95_latency_ms": int(percentile(latencies, 0.95)),
        "top_failures": fail_counter.most_common(5),
        "command_stats": command_stats,
        "latencies": latencies,
        "tool_rows": tool_rows,
    }


def build_pipeline_tree(pipeline_state):
    current_stage = pipeline_state.get("current_stage", "unknown")
    completed = set(pipeline_state.get("stages_completed", []))
    tree = Tree("[bold cyan]Pipeline Checkpoints[/bold cyan]", guide_style="bright_black")

    for stage in PIPELINE_STAGES:
        if stage == current_stage:
            style = "yellow"
            marker = "◉"
            state_label = "CURRENT"
        elif stage in completed:
            style = "green"
            marker = "●"
            state_label = "DONE"
        else:
            style = "bright_black"
            marker = "○"
            state_label = "PENDING"
        tree.add(f"[{style}]{marker} {stage:<8} [{state_label}][/{style}]")
    return tree


def build_checkpoint_table(state):
    workspace_state = state.get("workspace_state", {})
    quality_state = state.get("quality_state", {})
    active_content = state.get("active_content", {})

    checkpoints = [
        ("Competitors Registered", workspace_state.get("competitors_registered", 0) > 0),
        ("Review Passed", bool(quality_state.get("overall_pass"))),
        ("Content Approved", bool(active_content.get("last_approved"))),
    ]

    table = Table(box=box.SIMPLE_HEAD, expand=True)
    table.add_column("Checkpoint")
    table.add_column("Status", justify="right")
    for name, ok in checkpoints:
        status = "[green]READY[/green]" if ok else "[red]BLOCKED[/red]"
        table.add_row(name, status)
    return table


def build_progress_bar(completed_count):
    total = len(PIPELINE_STAGES)
    percent = (completed_count / total) * 100 if total else 0
    bar = ProgressBar(total=total, completed=completed_count)
    return Group(
        Text("Pipeline Progress", style="bold"),
        bar,
        Text(f"{completed_count}/{total} ({percent:.0f}%)", style="cyan"),
    )


def build_header_panel(metrics, compact=False):
    pipeline = metrics["state"].get("pipeline_state", {})
    stage = pipeline.get("current_stage", "unknown")
    command = pipeline.get("last_command", "none")
    agent = pipeline.get("last_agent", "none")
    last_status = pipeline.get("last_status", "unknown")

    if compact:
        title = f"[bold cyan]Sovereign Runtime[/bold cyan] • [yellow]{stage}[/yellow] • [magenta]{last_status}[/magenta]"
        return Panel(title, border_style="cyan", expand=True)

    content = (
        f"[bold]Current stage:[/bold] [yellow]{stage}[/yellow]\n"
        f"[bold]Last command:[/bold] {command}\n"
        f"[bold]Last agent:[/bold] {agent}\n"
        f"[bold]Last status:[/bold] [magenta]{last_status}[/magenta]\n"
        f"[bold]Workflow events:[/bold] {metrics['workflow_events']}  "
        f"[bold]Tool events:[/bold] {metrics['tool_events']}"
    )
    return Panel(content, title="GALLERIA RUNTIME STATUS", border_style="cyan", expand=True)


def build_metrics_table(metrics):
    table = Table(title="Latency & Telemetry", box=box.SIMPLE, expand=True)
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("P50 latency (ms)", str(metrics["p50_latency_ms"]))
    table.add_row("P95 latency (ms)", str(metrics["p95_latency_ms"]))
    table.add_row("Workflow events", str(metrics["workflow_events"]))
    table.add_row("Tool events", str(metrics["tool_events"]))
    return table


def build_failures_panel(metrics):
    if not metrics["top_failures"]:
        content = Text("No failures recorded.", style="green")
        return Panel(content, title="Top Failure Reasons", border_style="green", expand=True)

    table = Table(box=box.SIMPLE_HEAD, expand=True)
    table.add_column("Failure Type")
    table.add_column("Count", justify="right")
    for reason, count in metrics["top_failures"]:
        style = "red" if count > 5 else "yellow"
        table.add_row(reason, f"[{style}]{count}[/{style}]")
    return Panel(table, title="Top Failure Reasons", border_style="red", expand=True)


def build_routing_quality_panel(metrics):
    table = Table(box=box.SIMPLE_HEAD, expand=True)
    table.add_column("Command")
    table.add_column("Runs", justify="right")
    table.add_column("Fallback %", justify="right")
    table.add_column("Low-Conf %", justify="right")
    for command, stats in sorted(metrics["command_stats"].items()):
        runs = stats["runs"] or 1
        fallback_rate = (stats["fallbacks"] / runs) * 100
        low_conf = (stats["low_confidence"] / runs) * 100
        table.add_row(command, str(stats["runs"]), f"{fallback_rate:.1f}%", f"{low_conf:.1f}%")
    return Panel(table, title="Command Routing Quality", border_style="blue", expand=True)


def sparkline(values):
    if not values:
        return "n/a"
    bars = "▁▂▃▄▅▆▇█"
    v_min = min(values)
    v_max = max(values)
    if v_min == v_max:
        return bars[0] * len(values)
    chars = []
    for value in values:
        normalized = (value - v_min) / (v_max - v_min)
        idx = min(len(bars) - 1, int(normalized * (len(bars) - 1)))
        chars.append(bars[idx])
    return "".join(chars)


def trend_direction(values, invert=False):
    if len(values) < 2:
        return "[dim]→ flat[/dim]"
    first = values[0]
    last = values[-1]
    delta = last - first
    if delta == 0:
        return "[dim]→ flat[/dim]"

    improving = delta < 0 if not invert else delta > 0
    worsening = not improving
    if improving:
        return "[green]↓ improving[/green]"
    if worsening:
        return "[red]↑ worsening[/red]"
    return "[dim]→ flat[/dim]"


def build_trends_panel(metrics, trend_window):
    latencies = metrics.get("latencies", [])
    latency_window = latencies[-trend_window:]

    tool_rows = metrics.get("tool_rows", [])
    failure_series = []
    for row in tool_rows[-trend_window:]:
        failure_series.append(1 if row.get("failure_type") else 0)

    latency_trend = sparkline(latency_window)
    failure_trend = sparkline(failure_series)
    latency_direction = trend_direction(latency_window, invert=False)
    failure_direction = trend_direction(failure_series, invert=False)

    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("Signal")
    table.add_column("Trend")
    table.add_column("Direction")
    table.add_column("Window", justify="right")
    table.add_row("Latency (ms)", f"[cyan]{latency_trend}[/cyan]", latency_direction, str(len(latency_window)))
    table.add_row("Failure Drift", f"[yellow]{failure_trend}[/yellow]", failure_direction, str(len(failure_series)))
    table.add_row("Failure Ratio", f"{sum(failure_series)}/{len(failure_series) if failure_series else 0}", "[dim]-[/dim]", "recent")
    return Panel(table, title=f"Mini Trends (last {trend_window})", border_style="magenta", expand=True)


def build_dashboard(compact=False, watch=False, trend_window=20):
    metrics = build_metrics()
    pipeline_state = metrics["state"].get("pipeline_state", {})
    completed = set(pipeline_state.get("stages_completed", []))
    completed_count = len(completed.intersection(PIPELINE_STAGES))

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=5 if compact else 8),
        Layout(name="progress", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=3),
    )
    layout["left"].split_column(
        Layout(name="metrics", ratio=1),
        Layout(name="failures", ratio=1),
        Layout(name="trends", ratio=1),
    )
    layout["right"].split_column(
        Layout(name="pipeline", ratio=2),
        Layout(name="routing", ratio=2),
    )

    layout["header"].update(build_header_panel(metrics, compact=compact))
    layout["progress"].update(Panel(build_progress_bar(completed_count), border_style="cyan", padding=(0, 1)))
    layout["metrics"].update(build_metrics_table(metrics))
    layout["failures"].update(build_failures_panel(metrics))
    layout["trends"].update(build_trends_panel(metrics, trend_window))
    layout["pipeline"].update(
        Panel(Group(build_pipeline_tree(pipeline_state), build_checkpoint_table(metrics["state"])),
              title="Pipeline & Checkpoints",
              border_style="cyan",
              expand=True)
    )
    layout["routing"].update(build_routing_quality_panel(metrics))

    if watch:
        spinner = Progress(
            SpinnerColumn(style="cyan"),
            TextColumn("[bold cyan]Watching telemetry...[/bold cyan]"),
            TextColumn("Press Ctrl+C to exit"),
        )
        spinner.add_task("watch", total=None)
        layout["footer"].update(Align.left(spinner))
    else:
        layout["footer"].update(Panel("[cyan]Snapshot mode[/cyan] • use [bold]--watch[/bold] for live updates", border_style="cyan"))
    return layout


def parse_args():
    parser = argparse.ArgumentParser(description="Sovereign runtime status dashboard.")
    parser.add_argument("--watch", action="store_true", help="Run in live refresh mode.")
    parser.add_argument("--interval", type=float, default=1.0, help="Refresh interval in seconds for --watch.")
    parser.add_argument("--compact", action="store_true", help="Use compact header mode.")
    parser.add_argument("--trend-window", type=int, default=20, help="Number of latest samples used for trend lines.")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.interval <= 0:
        raise SystemExit("--interval must be a positive number.")
    if args.trend_window <= 0:
        raise SystemExit("--trend-window must be a positive integer.")

    if args.watch:
        with Live(
            build_dashboard(compact=args.compact, watch=True, trend_window=args.trend_window),
            refresh_per_second=max(1, int(1 / args.interval)),
            screen=True,
        ) as live:
            while True:
                live.update(build_dashboard(compact=args.compact, watch=True, trend_window=args.trend_window))
                time.sleep(args.interval)
    else:
        from rich.console import Console

        console = Console()
        console.print(build_dashboard(compact=args.compact, watch=False, trend_window=args.trend_window))


if __name__ == "__main__":
    main()
