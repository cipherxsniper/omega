# 🧠 Omega v12 Cognitive Router (Competing Thought Paths)

from omega_message_bus_v12 import bus
import random


class CognitiveRouter:

    def __init__(self):
        self.node_state = {}

    def register(self, node):
        if node not in self.node_state:
            self.node_state[node] = {
                "activation": 0.5,
                "bias": random.uniform(0.4, 0.6)
            }

    def route(self, node, signal):

        self.register(node)

        state = self.node_state[node]

        # competing influence dynamics
        score_a = signal * state["bias"]
        score_b = (1 - signal) * (1 - state["bias"])

        chosen = "PATH_A" if score_a > score_b else "PATH_B"

        # publish decision into ecosystem
        bus.publish("routing", {
            "node": node,
            "choice": chosen,
            "signal": signal
        })

        # feedback learning
        if chosen == "PATH_A":
            state["bias"] += 0.01
        else:
            state["bias"] -= 0.01

        state["bias"] = max(0.05, min(0.95, state["bias"]))

        return chosen
