#!/usr/bin/env python3
import json
import datetime
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACES = ROOT / "workspaces" / "clients"
DASHBOARD_DIR = ROOT / "dashboard"
PROJECTS_DASH_DIR = DASHBOARD_DIR / "projects"
ARCHIVE_DIR = DASHBOARD_DIR / "archive"
INDEX_PATH = ROOT / ".ai" / "memory" / "workspace-index.json"
TEMPLATE_INDEX = ROOT / ".ai" / "templates" / "dashboard" / "index.md"

def sync_dashboards():
    print("🧠 Master Sync: Rendering Modular Widget Dashboard...")
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    PROJECTS_DASH_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run Phase 5 Archive Protocol
    archive_legacy_state()

    summary_data = []

    # Traverse Sovereign Workspaces
    for client_dir in WORKSPACES.iterdir():
        if client_dir.is_dir() and client_dir.name != ".DS_Store":
            client_slug = client_dir.name
            
            for project_dir in client_dir.iterdir():
                if project_dir.is_dir() and project_dir.name.startswith("001_"):
                    project_slug = project_dir.name
                    
                    # Dashboard localized memory
                    dash_memory_path = project_dir / ".ai" / "dashboard" / "memory.json"
                    if dash_memory_path.exists():
                        try:
                            memory = json.loads(dash_memory_path.read_text())
                            # Render Project Page (Simplified logic, not standardizing full widget nesting here yet)
                            render_project_page(client_slug, project_slug, memory)
                            summary_data.append(memory)
                        except Exception as e:
                            print(f"⚠️ Warning: Invalid dashboard memory in {project_slug} - {e}")
                            
    # Render Modular Global Index (Replacing hardcode with Template Parsing)
    render_global_index(summary_data)
    
    # Update invisible index
    update_invisible_index(summary_data)
    print(f"✅ Dashboard Matrix Rendered at {DASHBOARD_DIR.relative_to(ROOT)}")


def archive_legacy_state():
    """Archive Protocol: Moves the current dashboard/index.md to historical storage."""
    current_index = DASHBOARD_DIR / "index.md"
    if current_index.exists():
        timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d')
        exact_time = datetime.datetime.now().strftime('%H%M%S')
        daily_archive_dir = ARCHIVE_DIR / timestamp_str
        daily_archive_dir.mkdir(parents=True, exist_ok=True)
        
        target_name = f"index-{exact_time}.md"
        shutil.copy2(current_index, daily_archive_dir / target_name)
        print(f"📦 Archived previous dashboard state to archive/{timestamp_str}/{target_name}")


def render_project_page(client, project, memory):
    file_name = f"{client}_{project}.md"
    file_path = PROJECTS_DASH_DIR / file_name
    
    content = f"# Project: {project}\n"
    content += f"**Client**: `{client}` | **Health**: {memory.get('health', 0)}/100 | **Status**: {memory.get('status', 'Unknown')}\n"
    content += f"**Progress**: {memory.get('progress_percentage', 0)}%\n\n"
    
    content += "## Plan Phases\n"
    for phase in memory.get("phases", []):
        status_icon = "✅" if phase["status"] == "completed" else "⏳" if phase["status"] == "active" else "⬜"
        content += f"- {status_icon} **{phase['name']}**\n"
        
    content += "\n## Granular Tasks\n"
    for task in memory.get("tasks", []):
        checkbox = "[x]" if task["completed"] else "[ ]"
        content += f"- {checkbox} {task['description']}\n"
        
    content += f"\n*(Auto-Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})*"
    file_path.write_text(content)


def generate_widget_roster(summary_data):
    """Generates the content for widget-project-roster replacement."""
    if not summary_data:
        return "*No active projects detected.*"
    
    out = ""
    for project in summary_data:
        client = project.get("client_id", "Unknown")
        proj_name = project.get("project_id", "Unknown")
        link = f"projects/{client}_{proj_name}.md"
        out += f"- 🏗️ **[{proj_name}]({link})** | {client} | Progress: {project.get('progress_percentage', 0)}%\n"
    return out


def generate_widget_global(summary_data):
    """Generates the content for widget-global-status replacement."""
    return f"**Total Active Monitored Assets**: {len(summary_data)}\n**System Health**: OMEGA-Optimal\n"


def render_global_index(summary_data):
    """Parses .ai/templates/dashboard/index.md and dynamically injects widgets."""
    file_path = DASHBOARD_DIR / "index.md"
    if not TEMPLATE_INDEX.exists():
        print("❌ CRITICAL ERROR: Base Template Index missing.")
        return
        
    template_str = TEMPLATE_INDEX.read_text()
    
    # Execute lazy-load Widget Directives
    roster_widget_data = generate_widget_roster(summary_data)
    global_widget_data = generate_widget_global(summary_data)
    
    template_str = template_str.replace("<!-- INCLUDE: widget-global-status -->", global_widget_data)
    template_str = template_str.replace("<!-- INCLUDE: widget-project-roster -->", roster_widget_data)
    
    # Inject Timestamps
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    template_str = template_str.replace("{{TIMESTAMP}}", timestamp)
    
    file_path.write_text(template_str)


def update_invisible_index(summary_data):
    if INDEX_PATH.exists():
        index = json.loads(INDEX_PATH.read_text())
    else:
        index = {"version": "2.1.0", "clients": {}, "metrics": {}}
        
    index["metrics"]["total_projects"] = len(summary_data)
    index["last_synced"] = datetime.datetime.now().isoformat()
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, indent=2))

if __name__ == "__main__":
    sync_dashboards()
