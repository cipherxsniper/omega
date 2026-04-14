from copy import deepcopy
from pathlib import Path

# ============================
# NODE MODEL v3
# ============================

class NodeV3:
    def __init__(self, node_id, layer):
        self.id = node_id
        self.layer = layer

        self.health = 1.0
        self.trust = 1.0

        self.history = [1.0]
        self.velocity = 0.0

        self.influence = 1.0
        self.importance = 1.0

        self.depends_on = []
        self.used_by = []

    def update(self, new_health):
        self.history.append(new_health)
        if len(self.history) > 10:
            self.history.pop(0)

        self.velocity = self.history[-1] - self.history[-2] if len(self.history) > 1 else 0
        self.health = new_health


# ============================
# COGNITIVE GRAPH v3
# ============================

class OmegaGraphCognitionV3:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

        self.predictions = {}
        self.simulations = {}

    # ------------------------
    # ADD NODE
    # ------------------------
    def add_node(self, node):
        self.nodes[node.id] = node
        self.edges[node.id] = []

    # ------------------------
    # LINK
    # ------------------------
    def link(self, a, b):
        self.edges[a].append(b)
        self.nodes[a].depends_on.append(b)
        self.nodes[b].used_by.append(a)

    # ------------------------
    # PREDICT FAILURE
    # ------------------------
    def predict_failure(self, node):
        if len(node.history) < 2:
            return 0.1

        trend = node.velocity

        risk = (1.0 - node.health)

        if trend < 0:
            risk += abs(trend) * 0.5

        if node.trust < 0.5:
            risk += 0.2

        return min(1.0, risk)

    # ------------------------
    # SIMULATE FUTURE STATE
    # ------------------------
    def simulate(self):
        simulation = {}

        for node_id, node in self.nodes.items():
            future_risk = self.predict_failure(node)

            if future_risk > 0.7:
                state = "FAILURE"
            elif future_risk > 0.4:
                state = "DEGRADED"
            else:
                state = "STABLE"

            simulation[node_id] = state

        self.simulations = simulation
        return simulation

    # ------------------------
    # REWIRE GRAPH
    # ------------------------
    def rewire(self):
        for node_id, state in self.simulations.items():
            node = self.nodes[node_id]

            if state == "FAILURE":
                # reduce influence
                node.trust *= 0.8

                # bypass node if possible
                for dependent in node.used_by:
                    for dep in node.depends_on:
                        if dep not in self.edges[dependent]:
                            self.edges[dependent].append(dep)

            elif state == "STABLE":
                node.trust *= 1.05

    # ------------------------
    # UPDATE SYSTEM
    # ------------------------
    def tick(self, health_updates):
        for node_id, health in health_updates.items():
            self.nodes[node_id].update(health)

        self.simulate()
        self.rewire()

    # ------------------------
    # SYSTEM VIEW
    # ------------------------
    def snapshot(self):
        print("\n🧠 OMEGA GRAPH COGNITION v3\n")

        for node in self.nodes.values():
            print("────────────────────────")
            print(f"NODE  : {node.id}")
            print(f"HEALTH: {round(node.health, 3)}")
            print(f"VEL   : {round(node.velocity, 3)}")
            print(f"TRUST : {round(node.trust, 3)}")
            print(f"STATE : {self.simulations.get(node.id, 'UNKNOWN')}")


# ============================
# BOOTSTRAP
# ============================

if __name__ == "__main__":
    graph = OmegaGraphCognitionV3()

    graph.add_node(NodeV3("swarm_bus", "runtime"))
    graph.add_node(NodeV3("memory", "core"))
    graph.add_node(NodeV3("assistant", "core"))
    graph.add_node(NodeV3("emitter", "runtime"))

    graph.link("swarm_bus", "memory")
    graph.link("memory", "assistant")
    graph.link("emitter", "swarm_bus")

    # simulate updates
    graph.tick({
        "swarm_bus": 0.6,
        "memory": 0.5,
        "assistant": 0.9,
        "emitter": 0.3
    })

    graph.snapshot()
