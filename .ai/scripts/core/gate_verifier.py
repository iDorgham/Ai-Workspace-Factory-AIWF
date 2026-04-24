import os
import json
import sys

STATE_FILE = '.ai/memory/state.json'

def init_state():
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'w') as f:
            json.dump({"workflow_stage": "none"}, f)

def read_state():
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def write_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def cmd_review():
    state = read_state()
    state["workflow_stage"] = "reviewed"
    write_state(state)
    print("Gate: /review passed.")

def cmd_approve():
    state = read_state()
    if state.get("workflow_stage") != "reviewed":
        print("ERROR: Cannot /approve before /review. Hard Block.")
        sys.exit(1)
    state["workflow_stage"] = "approved"
    write_state(state)
    print("Gate: /approve passed.")

def cmd_export():
    state = read_state()
    if state.get("workflow_stage") != "approved":
        print("ERROR: Cannot /export before /approve. Hard Block.")
        sys.exit(1)
    state["workflow_stage"] = "exported"
    write_state(state)
    print("Gate: /export passed. Data safely exported.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
         print("Usage: python gate_verifier.py [init|review|approve|export]")
         sys.exit(1)
         
    action = sys.argv[1]
    if action == "init": init_state()
    elif action == "review": cmd_review()
    elif action == "approve": cmd_approve()
    elif action == "export": cmd_export()
    else: print("Unknown action")
