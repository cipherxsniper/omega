import os, json

os.makedirs("registry", exist_ok=True)

path = "registry/node_registry.json"

if not os.path.exists(path):
    with open(path, "w") as f:
        json.dump({
            "nodes": {},
            "total_nodes": 0
        }, f, indent=2)

print("🧠 Registry boot complete")
