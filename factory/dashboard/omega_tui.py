import os
import json
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from datetime import datetime

class OmegaDashboard:
    def __init__(self, factory_root):
        self.factory_root = factory_root
        self.console = Console()
        self.workspaces_path = os.path.join(factory_root, "workspaces")

    def get_workspace_data(self):
        """Aggregate data from all workspaces."""
        data = []
        # Support both flat and nested workspace structures
        potential_paths = [
            self.workspaces_path,
            os.path.join(self.workspaces_path, "01-Personal"),
            os.path.join(self.workspaces_path, "02-Clients")
        ]
        
        all_dirs = []
        for p in potential_paths:
            if os.path.exists(p):
                for d in os.listdir(p):
                    full_path = os.path.join(p, d)
                    if os.path.isdir(full_path):
                        # Find 001_ subfolders
                        for sub in os.listdir(full_path):
                            sub_p = os.path.join(full_path, sub)
                            if os.path.isdir(sub_p) and (sub.startswith("001_") or os.path.exists(os.path.join(sub_p, ".ai"))):
                                all_dirs.append(sub_p)
                        # Also check the dir itself if it's a project
                        if d.startswith("smoke_") or os.path.exists(os.path.join(full_path, ".ai")):
                            all_dirs.append(full_path)

        # De-duplicate
        all_dirs = list(set(all_dirs))

        for ws in sorted(all_dirs):
            name = os.path.basename(ws)
            ai_path = os.path.join(ws, ".ai")
            status = "🟢 ACTIVE" if os.path.exists(ai_path) else "🔴 INACTIVE"
            
            # Try to get sync status
            sync_log = os.path.join(ws, ".ai/logs/sync.log")
            sync_ver = "v6.0.0"
            if os.path.exists(sync_log):
                with open(sync_log, "r") as f:
                    last_line = f.readlines()[-1]
                    if "SYNC v7.2.0" in last_line:
                        sync_ver = "v7.2.0 ✅"
            
            # Last mutation
            last_mod = datetime.fromtimestamp(os.path.getmtime(ws)).strftime("%Y-%m-%d %H:%M")
            
            data.append({
                "name": name,
                "status": status,
                "version": sync_ver,
                "last_mod": last_mod
            })
        return data

    def generate_table(self):
        table = Table(title="AIWF OMEGA COMMAND CENTER", expand=True, border_style="cyan")
        table.add_column("Workspace", style="bold white")
        table.add_column("Status", justify="center")
        table.add_column("Orchestration", justify="center")
        table.add_column("Last Activity", justify="right", style="dim")

        workspaces = self.get_workspace_data()
        for ws in workspaces:
            table.add_row(ws["name"], ws["status"], ws["version"], ws["last_mod"])
        return table

    def run(self):
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        layout["header"].update(Panel(Text("🛰️ AIWF v7.5.0 — Omega Dash Mode", justify="center", style="bold cyan")))
        layout["footer"].update(Panel(Text("Press Ctrl+C to exit | Swarm Router: ACTIVE", justify="center", style="dim")))

        with Live(layout, refresh_per_second=1, screen=True):
            while True:
                layout["main"].update(self.generate_table())
                time.sleep(5)

if __name__ == "__main__":
    root = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
    dash = OmegaDashboard(root)
    dash.run()
