#!/usr/bin/env python3

import time
import queue
import threading
import os
from datetime import datetime, timezone

from omega_node_adapter_v5 import start_node

# ==========================
# NEXUS STATE
# ==========================
NEXUS = {
    "nodes": {},
    "events": [],
    "coherence": 0.5,
    "entropy": 0.5
}

BUS = queue.Queue()

SWARM_SCRIPTS = [
    "omega_self_awareness_v19.py",
    "omega_self_model_v23.py",
    "omega_self_reflective_kernel_v6_3.py",
    "omega_recursive_intelligence_v13.py",
    "omega_swarm_network_v19.py",
    "omega_swarm_node_v8.py",
    "omega_swarm_consciousness_v20.py",
]

# ==========================
# PROCESSOR
# ==========================
def process(msg):
    source = msg["source"]

    if source not in NEXUS["nodes"]:
        NEXUS["nodes"][source] = 0

    NEXUS["nodes"][source] += 1
    NEXUS["events"].append(msg)

    data = msg["data"]

    if "coherence" in data:
        NEXUS["coherence"] += 0.01

    if "entropy" in data:
        NEXUS["entropy"] += 0.01

# ==========================
# OBSERVER
# ==========================
def observer():
    while True:
        try:
            msg = BUS.get(timeout=1)
            process(msg)

            print(f"""
[Ω NEXUS v5]
Time: {datetime.now(timezone.utc).isoformat()}
Source: {msg['source']}
Nodes: {len(NEXUS['nodes'])}
Coherence: {NEXUS['coherence']:.3f}
Entropy: {NEXUS['entropy']:.3f}
Last: {msg['data'][:120]}
""")

        except queue.Empty:
            continue

# ==========================
# HEARTBEAT
# ==========================
def heartbeat():
    while True:
        BUS.put({
            "time": datetime.now(timezone.utc).isoformat(),
            "source": "nexus_core",
            "type": "heartbeat",
            "data": "alive"
        })
        time.sleep(5)

# ==========================
# MAIN
# ==========================
def main():
    print("[Ω] NEXUS v5 SWARM INITIALIZING")

    threading.Thread(target=observer, daemon=True).start()
    threading.Thread(target=heartbeat, daemon=True).start()

    # START REAL SWARM NODES
    for script in SWARM_SCRIPTS:
        if os.path.exists(script):
            start_node(script, BUS)
            print(f"[Ω] NODE ATTACHED: {script}")
        else:
            print(f"[!] MISSING NODE: {script}")

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
