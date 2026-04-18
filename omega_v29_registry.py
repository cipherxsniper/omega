import os

def scan_nodes(base_path="."):
    nodes = []

    for root, _, files in os.walk(base_path):
        for f in files:
            if f.endswith(".py"):
                nodes.append(os.path.join(root, f))

    return nodes

def register(nodes):
    registry = {}

    for n in nodes:
        name = n.split("/")[-1].replace(".py","")
        registry[name] = {
            "path": n,
            "active": True
        }

    return registry
