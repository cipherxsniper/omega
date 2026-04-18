import numpy as np
import random
from omega.core.event_bus import emit
from omega.core.global_memory import write

class QuantumParticle:
    def __init__(self, pid):
        self.id = pid
        self.jump = 0
        self.pos = np.random.rand(2) * 100
        self.vel = (np.random.rand(2) - 0.5) * 2
        self.memory = []

        self.colors = ["purple", "green", "teal", "pink"]

    def color(self):
        return self.colors[self.jump % len(self.colors)]

    def jump_to(self, node_id, data):
        self.jump += 1
        payload = {
            "particle": self.id,
            "to": node_id,
            "jump": self.jump,
            "color": self.color(),
            "data": data
        }

        self.memory.append(payload)

        emit(payload)
        write(payload)

        return payload
