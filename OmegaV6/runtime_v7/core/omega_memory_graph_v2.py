import json
import os
import time
import threading

BASE = os.path.expanduser("~/Omega/OmegaV6")
MEM_PATH = os.path.join(BASE, "memory/omega_memory_graph_v2.json")

class OmegaMemoryGraphV2:
    def __init__(self):
        os.makedirs(os.path.dirname(MEM_PATH), exist_ok=True)
        self.lock = threading.Lock()
        self.graph = self.load()
        print("[OMEGA MEMORY V2] ONLINE")

    def load(self):
        if os.path.exists(MEM_PATH):
            try:
                with open(MEM_PATH, "r") as f:
                    return json.load(f)
            except:
                return self.empty_graph()
        return self.empty_graph()

    def empty_graph(self):
        return {"nodes": {}, "edges": {}, "events": [], "last_update": time.time()}

    def save(self):
        with self.lock:
            self.graph["last_update"] = time.time()
            with open(MEM_PATH, "w") as f:
                json.dump(self.graph, f, indent=2)

    def ingest(self, event):
        with self.lock:
            node = event.get("node_id", "unknown")
            etype = event.get("type", "unknown")

            self.graph["events"].append({
                "node": node,
                "type": etype,
                "time": time.time()
            })

            if node not in self.graph["nodes"]:
                self.graph["nodes"][node] = {"activity": 0, "last_seen": time.time()}

            self.graph["nodes"][node]["activity"] += 1
            self.graph["nodes"][node]["last_seen"] = time.time()

            key = f"{node}:{etype}"
            self.graph["edges"][key] = self.graph["edges"].get(key, 0) + 1

    def run(self):
        while True:
            self.save()
            time.sleep(5)

_MEMORY = None

def get_memory():
    global _MEMORY
    if _MEMORY is None:
        _MEMORY = OmegaMemoryGraphV2()
    return _MEMORY

if __name__ == "__main__":
    get_memory().run()

    def summary(self):
        return {
            "total_events": len(self.graph["events"]),
            "total_nodes": len(self.graph["nodes"]),
            "total_edges": len(self.graph["edges"])
        }
