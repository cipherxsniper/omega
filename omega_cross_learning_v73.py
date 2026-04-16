class OmegaCrossLearningV73:
    def __init__(self, layer):
        self.layer = layer

    def propagate_learning(self):
        nodes = list(self.layer.memory.node_memory.keys())

        for a in nodes:
            for b in nodes:
                if a == b:
                    continue

                mem_a = self.layer.memory.get(a)
                mem_b = self.layer.memory.get(b)

                influence = mem_a["avg_health"] - mem_b["avg_health"]

                key = (a, b)

                if key not in self.layer.weights:
                    self.layer.weights[key] = 0.5

                self.layer.weights[key] += influence * 0.01

                self.layer.weights[key] = max(
                    0.1,
                    min(1.0, self.layer.weights[key])
                )
