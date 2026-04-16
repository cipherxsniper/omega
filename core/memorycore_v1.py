# core/memorycore_v1.py

import json
import time
import os

class MemoryCore:
    def __init__(self, filepath="logs/memory.json"):
        self.filepath = filepath
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return []

    def save_memory(self):
        with open(self.filepath, "w") as f:
            json.dump(self.memory, f, indent=2)

    def store(self, data, tag="general"):
        entry = {
            "time": time.time(),
            "tag": tag,
            "data": data
        }
        self.memory.append(entry)
        self.save_memory()

    def retrieve(self, keyword=None):
        if not keyword:
            return self.memory[-10:]
        return [m for m in self.memory if keyword in str(m)]

    def pattern_scan(self):
        tags = {}
        for m in self.memory:
            tags[m["tag"]] = tags.get(m["tag"], 0) + 1
        return tags

    def summarize(self):
        return {
            "total_memories": len(self.memory),
            "patterns": self.pattern_scan()
        }
