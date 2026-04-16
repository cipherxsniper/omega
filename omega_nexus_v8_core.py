# omega_nexus_v8_core.py

import subprocess
import time
import threading
from omega_neural_bus_v8 import BUS

NODES = [
    "omega_self_awareness_v19.py",
    "omega_swarm_consciousness_v20.py",
    "omega_recursive_intelligence_v13.py",
    "omega_self_model_v23.py"
]

processes = []

def launch(node):
    p = subprocess.Popen(["python3", node])
    processes.append((node, p))

def observer():
    while True:
        event = BUS.get()
        print(f"""
[Ω NEXUS v8 OBSERVER]
Node: {event['node']}
Type: {event['type']}
Data: {event['data']}
""")

def health():
    while True:
        for node, p in processes:
            if p.poll() is not None:
                print(f"[Ω RESTART] {node}")
                launch(node)
        time.sleep(5)

def main():
    print("[Ω] NEXUS v8 ORGANISM ONLINE")

    for n in NODES:
        launch(n)

    threading.Thread(target=observer, daemon=True).start()
    threading.Thread(target=health, daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
