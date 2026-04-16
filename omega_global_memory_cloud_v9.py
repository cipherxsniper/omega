import time

class OmegaGlobalMemoryCloud:
    def __init__(self):
        self.memory = []

    def store(self, data):
        self.memory.append({"data": data, "ts": time.time()})

    def retrieve(self, limit=10):
        return self.memory[-limit:]
