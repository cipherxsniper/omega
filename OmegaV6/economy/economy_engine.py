import time
import random

class EconomyEngineV6:

    def step(self, frame):
        frame["economy"] = {
            "inflation": random.random() * 0.05
        }

        frame["memory"]["events"].append({
            "t": time.time(),
            "type": "economy_tick"
        })
        return frame
