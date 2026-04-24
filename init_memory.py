import json
import os

path = os.path.expanduser("~/Omega/dkf_memory.json")

if not os.path.exists(path):
    with open(path, "w") as f:
        json.dump([], f)

print("🧠 Memory system initialized")
