import json
import os
import time

MEM = os.path.expanduser("~/Omega/omega_memory_v13.json")

def load():
    return json.load(open(MEM))

while True:
    db = load()

    print("\n🧠 OMEGA v13 NEURAL OBSERVER")
    print("============================")

    print(f"Iteration: {db['global_state']['iteration']}")
    print(f"Dominant Brain: {db['global_state']['dominant_node']}")

    print("\nNodes:")
    for n, d in db["nodes"].items():
        print(
            f"- {n}: score={round(d['score'],2)} "
            f"stability={round(d['stability'],2)} "
            f"events={d['events']}"
        )

    print("============================\n")
    time.sleep(5)
