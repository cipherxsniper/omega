import os
import json

GRAPH_FILE = "omega_v30_code_graph.json"

def scan_project(root="."):
    graph = {}

    for path, _, files in os.walk(root):
        for f in files:
            if f.endswith(".py"):
                full = os.path.join(path, f)

                graph[f] = {
                    "path": full,
                    "imports": [],
                    "status": "active"
                }

    return graph

def save_graph(graph):
    json.dump(graph, open(GRAPH_FILE, "w"), indent=2)

def load_graph():
    try:
        return json.load(open(GRAPH_FILE))
    except:
        return {}
