import os

def scan_nodes(base_path="."):

    nodes = []

    for root, dirs, files in os.walk(base_path):

        for f in files:

            if f.endswith(".py") or f.endswith(".js"):

                full_path = os.path.join(root, f)

                nodes.append({
                    "name": f,
                    "path": full_path,
                    "type": "agent_node"
                })

    return nodes
