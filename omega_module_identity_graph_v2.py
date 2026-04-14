import ast
from pathlib import Path

ROOT = Path.home() / "Omega"

# ============================
# NODE MODEL
# ============================

class Node:
    def __init__(self, node_id, layer, path):
        self.id = node_id
        self.layer = layer
        self.path = path

        self.runtime_health = 1.0
        self.semantic_health = 1.0
        self.trust = 1.0

        self.depends_on = []
        self.used_by = []

        self.state = "ALIVE"

    def compute_health(self):
        return (
            self.runtime_health * 0.4 +
            self.semantic_health * 0.4 +
            self.trust * 0.2
        )


# ============================
# GRAPH STRUCTURE
# ============================

class OmegaModuleGraphV2:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.reverse_edges = {}

    # ------------------------
    # ADD NODE
    # ------------------------
    def add_node(self, node: Node):
        self.nodes[node.id] = node
        self.edges[node.id] = []
        self.reverse_edges[node.id] = []

    # ------------------------
    # ADD DEPENDENCY EDGE
    # ------------------------
    def link(self, a, b):
        # a depends on b
        self.edges[a].append(b)
        self.reverse_edges[b].append(a)

        self.nodes[a].depends_on.append(b)
        self.nodes[b].used_by.append(a)

    # ------------------------
    # UPDATE HEALTH
    # ------------------------
    def update_health(self, node_id, runtime=None, semantic=None, trust=None):
        node = self.nodes[node_id]

        if runtime is not None:
            node.runtime_health = runtime
        if semantic is not None:
            node.semantic_health = semantic
        if trust is not None:
            node.trust = trust

        if node.compute_health() < 0.3:
            node.state = "FAILED"
        elif node.compute_health() < 0.6:
            node.state = "DEGRADED"
        else:
            node.state = "ALIVE"

    # ------------------------
    # PROPAGATE FAILURE
    # ------------------------
    def propagate(self):
        for node in self.nodes.values():
            if node.state == "FAILED":
                for dependent in node.used_by:
                    self.nodes[dependent].trust *= 0.8

    # ------------------------
    # SYSTEM SNAPSHOT
    # ------------------------
    def snapshot(self):
        print("\n🧠 OMEGA MODULE IDENTITY GRAPH v2\n")

        for n in self.nodes.values():
            print("──────────────────────────────")
            print(f"NODE   : {n.id}")
            print(f"LAYER  : {n.layer}")
            print(f"STATE  : {n.state}")
            print(f"HEALTH : {round(n.compute_health(), 3)}")
            print(f"DEPENDS: {n.depends_on}")
            print(f"USED BY: {n.used_by}")

    # ------------------------
    # SYSTEM HEALTH
    # ------------------------
    def system_health(self):
        total = sum(n.compute_health() for n in self.nodes.values())
        return total / len(self.nodes) if self.nodes else 0


# ============================
# BOOTSTRAP SYSTEM
# ============================

def build_default_graph():
    g = OmegaModuleGraphV2()

    g.add_node(Node("swarm_bus", "runtime", "omega_event_bus_v12.py"))
    g.add_node(Node("memory", "core", "omega_swarm_memory_bridge_v9.py"))
    g.add_node(Node("assistant", "core", "omega_unified_brain_v22.py"))
    g.add_node(Node("emitter", "runtime", "test_swarm_emitter.py"))

    g.link("swarm_bus", "memory")
    g.link("memory", "assistant")
    g.link("emitter", "swarm_bus")

    return g


# ============================
# RUN ENGINE
# ============================

if __name__ == "__main__":
    graph = build_default_graph()

    graph.snapshot()

    graph.propagate()

    print("\n📊 SYSTEM HEALTH:", round(graph.system_health(), 3))
