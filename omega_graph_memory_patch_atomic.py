import os
import time
import json
import threading

LOCK = threading.Lock()

def _atomic_write(self, graph):
    with LOCK:
        tmp = GRAPH_FILE + ".tmp"

        # safe write to temp file first
        with open(tmp, "w") as f:
            json.dump(graph, f)

        # retry-safe atomic swap
        for _ in range(3):
            try:
                os.replace(tmp, GRAPH_FILE)
                break
            except FileNotFoundError:
                time.sleep(0.05)
