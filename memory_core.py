import json
import os
from collections import deque

MEM_FILE = "memory.json"

class MemoryCore:
    def __init__(self, max_size=200):
        self.max_size = max_size
        self.memory = deque(maxlen=max_size)
        self.load()

    def add(self, user, message, reply):
        entry = {
            "user": user,
            "message": message,
            "reply": reply
        }
        self.memory.append(entry)
        self.save()

    def get_recent(self, n=10):
        return list(self.memory)[-n:]

    def summarize(self):
        return f"Memory depth: {len(self.memory)}"

    def save(self):
        try:
            with open(MEM_FILE, "w") as f:
                json.dump(list(self.memory), f)
        except:
            pass

    def load(self):
        if os.path.exists(MEM_FILE):
            try:
                with open(MEM_FILE, "r") as f:
                    data = json.load(f)
                    self.memory.extend(data)
            except:
                self.memory = deque(maxlen=self.max_size)

memory = MemoryCore()
