class MemoryCore:
    def __init__(self):
        self.store = []

    def add(self, entry):
        self.store.append(entry)

    def compress(self):
        summary = {}

        for m in self.store:
            key = m.get("node", "unknown")
            summary[key] = summary.get(key, 0) + 1

        return summary
