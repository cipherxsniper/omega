# 🌐 Omega v17 Communication Mesh

import random

class CommunicationMesh:

    def __init__(self, state):
        self.state = state.state

    def send_signal(self, a, b, strength=0.5):

        node_a = self.state["nodes"][a]
        node_b = self.state["nodes"][b]

        if "connections" not in node_a:
            node_a["connections"] = {}

        if b not in node_a["connections"]:
            node_a["connections"][b] = {
                "weight": strength,
                "trust": 0.5,
                "volatility": 0.2
            }

        conn = node_a["connections"][b]

        noise = random.uniform(-0.05, 0.05)

        conn["weight"] = max(0.01, min(1.0,
            conn["weight"] + noise + (node_a["energy"] * 0.01)
        ))

        return conn["weight"]
