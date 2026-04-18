import os
import time
import json
import hashlib
import subprocess
from datetime import datetime

OMEGA_PATHS = [
    os.path.expanduser("~/Omega"),
    os.path.expanduser("~/Omega/omega-bot")
]

STATE_FILE = "omega_v38_state.json"

# ---------------------------
# UTILITIES
# ---------------------------

def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def safe_read(path):
    try:
        with open(path, "r", errors="ignore") as f:
            return f.read()[:250]
    except:
        return ""

def is_code_file(file):
    return file.endswith((".py", ".js", ".sh", ".json", ".ts"))

def count_processes():
    try:
        out = subprocess.getoutput("ps aux | wc -l")
        return int(out.strip())
    except:
        return 0

# ---------------------------
# NODE DISCOVERY ENGINE
# ---------------------------

def build_nodes():
    nodes = {}

    for base in OMEGA_PATHS:
        if not os.path.exists(base):
            continue

        for root, _, files in os.walk(base):
            for file in files:
                path = os.path.join(root, file)

                nodes[path] = {
                    "type": "code_node" if is_code_file(file) else "data_node",
                    "hash": hash_file(path),
                    "size": os.path.getsize(path) if os.path.exists(path) else 0,
                    "preview": safe_read(path),
                }

    return nodes

# ---------------------------
# SEMANTIC TRANSLATOR
# ---------------------------

def to_english(node_path, node_data):
    name = os.path.basename(node_path)

    if node_data["type"] == "code_node":
        return f"""
🧠 CODE NODE:
File: {name}

Role:
This file acts as an execution agent inside the Omega system.

Behavior:
It defines logic, computation, or system control flow.

Preview:
{node_data['preview'][:120]}
"""

    return f"""
📄 DATA NODE:
File: {name}

Role:
This file stores memory, configuration, or state.

Behavior:
It influences system knowledge but does not execute logic.

Preview:
{node_data['preview'][:120]}
"""

# ---------------------------
# STATE HANDLER
# ---------------------------

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except:
        pass

# ---------------------------
# CHANGE DETECTION
# ---------------------------

def detect_changes(old, new):
    changes = 0
    for k in new:
        if k not in old or old[k].get("hash") != new[k].get("hash"):
            changes += 1
    return changes

# ---------------------------
# ANALYSIS ENGINE
# ---------------------------

def analyze(nodes):
    report = {
        "timestamp": str(datetime.now()),
        "total_nodes": len(nodes),
        "code_nodes": 0,
        "data_nodes": 0,
        "process_count": count_processes(),
        "observations": []
    }

    for path, node in nodes.items():
        if node["type"] == "code_node":
            report["code_nodes"] += 1
        else:
            report["data_nodes"] += 1

        report["observations"].append(to_english(path, node))

    return report

# ---------------------------
# DASHBOARD LOOP
# ---------------------------

def run_dashboard():
    print("🧠 Omega v38 Observer Dashboard ONLINE\n")

    old_nodes = load_state()

    while True:
        nodes = build_nodes()
        report = analyze(nodes)

        report["changes_detected"] = detect_changes(old_nodes, nodes)

        print("\n" + "="*70)
        print("🧠 OMEGA OBSERVABILITY LAYER v38")
        print("="*70)

        print(f"Time: {report['timestamp']}")
        print(f"Total Nodes: {report['total_nodes']}")
        print(f"Code Nodes: {report['code_nodes']}")
        print(f"Data Nodes: {report['data_nodes']}")
        print(f"Running Processes (approx): {report['process_count']}")
        print(f"Changes Detected: {report['changes_detected']}")

        print("\n🧠 LIVE SYSTEM INTERPRETATION:\n")

        for obs in report["observations"][:6]:
            print(obs)
            print("-"*50)

        print("\n❓ SYSTEM QUERY:")
        print("What structural patterns are emerging across files, changes, and execution flow?\n")

        old_nodes = nodes
        save_state(nodes)

        time.sleep(5)

if __name__ == "__main__":
    run_dashboard()
