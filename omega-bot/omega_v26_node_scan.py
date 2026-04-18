import os

def scan_all_nodes(base_path="~/Omega"):

    nodes = []

    for root, dirs, files in os.walk(os.path.expanduser(base_path)):

        for f in files:

            if f.endswith((".py", ".js", ".sh", ".json")):

                nodes.append({
                    "name": f,
                    "path": os.path.join(root, f),
                    "role": "agent_node"
                })

    return nodes
