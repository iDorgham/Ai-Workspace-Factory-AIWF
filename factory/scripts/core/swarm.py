#!/usr/bin/env python3
"""
AIWF Swarm Router v1.0.0
Parallel task execution across multiple workspaces.
"""

import os
import subprocess
import concurrent.futures
import sys
import json
import time
from datetime import datetime

class SwarmRouter:
    def __init__(self, factory_root):
        self.factory_root = factory_root
        self.workspaces_path = os.path.join(factory_root, "workspaces")
        self.state_file = os.path.join(factory_root, "docs/reports/factory/swarm_state.json")
        self.active_processes = {} # pid -> subprocess.Popen object
        self.locks_path = os.path.join(factory_root, ".ai/locks")
        os.makedirs(self.locks_path, exist_ok=True)

    def acquire_lock(self, agent_id, ttl=300):
        """Acquire a mutex lock for an agent with TTL."""
        lock_file = os.path.join(self.locks_path, f"{agent_id}.lock")
        if os.path.exists(lock_file):
            # Check TTL
            mtime = os.path.getmtime(lock_file)
            if time.time() - mtime < ttl:
                 print(f"🔒 [LOCK] Agent {agent_id} is busy. Waiting for lock...")
                 return False
            else:
                 print(f"🔓 [LOCK] Stale lock found for {agent_id}. Breaking.")
                 os.remove(lock_file)
        
        with open(lock_file, "w") as f:
            f.write(str(os.getpid()))
        return True

    def release_lock(self, agent_id):
        """Release a mutex lock."""
        lock_file = os.path.join(self.locks_path, f"{agent_id}.lock")
        if os.path.exists(lock_file):
            os.remove(lock_file)
            return True
        return False

    def get_workspaces(self, group=None):
        """Find workspaces, optionally filtered by group directory."""
        workspaces = []
        target_dirs = [self.workspaces_path]
        if group:
            group_dir = os.path.join(self.workspaces_path, group)
            if os.path.exists(group_dir):
                target_dirs = [group_dir]
            else:
                print(f"⚠️ Group {group} not found.")
                return []

        for p in target_dirs:
            for d in os.listdir(p):
                full_path = os.path.join(p, d)
                if os.path.isdir(full_path):
                    # Find 001_ subfolders
                    for sub in os.listdir(full_path):
                        sub_p = os.path.join(full_path, sub)
                        if os.path.isdir(sub_p) and (sub.startswith("001_") or os.path.exists(os.path.join(sub_p, ".ai"))):
                            workspaces.append(sub_p)
                    if d.startswith("smoke_") or os.path.exists(os.path.join(full_path, ".ai")):
                        workspaces.append(full_path)
        return list(set(workspaces))

    def update_state(self, command):
        """Persist active swarm state to file for TUI monitoring."""
        try:
            state = {
                "timestamp": datetime.now().isoformat(),
                "active_command": command,
                "process_count": len(self.active_processes),
                "pids": list(self.active_processes.keys())
            }
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"⚠️ [SWARM] State update error: {e}")

    def halt_all(self):
        """Emergency stop for all active swarm processes."""
        print(f"\n🚨 [PANIC] Halting {len(self.active_processes)} active processes...")
        for pid, proc in list(self.active_processes.items()):
            try:
                proc.terminate()
                print(f"🛑 Terminated PID {pid}")
            except Exception as e:
                print(f"⚠️ Could not terminate PID {pid}: {e}")
        self.active_processes.clear()

    def run_command_in_workspace(self, ws_path, command):
        """Execute a shell command inside a workspace with PID tracking."""
        name = os.path.basename(ws_path)
        print(f"📡 [SWARM] Starting '{command}' in {name}...")
        
        start_time = datetime.now()
        try:
            proc = subprocess.Popen(
                command, 
                shell=True, 
                cwd=ws_path, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.active_processes[proc.pid] = proc
            
            stdout, stderr = proc.communicate(timeout=300)
            
            # Remove from tracking after completion
            if proc.pid in self.active_processes:
                del self.active_processes[proc.pid]

            duration = (datetime.now() - start_time).total_seconds()
            status = "✅ SUCCESS" if proc.returncode == 0 else "❌ FAILED"
            
            return {
                "workspace": name,
                "status": status,
                "duration": f"{duration:.2f}s",
                "output": stdout[-500:], # Last 500 chars
                "error": stderr
            }
        except subprocess.TimeoutExpired:
            if proc.pid in self.active_processes:
                proc.kill()
                del self.active_processes[proc.pid]
            return {"workspace": name, "status": "⏰ TIMEOUT", "duration": "300s", "error": "Process timed out"}
        except Exception as e:
            return {
                "workspace": name,
                "status": "🚨 ERROR",
                "duration": "N/A",
                "error": str(e)
            }

    def execute_parallel(self, command, group=None, max_workers=5):
        """Run command across all workspaces in parallel with panic handling."""
        workspaces = self.get_workspaces(group)
        print(f"🚀 Swarming {len(workspaces)} workspaces with command: '{command}'")
        
        results = []
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Pre-register PIDs if possible, or just update after start
                future_to_ws = {executor.submit(self.run_command_in_workspace, ws, command): ws for ws in workspaces}
                self.update_state(command)
                for future in concurrent.futures.as_completed(future_to_ws):
                    results.append(future.result())
        except KeyboardInterrupt:
            self.halt_all()
            sys.exit(1)
        
        return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: swarm.py '<command>' [--group=name]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    group_name = None
    for arg in sys.argv:
        if arg.startswith("--group="):
            group_name = arg.split("=")[1]
            
    root = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
    router = SwarmRouter(root)
    results = router.execute_parallel(cmd, group=group_name)
    
    print("\n=== SWARM SUMMARY ===")
    for res in results:
        print(f"{res['status']} | {res['workspace']} ({res['duration']})")
