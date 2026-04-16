import json
from collections import defaultdict


class MemoryBus:
    def __init__(self):
        self.memory = defaultdict(list)

    def store(self, source, data):
        self.memory[source].append(data)

        with open("omega_memory.json", "w") as f:
            json.dump(self.memory, f, indent=2)
