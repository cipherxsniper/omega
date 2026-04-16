import subprocess
import time
import json
import os
import socket
import uuid
import hashlib
from threading import Thread

# -----------------------------
# FILE PATHS
# -----------------------------
STATE_FILE = "runtime_v7/supervisor/control_plane_state_v9.json"
MEMORY_FILE = "runtime_v7/supervisor/cognitive_memory_graph.json"
TRUST_FILE  = "runtime_v7/supervisor/trust_db.json"

os.makedirs("runtime_v7/supervisor", exist_ok=True)
os.makedirs("logs", exist_ok=True)


# -----------------------------
# NODE STACK
# -----------------------------
NODES = {
    "bus": "python runtime_v7/core/v9_9_swarm_bus_v2.py",
    "v10": "python runtime_v7/core/v10_cognitive_event_memory_graph.py",
    "v11": "python runtime_v7/core/v11_swarm_reasoning_engine.py",
    "v12": "python runtime_v7/core/v12_swarm_cognition_layer.py",
}


# =========================================================
# 🧠 V7 — COGNITIVE MEMORY GRAPH CORE
# =========================================================

def load_memory():
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE))
    return {"events": [], "edges": []}


def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w"), indent=2)


def write_memory(event):
    mem = load_memory()
    mem["events"].append(event)

    # simple causal linking
    if len(mem["events"]) > 1:
        mem["edges"].append({
            "from": mem["events"][-2]["id"],
            "to": event["id"]
        })

    save_memory(mem)


# =========================================================
# 🔐 V9 — ZERO TRUST FABRIC
# =========================================================

def load_trust():
    if os.path.exists(TRUST_FILE):
        return json.load(open(TRUST_FILE))
    return {}


def save_trust(db):
    json.dump(db, open(TRUST_FILE, "w"), indent=2)


def sign(node_id, payload):
    raw = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(node_id.encode() + raw).hexdigest()


def verify(node_id, payload, signature):
    expected = sign(node_id, payload)
    return expected == signature


def trust_score(node_id):
    db = load_trust()
    return db.get(node_id, 0.5)


def update_trust(node_id, delta):
    db = load_trust()
    db[node_id] = max(0.0, min(1.0, db.get(node_id, 0.5) + delta))
    save_trust(db)


# =========================================================
# 🌐 V8 — FEDERATION LAYER
# =========================================================

PEERS = set()

def discover_peers():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 6017))

    while True:
        data, addr = sock.recvfrom(65535)

        try:
            msg = json.loads(data.decode())
            node_id = msg.get("node_id")

            if not node_id:
                continue

            PEERS.add(addr[0])

            print(f"[V8] peer discovered: {node_id} @ {addr[0]}")

            # V9 trust gate
            if not verify(node_id, msg, msg.get("sig", "")):
                print("[V9] REJECTED (bad signature)")
                update_trust(node_id, -0.2)
                continue

            update_trust(node_id, +0.01)

            # V7 MEMORY WRITE
            write_memory({
                "id": str(uuid.uuid4()),
                "node": node_id,
                "type": msg.get("type"),
                "ts": time.time()
            })

        except Exception as e:
            print("[FEDERATION ERROR]", e)


# =========================================================
# CONTROL PLANE
# =========================================================

def start_node(name, cmd):
    print(f"[BOOT] {name}")

    log_file = open(f"logs/{name}.log", "a")

    proc = subprocess.Popen(
        cmd.split(),
        stdout=log_file,
        stderr=log_file
    )

    return proc


def monitor(processes):
    while True:

        for name, proc in list(processes.items()):

            if proc.poll() is not None:
                print(f"[CRASH] {name} -> restarting")

                processes[name] = start_node(name, NODES[name])

        print(f"[STATUS] peers={len(PEERS)} memory_events={len(load_memory()['events'])}")

        time.sleep(5)


# =========================================================
# BOOTSTRAP
# =========================================================

def main():

    print("🧠 V9 SWARM CONTROL PLANE ONLINE")

    processes = {}

    for name, cmd in NODES.items():
        processes[name] = start_node(name, cmd)

    Thread(target=discover_peers, daemon=True).start()
    monitor(processes)


if __name__ == "__main__":
    main()
