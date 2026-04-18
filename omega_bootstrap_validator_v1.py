import os
import subprocess
import json
import time

BASE = os.path.expanduser("~/Omega")

REGISTRY_FILE = os.path.join(BASE, "omega_registry.json")

def write_registry(data):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        return {"nodes": {}}
    with open(REGISTRY_FILE, "r") as f:
        return json.load(f)

def start_node(name, cmd):
    print(f"🚀 Starting {name}")
    return subprocess.Popen(cmd, shell=True)

def bootstrap():
    print("🧠 OMEGA BOOTSTRAP v1 STARTING...")

    registry = load_registry()
    registry["nodes"] = {}

    # CORE NODES (ONLY ONCE)
    nodes = {
        "observer": "python3 ~/Omega/omega_observer.py",
        "heartbeat_py": "python3 ~/Omega/python/heartbeat.py",
        "heartbeat_js": "node ~/Omega/core/heartbeat.js",
        "event_bus": "node ~/Omega/core/observer.js"
    }

    for name, cmd in nodes.items():
        proc = start_node(name, cmd)
        registry["nodes"][name] = {
            "cmd": cmd,
            "pid": proc.pid,
            "status": "running"
        }

    write_registry(registry)

    print("🧠 BOOT COMPLETE - ALL NODES REGISTERED")

    while True:
        registry = load_registry()
        registry["timestamp"] = time.time()
        write_registry(registry)
        time.sleep(5)

if __name__ == "__main__":
    bootstrap()
