import json
import os

path = os.path.expanduser("~/Omega/dkf_swarm_memory.json")

if not os.path.exists(path):
    with open(path, "w") as f:
        json.dump([], f)

print("🧠 Swarm memory initialized")
