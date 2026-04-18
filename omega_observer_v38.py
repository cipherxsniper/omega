import time
import os
import json
from collections import deque

class ObserverView:

    def __init__(self):
        self.stream = deque(maxlen=20)

    def ingest(self, node, data):
        self.stream.append({
            "node": node,
            "data": data,
            "time": time.time()
        })

    def translate(self, data):
        """
        Converts unreadable / raw signals into structured English.
        """
        if isinstance(data, str):
            return f"🧠 Signal: {data}"
        elif isinstance(data, dict):
            return " | ".join([f"{k}:{v}" for k, v in data.items()])
        else:
            return str(data)

    def render(self):
        os.system("clear")
        print("🧠 OMEGA OBSERVER VIEW (LIVE NODE MESH)\n")

        for item in list(self.stream):
            readable = self.translate(item["data"])
            print(f"[{item['node']}] → {readable}")
