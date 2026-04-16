import json
import os
import time
import threading

MEMORY_FILE = "memory/omega_memory_graph_v3.json"


class OmegaMemoryGraphV3:

    def __init__(self):
        self.graph = {}
        self.lock = threading.Lock()
        self._load()

        print("[OMEGA MEMORY V3] ONLINE")

    # -----------------------------
    # LOAD / SAVE
    # -----------------------------
    def _load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    self.graph = json.load(f)
            except:
                self.graph = {}

    def save(self):
        with self.lock:
            os.makedirs("memory", exist_ok=True)
            with open(MEMORY_FILE, "w") as f:
                json.dump(self.graph, f)

    # -----------------------------
    # STORE EVENT
    # -----------------------------
    def store(self, event):
        key = event.get("type", "unknown")

        if key not in self.graph:
            self.graph[key] = {
                "count": 0,
                "last_seen": 0,
                "patterns": []
            }

        self.graph[key]["count"] += 1
        self.graph[key]["last_seen"] = event.get("timestamp", time.time())

        # pattern detection
        if self.graph[key]["count"] % 5 == 0:
            self.graph[key]["patterns"].append("repeating_signal")

        self.save()

    # -----------------------------
    # SUMMARY (FIX YOUR ERROR)
    # -----------------------------
    def summary(self):
        return {
            "event_types": len(self.graph),
            "total_patterns": sum(len(v["patterns"]) for v in self.graph.values()),
            "total_events": sum(v["count"] for v in self.graph.values())
        }

    # -----------------------------
    # THINKING PRIMITIVE
    # -----------------------------
    def infer(self):
        insights = []

        for k, v in self.graph.items():
            if v["count"] > 10:
                insights.append(f"{k} is dominant")

            if len(v["patterns"]) > 2:
                insights.append(f"{k} shows repeating structure")

        return insights


# -----------------------------
# SINGLETON
# -----------------------------
_GLOBAL_MEMORY = None


def get_memory():
    global _GLOBAL_MEMORY
    if _GLOBAL_MEMORY is None:
        _GLOBAL_MEMORY = OmegaMemoryGraphV3()
    return _GLOBAL_MEMORY


if __name__ == "__main__":
    mem = get_memory()
    while True:
        print(mem.summary())
        time.sleep(5)

    def summary(self):
        try:
            total = len(self.memory.get("events", []))

            if total == 0:
                return {
                    "total_events": 0,
                    "last_event": None,
                    "types": {}
                }

            last_event = self.memory["events"][-1]

            types = {}
            for e in self.memory["events"]:
                t = e.get("type", "unknown")
                types[t] = types.get(t, 0) + 1

            return {
                "total_events": total,
                "last_event": last_event,
                "types": types
            }

        except Exception as e:
            print("[MEMORY SUMMARY ERROR]", e)
            return {}


    def store(self, event):
        try:
            if "events" not in self.memory:
                self.memory["events"] = []

            self.memory["events"].append(event)

            if len(self.memory["events"]) > 10000:
                self.memory["events"] = self.memory["events"][-5000:]

            self.save()

        except Exception as e:
            print("[MEMORY STORE ERROR]", e)


    def save(self):
        try:
            with open("memory/omega_memory_graph_v2.json", "w") as f:
                json.dump(self.memory, f)
        except Exception as e:
            print("[MEMORY SAVE ERROR]", e)

