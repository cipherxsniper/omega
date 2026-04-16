class OmegaCognitionMemoryV73:
    def __init__(self):
        self.node_memory = {}

    def record(self, node, payload, result):
        if node not in self.node_memory:
            self.node_memory[node] = {
                "runs": 0,
                "avg_health": 1.0,
                "history": []
            }

        mem = self.node_memory[node]

        mem["runs"] += 1

        health = result.get("health", 0.5)

        mem["avg_health"] = (
            (mem["avg_health"] * (mem["runs"] - 1)) + health
        ) / mem["runs"]

        mem["history"].append({
            "payload": payload,
            "result": result
        })

        # ✅ FIX: proper truncation
        mem["history"] = mem["history"][-20:]

    def get(self, node):
        return self.node_memory.get(node, {
            "runs": 0,
            "avg_health": 1.0,
            "history": []
        })
