# 🧠 Omega v11.6 Dynamic Propagation Field Engine (FIXED)

import math
import time
import random
from collections import defaultdict, deque

class FieldEngine:

    def __init__(self):

        self.nodes = {
            "node_attention": (0, 0),
            "node_goal": (2, 1),
            "node_memory": (1, 3),
            "node_stability": (3, 3)
        }

        self.energy_field = defaultdict(float)
        self.event_trace = deque(maxlen=500)

        # drift introduces long-term evolution
        self.drift = defaultdict(lambda: random.uniform(0.95, 1.05))

    def distance(self, a, b):
        ax, ay = self.nodes[a]
        bx, by = self.nodes[b]
        return math.sqrt((ax - bx)**2 + (ay - by)**2)

    def emit(self, source, intensity=1.0):

        self.event_trace.append((source, intensity, time.time()))

        for node in self.nodes:

            dist = self.distance(source, node)
            decay = math.exp(-dist)

            noise = random.uniform(-0.05, 0.05)

            # 🔥 dynamic drift makes system non-static
            modifier = self.drift[node]

            energy = max(0.0, (intensity * decay * modifier) + noise)

            self.energy_field[node] += energy

    def get_heatmap(self):

        total = sum(self.energy_field.values()) + 1e-6

        return {
            node: round(val / total, 3)
            for node, val in self.energy_field.items()
        }

    def decay(self):
        for node in self.energy_field:
            self.energy_field[node] *= 0.91

    def apply_flow(self, flow_updates):
        for node, delta in flow_updates.items():
            self.state[node] = self.state.get(node, 0.0) + delta

    def decay(self):
        for k in self.state:
            self.state[k] *= 0.97

    def equilibrium_pressure(self):
        avg = sum(self.state.values()) / max(len(self.state), 1)

        for k in self.state:
            self.state[k] += (avg - self.state[k]) * 0.05
