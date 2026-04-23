import os
import time
from datetime import datetime

class OmegaDashboardLite:
    def __init__(self, factory_root):
        self.factory_root = factory_root
        self.workspaces_path = os.path.join(factory_root, "workspaces")

    def get_workspace_data(self):
        data = []
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
                        for sub in os.listdir(full_path):
                            sub_p = os.path.join(full_path, sub)
                            if os.path.isdir(sub_p) and (sub.startswith("001_") or os.path.exists(os.path.join(sub_p, ".ai"))):
                                all_dirs.append(sub_p)
                        if d.startswith("smoke_") or os.path.exists(os.path.join(full_path, ".ai")):
                            all_dirs.append(full_path)

        all_dirs = list(set(all_dirs))

        for ws in sorted(all_dirs):
            name = os.path.basename(ws)
            ai_path = os.path.join(ws, ".ai")
            status = "ACTIVE" if os.path.exists(ai_path) else "INACTIVE"
            
            sync_log = os.path.join(ws, ".ai/logs/sync.log")
            sync_ver = "v6.0.0"
            if os.path.exists(sync_log):
                with open(sync_log, "r") as f:
                    lines = f.readlines()
                    if lines and "SYNC v7.2.0" in lines[-1]:
                        sync_ver = "v7.2.0"
            
            last_mod = datetime.fromtimestamp(os.path.getmtime(ws)).strftime("%Y-%m-%d %H:%M")
            data.append((name[:25], status, sync_ver, last_mod))
        return data

    def get_swarm_data(self):
        swarm_file = os.path.join(self.factory_root, "factory/reports/swarm_state.json")
        if os.path.exists(swarm_file):
            import json
            try:
                with open(swarm_file, "r") as f:
                    return json.load(f)
            except:
                return None
        return None

    def draw(self):
        os.system('clear')
        print("="*80)
        print("🛰️  AIWF OMEGA COMMAND CENTER (LITE) | " + datetime.now().strftime("%H:%M:%S"))
        print("="*80)
        print(f"{'Workspace':<26} | {'Status':<10} | {'Orchestration':<15} | {'Last Activity'}")
        print("-" * 80)
        
        for ws in self.get_workspace_data():
            print(f"{ws[0]:<26} | {ws[1]:<10} | {ws[2]:<15} | {ws[3]}")
            
        print("-" * 80)
        
        # Swarm Panel
        swarm = self.get_swarm_data()
        if swarm:
            print(f"🔥 ACTIVE SWARM | Cmd: {swarm['active_command']}")
            print(f"📡 Workers: {swarm['process_count']} active processes")
            print(f"⏱️  Started: {swarm['timestamp']}")
            print("-" * 80)

        print("Press Ctrl+C to exit")

    def run(self):
        try:
            while True:
                self.draw()
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nExiting Dashboard...")

if __name__ == "__main__":
    root = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
    dash = OmegaDashboardLite(root)
    dash.run()
