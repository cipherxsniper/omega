#!/usr/bin/env python3
# OMEGA NEXUS v7 - NEURAL MESH CORE

import os
import subprocess
import time
import json
import threading
import queue
import uuid
from datetime import datetime

# ==========================
# EVENT BUS
# ==========================

EVENT_BUS = queue.Queue()

SYSTEM_STATE = {
    "nodes": {},
    "edges": [],
    "events": [],
    "generation": 0,
    "coherence": 0.5,
}

# ==========================
# NODE REGISTRY
# ==========================

NODE_FILES = [
    "omega_swarm_node_v8.py",
    "omega_self_model_v23.py",
    "omega_self_awareness_v19.py",
    "omega_recursive_intelligence_v13.py",
    "omega_swarm_consciousness_v20.py"
]

processes = {}

# ==========================
# EVENT FORMAT STANDARD
# ==========================

def emit(node, event_type, data):
    EVENT_BUS.put({
        "id": str(uuid.uuid4()),
        "time": datetime.utcnow().isoformat(),
        "node": node,
        "type": event_type,
        "data": data
    })

# ==========================
# NODE LAUNCHER
# ==========================

def launch_node(script):
    proc = subprocess.Popen(
        ["python3", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    processes[script] = proc

    threading.Thread(target=stream_node, args=(script, proc), daemon=True).start()

def stream_node(script, proc):
    for line in proc.stdout:
        EVENT_BUS.put({
            "id": str(uuid.uuid4()),
            "time": datetime.utcnow().isoformat(),
            "node": script,
            "type": "raw",
            "data": line.strip()
        })

# ==========================
# BINARY DECODER (REAL FIX)
# ==========================

def decode_binary(text):
    try:
        bits = text.strip().split()
        if all(b in ("0", "1", "01", "10") or set(b) <= {"0","1"} for b in bits):
            chars = []
            for b in bits:
                if len(b) >= 8:
                    chars.append(chr(int(b, 2)))
            return "".join(chars)
    except:
        pass
    return None

# ==========================
# OBSERVER ENGINE
# ==========================

def observer():
    while True:
        event = EVENT_BUS.get()

        SYSTEM_STATE["events"].append(event)

        node = event["node"]
        data = event["data"]

        # register node
        SYSTEM_STATE["nodes"].setdefault(node, 0)
        SYSTEM_STATE["nodes"][node] += 1

        # decode binary if possible
        decoded = decode_binary(data)
        if decoded:
            event["decoded"] = decoded

        # compute coherence (simple but stable)
        SYSTEM_STATE["coherence"] = min(
            1.0,
            0.5 + (len(SYSTEM_STATE["nodes"]) * 0.01)
        )

        print(render_observation(event))


# ==========================
# OBSERVATION OUTPUT
# ==========================

def render_observation(event):
    return f"""
[Ω NEXUS v7 OBSERVER]
Time: {event['time']}
Node: {event['node']}
Type: {event['type']}

DATA:
{event['data']}

{"DECODED: " + event['decoded'] if 'decoded' in event else ""}

SYSTEM:
Nodes Active: {len(SYSTEM_STATE['nodes'])}
Coherence: {SYSTEM_STATE['coherence']:.3f}
Generation: {SYSTEM_STATE['generation']}
"""

# ==========================
# GROWTH ENGINE (CONTROLLED)
# ==========================

def growth_engine():
    while True:
        time.sleep(10)

        if len(SYSTEM_STATE["nodes"]) < 10:
            new_node = f"omega_autogen_node_{SYSTEM_STATE['generation']}.py"

            print(f"[Ω GROWTH] spawning {new_node}")

            SYSTEM_STATE["generation"] += 1

# ==========================
# HEALTH MONITOR
# ==========================

def health():
    while True:
        for script, proc in list(processes.items()):
            if proc.poll() is not None:
                print(f"[Ω RESTART] {script}")
                launch_node(script)
        time.sleep(5)

# ==========================
# MAIN
# ==========================

def main():
    print("[Ω] NEXUS v7 BOOTING")

    for n in NODE_FILES:
        if os.path.exists(n):
            launch_node(n)
            time.sleep(0.5)

    threading.Thread(target=observer, daemon=True).start()
    threading.Thread(target=health, daemon=True).start()
    threading.Thread(target=growth_engine, daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
