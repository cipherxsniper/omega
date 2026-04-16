import subprocess
import time
import json
import os
import socket
import uuid
import hashlib

STATE_FILE = "runtime_v7/supervisor/control_plane_state.json"


# -----------------------------
# NODE DEFINITIONS (DAG CORE)
# -----------------------------
NODES = {
    "bus": "python runtime_v7/core/v9_9_swarm_bus_v2.py",
    "v10": "python runtime_v7/core/v10_cognitive_event_memory_graph.py",
    "v11": "python runtime_v7/core/v11_swarm_reasoning_engine.py",
    "v12": "python runtime_v7/core/v12_swarm_cognition_layer.py",
}


# -----------------------------
# CRYPTO IDENTITY (V4)
# -----------------------------
def sign(node_id, payload: dict):
    raw = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(node_id.encode() + raw).hexdigest()


# -----------------------------
# STATE PERSISTENCE
# -----------------------------
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"nodes": {}}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# -----------------------------
# PROCESS START
# -----------------------------
def start_node(name, cmd, state):
    print(f"[CONTROL PLANE] starting {name}")

    log_path = f"logs/{name}.log"
    os.makedirs("logs", exist_ok=True)
    log_file = open(log_path, "a")

    proc = subprocess.Popen(
        cmd.split(),
        stdout=log_file,
        stderr=log_file
    )

    state["nodes"][name] = {
        "pid": proc.pid,
        "restarts": state["nodes"].get(name, {}).get("restarts", 0),
        "health": 1.0,
        "last_seen": time.time()
    }

    return proc


# -----------------------------
# V5 MESH UPDATE
# -----------------------------
def broadcast_state(state):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    payload = {
        "type": "swarm_state",
        "state": state,
        "node_id": str(uuid.uuid4())[:8]
    }

    payload["sig"] = sign(payload["node_id"], payload)

    sock.sendto(
        json.dumps(payload).encode(),
        ("127.0.0.1", 6017)
    )


# -----------------------------
# V6 DAG OPTIMIZER
# -----------------------------
def optimize_dag(state):
    nodes = state["nodes"]

    for name, info in nodes.items():
        # decay health if unstable
        if info["restarts"] > 3:
            info["health"] *= 0.9
        else:
            info["health"] = min(1.0, info["health"] + 0.01)

    # reorder priority (healthy nodes first)
    ordered = sorted(nodes.items(), key=lambda x: x[1]["health"], reverse=True)

    state["execution_order"] = [n[0] for n in ordered]


# -----------------------------
# MONITOR LOOP
# -----------------------------
def monitor(processes, state):
    while True:

        for name, proc in list(processes.items()):

            if proc.poll() is not None:
                code = proc.returncode

                print("\n[CRASH DETECTED]", name, "code:", code)

                state["nodes"][name]["restarts"] += 1
                state["nodes"][name]["last_exit"] = code

                time.sleep(2)

                # restart logic
                processes[name] = start_node(name, NODES[name], state)

        optimize_dag(state)
        broadcast_state(state)
        save_state(state)

        print("[CONTROL PLANE] DAG:", state.get("execution_order", []))

        time.sleep(5)


# -----------------------------
# BOOT
# -----------------------------
def main():
    print("[CONTROL PLANE V6] INITIALIZING UNIFIED SWARM")

    state = load_state()
    processes = {}

    for name, cmd in NODES.items():
        processes[name] = start_node(name, cmd, state)

    monitor(processes, state)


if __name__ == "__main__":
    main()
