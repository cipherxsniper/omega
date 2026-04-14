import os
import json

def ensure_graph_file():
    if not os.path.exists(GRAPH_FILE):
        with open(GRAPH_FILE, "w") as f:
            json.dump({"nodes": {}, "edges": [], "signals": []}, f)
