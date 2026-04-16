import os
import json

BRAIN_KEYWORDS = ["brain", "node", "omega_", "mesh", "kernel"]

def scan_system():
    files = os.listdir(".")
    brains = []

    for f in files:
        if f.endswith(".py"):
            if any(k in f for k in BRAIN_KEYWORDS):
                brains.append(f)

    return brains


def register():
    brains = scan_system()

    registry = {
        "total_nodes": len(brains),
        "nodes": []
    }

    for i, b in enumerate(brains):
        role = "brain" if "brain" in b else "node"
        registry["nodes"].append({
            "id": f"node_{i}",
            "file": b,
            "role": role,
            "status": "idle"
        })

    with open("omega_neural_registry.json", "w") as f:
        json.dump(registry, f, indent=2)

    print("[Ω REGISTRY] Nodes registered:", len(brains))


if __name__ == "__main__":
    register()
