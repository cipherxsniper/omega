import time
import random


class CivilizationEngineV6:

    def step_entities(self, frame):
        for e in frame["entities"].values():
            e["trust"] += random.uniform(-0.01, 0.01)
            e["wealth"] += random.uniform(-0.5, 0.5)

    def step_memory(self, frame):
        frame["memory"]["events"].append({
            "t": time.time(),
            "type": "cycle",
            "weight": random.random()
        })

    def step(self, frame):
        self.step_entities(frame)
        self.step_memory(frame)
        frame["timestamp"] = time.time()
        return frame
