#!/usr/bin/env python3
# OMEGA v4 NEXUS BRAIN MESH

import time
import json
import threading
import queue
import os
from datetime import datetime

# ==========================
# GLOBAL NEXUS STATE
# ==========================
NEXUS_STATE = {
    "nodes": {},
    "events": [],
    "belief_field": {},
    "coherence": 0.5,
    "entropy": 0.5
}

MESSAGE_BUS = queue.Queue()

# ==========================
# EMITTER API
# ==========================
def emit(source, msg_type, data):
    MESSAGE_BUS.put({
        "time": datetime.utcnow().isoformat(),
        "source": source,
        "type": msg_type,
        "data": data
    })

# ==========================
# PROCESS MESSAGE HANDLER
# ==========================
def process_message(msg):
    source = msg["source"]

    if source not in NEXUS_STATE["nodes"]:
        NEXUS_STATE["nodes"][source] = {
            "messages": 0,
            "last_seen": None
        }

    node = NEXUS_STATE["nodes"][source]
    node["messages"] += 1
    node["last_seen"] = msg["time"]

    NEXUS_STATE["events"].append(msg)

    # cognitive interpretation
    if msg["type"] == "belief_update":
        for k, v in msg["data"].items():
            NEXUS_STATE["belief_field"][k] = v

    elif msg["type"] == "signal":
        if "coherence" in str(msg["data"]):
            NEXUS_STATE["coherence"] += 0.01
        if "entropy" in str(msg["data"]):
            NEXUS_STATE["entropy"] += 0.01

# ==========================
# OBSERVER ENGINE
# ==========================
def observer():
    while True:
        try:
            msg = MESSAGE_BUS.get(timeout=1)
            process_message(msg)

            print(f"""
[Ω NEXUS OBSERVER]
Time: {msg['time']}
Source: {msg['source']}
Type: {msg['type']}
Nodes: {len(NEXUS_STATE['nodes'])}
Coherence: {NEXUS_STATE['coherence']:.3f}
Entropy: {NEXUS_STATE['entropy']:.3f}
""")

        except:
            continue

# ==========================
# HEARTBEAT (SYSTEM LIFELINE)
# ==========================
def heartbeat():
    while True:
        emit("nexus_core", "heartbeat", {"alive": True})
        time.sleep(5)

# ==========================
# SIMULATED NODE (for integration testing)
# ==========================
def fake_node(name):
    while True:
        emit(name, "signal", {"coherence": 0.6, "entropy": 0.4})
        time.sleep(3)

# ==========================
# MAIN
# ==========================
def main():
    print("[Ω] NEXUS v4 BOOTING")

    threading.Thread(target=observer, daemon=True).start()
    threading.Thread(target=heartbeat, daemon=True).start()

    # demo nodes (replace with real omega scripts later)
    for i in range(3):
        threading.Thread(target=fake_node, args=(f"node_{i}",), daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
