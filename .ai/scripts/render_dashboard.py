#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_FILE = ROOT / "dashboard" / "widget-registry.json"

def render_widget(widget_id, widget_cfg, context_path=None):
    source_path = ROOT / widget_cfg["source"]
    if context_path:
        # If in a project context, the source might be relative to the project
        project_source = Path(context_path) / widget_cfg["source"].split("/")[-1]
        if project_source.exists():
            source_path = project_source

    if not source_path.exists():
        return f"<!-- ⚠ Widget {widget_id} source not found -->"

    if widget_cfg["template"] == "<!-- INCLUDE_RAW -->":
        return source_path.read_text()

    try:
        data = json.loads(source_path.read_text())
        # Very simple template replacement (could use jinja2 if available, but staying deterministic/light)
        template = widget_cfg["template"]
        # Basic {{key}} replacement
        if "metrics" in data:
            template = template.replace("{{metrics.total_clients}}", str(data["metrics"].get("total_clients", 0)))
            template = template.replace("{{metrics.total_projects}}", str(data["metrics"].get("total_projects", 0)))
            template = template.replace("{{metrics.cross_project_patterns_detected}}", str(data["metrics"].get("cross_project_patterns_detected", 0)))
        
        template = template.replace("{{last_synced}}", str(data.get("last_synced", "Never")))
        template = template.replace("{{project_id}}", str(data.get("project_id", "Unknown")))
        template = template.replace("{{health}}", str(data.get("health", 0)))
        template = template.replace("{{progress_percentage}}", str(data.get("progress_percentage", 0)))
        
        return template
    except Exception as e:
        return f"<!-- ⚠ Error rendering {widget_id}: {str(e)} -->"

def generate_dashboard(scope, target_path):
    registry = json.loads(REGISTRY_FILE.read_text())["widgets"]
    output_file = Path(target_path) / "index.md"
    
    content = [f"# {scope.upper()} Dashboard\n"]
    
    for wid, wcfg in registry.items():
        if wcfg["tier"] == scope:
            content.append(render_widget(wid, wcfg, target_path if scope == "project" else None))
            content.append("\n---")
    
    output_file.write_text("\n".join(content))
    print(f"✅ Rendered {scope} dashboard to {output_file.name}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: render_dashboard.py <root|client|project> <target_dir>")
        sys.exit(1)
    
    generate_dashboard(sys.argv[1], sys.argv[2])
