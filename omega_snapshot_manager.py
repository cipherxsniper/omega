import json
import os
import time

REGISTRY = "omega_version_registry.json"

def load_registry():
    if os.path.exists(REGISTRY):
        with open(REGISTRY, "r") as f:
            return json.load(f)
    return {"versions": [], "latest": None}

def save_registry(data):
    with open(REGISTRY, "w") as f:
        json.dump(data, f, indent=2)

def snapshot(version, metadata):
    data = load_registry()

    data["versions"].append({
        "version": version,
        "timestamp": time.time(),
        "metadata": metadata
    })

    data["latest"] = version
    save_registry(data)
