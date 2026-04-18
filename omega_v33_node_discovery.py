import os

def scan_nodes(paths):
    nodes = []

    for base in paths:
        for root, _, files in os.walk(base):
            for f in files:
                if f.endswith(".py"):
                    nodes.append({
                        "name": f,
                        "path": os.path.join(root, f)
                    })

    return nodes
