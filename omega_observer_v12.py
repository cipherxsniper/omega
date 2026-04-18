import json
import os
import time

MEM = os.path.expanduser("~/Omega/omega_memory_v12.json")

def load():
    return json.load(open(MEM))

def translate():
    db = load()

    print("\n🧠 OMEGA v12 OBSERVER")
    print("====================")

    nodes = db.get("node_memory", {})
    events = db.get("events", [])

    print(f"Active Nodes: {len(nodes)}")
    print(f"Event Stream: {len(events)} entries")

    for n, d in nodes.items():
        print(
            f"- Node {n}: score={round(d['score'],2)} "
            f"stability={d['stability']}"
        )

    print("====================\n")

while True:
    translate()
    time.sleep(5)
