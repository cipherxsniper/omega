import time
import random

class CivilizationEngineV6:

    def step_entities(self, frame):
        for e in frame.get("entities", {}).values():
            e["trust"] = e.get("trust", 0) + random.uniform(-0.01, 0.01)
            e["wealth"] = e.get("wealth", 0) + random.uniform(-0.5, 0.5)
        return frame

    def step_memory(self, frame):
        frame["memory"]["events"].append({
            "t": time.time(),
            "type": "civilization_tick"
        })
        return frame

    def step(self, frame):
        frame = self.step_entities(frame)
        frame = self.step_memory(frame)
        frame["timestamp"] = time.time()
        return frame
