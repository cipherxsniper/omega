import subprocess
import threading
import time
import json
import os
import queue
import re
from datetime import datetime

# ==========================
# CONFIG
# ==========================

NODES = [
    "omega_self_awareness_v19.py",
    "omega_self_model_v23.py",
    "omega_swarm_network_v19.py",
    "omega_swarm_consciousness_v20.py",
]

MAX_RESTARTS = 3

# ==========================
# EVENT BUS (CRITICAL FIX)
# ==========================

event_bus = queue.Queue()

# ==========================
# PROCESS REGISTRY
# ==========================

processes = {}
restart_count = {}

# ==========================
# SAFE JSON MEMORY
# ==========================

MEMORY_FILE = "nexus_memory_v6.json"

def safe_write_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"events": [], "nodes": {}}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

memory = load_memory()

# ==========================
# BINARY DECODER
# ==========================

def decode_binary(line):
    try:
        if re.fullmatch(r"[01\s]+", line.strip()):
            bits = line.split()
            if all(len(b) == 8 for b in bits):
                return ''.join(chr(int(b, 2)) for b in bits)
    except:
        pass
    return None

# ==========================
# NODE LAUNCHER
# ==========================

def launch_node(script):
    proc = subprocess.Popen(
        ["python3", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    processes[script] = proc
    restart_count[script] = restart_count.get(script, 0)

    threading.Thread(
        target=stream_node_output,
        args=(script, proc),
        daemon=True
    ).start()

# ==========================
# STREAM NODE OUTPUT → EVENT BUS
# ==========================

def stream_node_output(script, proc):
    for line in proc.stdout:
        event_bus.put({
            "time": datetime.utcnow().isoformat(),
            "source": script,
            "raw": line.strip()
        })

# ==========================
# OBSERVER BRAIN (READ ONLY)
# ==========================

def observer():
    state = {
        "nodes_active": set(),
        "events": 0
    }

    while True:
        try:
            event = event_bus.get(timeout=1)

            decoded = decode_binary(event["raw"])
            signal = decoded if decoded else event["raw"]

            if "node_" in signal:
                state["nodes_active"].add(signal)

            state["events"] += 1

            memory["events"].append({
                "time": event["time"],
                "source": event["source"],
                "signal": signal
            })

            print(f"""
[Ω NEXUS v6 OBSERVER]
Time: {event["time"]}
Source: {event["source"]}
Nodes Active: {len(state["nodes_active"])}
Event Count: {state["events"]}
Signal: {signal}
""")

        except queue.Empty:
            continue

# ==========================
# HEALTH MONITOR
# ==========================

def health_monitor():
    while True:
        for script, proc in list(processes.items()):
            if proc.poll() is not None:

                restart_count[script] += 1

                if restart_count[script] > MAX_RESTARTS:
                    print(f"[Ω] NODE FAILED PERMANENTLY: {script}")
                    continue

                print(f"[RESTART] {script}")
                launch_node(script)

        safe_write_json(MEMORY_FILE, memory)
        time.sleep(5)

# ==========================
# MAIN ORCHESTRATOR
# ==========================

def main():
    print("[Ω] NEXUS v6 INITIALIZING")

    for node in NODES:
        if os.path.exists(node):
            launch_node(node)
            time.sleep(0.5)

    threading.Thread(target=observer, daemon=True).start()
    threading.Thread(target=health_monitor, daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
