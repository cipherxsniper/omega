# 🔁 Omega v17 Evolution Engine

import random

class EvolutionEngine:

    def evolve_node(self, node):

        # mutation pressure
        mutation = random.uniform(-0.02, 0.02)

        node["energy"] += mutation

        # selection pressure
        if node["energy"] < 0.2:
            node["stability"] *= 0.95

        if node["energy"] > 0.8:
            node["trust"] *= 1.02

        node["energy"] = max(0.01, min(1.0, node["energy"]))
        node["trust"] = max(0.01, min(1.0, node["trust"]))
