class OmegaMemoryDecayV717:

    def __init__(self, decay_rate=0.90, threshold=0.2):
        self.memory = {}
        self.decay_rate = decay_rate
        self.threshold = threshold

    def write(self, key, value):
        self.memory[key] = {
            "value": value,
            "strength": 1.0
        }

    def decay(self):
        to_delete = []

        for k, v in self.memory.items():
            v["strength"] *= self.decay_rate

            if v["strength"] < self.threshold:
                to_delete.append(k)

        for k in to_delete:
            del self.memory[k]

    def read(self, key):
        item = self.memory.get(key)
        if not item:
            return None

        # weaker memory returns partial confidence
        return item["value"], item["strength"]

    def snapshot(self):
        return self.memory
