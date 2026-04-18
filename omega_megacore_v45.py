import os
import json
import time
import subprocess
import psutil
from collections import defaultdict

ROOT = os.path.expanduser("~/Omega")
STATE_FILE = "omega_system_state.json"

# ---------------------------
# SYSTEM STATE
# ---------------------------

state = {
    "nodes": {},
    "failures": {},
    "messages": [],
    "metrics": {
        "chaos": 0.0,
        "coherence": 0.0,
        "flow": 0.0
    }
}

# ---------------------------
# v42 NODE DISCOVERY
# ---------------------------

def discover_nodes():
    nodes = []
    for r, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".py"):
                nodes.append(os.path.join(r, f))
    return nodes

def register_nodes():
    for n in discover_nodes():
        state["nodes"][n] = {
            "status": "active",
            "last_seen": time.time()
        }

# ---------------------------
# v43 DISTRIBUTED MEMORY (FILE BASED)
# ---------------------------

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def log(msg):
    state["messages"].append({
        "msg": msg,
        "time": time.time()
    })

# ---------------------------
# v44 OBSERVER VIEW
# ---------------------------

def compute_metrics():
    total = len(state["nodes"])
    alive = sum(1 for n in state["nodes"].values() if n["status"] == "active")

    coherence = alive / total if total else 0

    chaos = len(state["failures"]) / (total + 1)

    throughput = len(state["messages"]) % 50 / 50

    flow = (coherence * throughput) / (chaos + 1)

    state["metrics"] = {
        "chaos": round(chaos, 3),
        "coherence": round(coherence, 3),
        "flow": round(flow, 3)
    }

def render_dashboard():
    os.system("clear")
    print("🧠 OMEGA UNIFIED MEGACORE v45\n")

    m = state["metrics"]

    print(f"Nodes: {len(state['nodes'])}")
    print(f"Chaos Score: {m['chaos']}")
    print(f"Coherence: {m['coherence']}")
    print(f"Flow State: {m['flow']}\n")

    print("📡 Recent Messages:")
    for msg in state["messages"][-5:]:
        print(f"- {msg['msg']}")

# ---------------------------
# v45 SUPERVISOR (SAFE)
# ---------------------------

def is_running(file):
    for p in psutil.process_iter():
        try:
            if file in " ".join(p.cmdline()):
                return True
        except:
            pass
    return False

def restart(file):
    print(f"[SUPERVISOR] Restarting {file}")
    subprocess.Popen(["python", file])

def supervise():
    for n in list(state["nodes"].keys())[:10]:
        if not is_running(n):
            state["nodes"][n]["status"] = "restarting"
            restart(n)

# ---------------------------
# MESSAGE PARSER (wink wink safe handling)
# ---------------------------

def parse_message(msg):
    if "wink wink thought" in msg:
        return "UNSTRUCTURED_PACKET"

    return "STANDARD_PACKET"

# ---------------------------
# MAIN LOOP
# ---------------------------

def run():
    register_nodes()

    while True:
        compute_metrics()
        supervise()
        save_state()
        render_dashboard()

        log("system_tick")

        time.sleep(3)

if __name__ == "__main__":
    run()
