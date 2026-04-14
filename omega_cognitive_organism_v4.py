import random

# ============================
# NODE v4
# ============================

class NodeV4:
    def __init__(self, node_id, layer):
        self.id = node_id
        self.layer = layer

        self.health = 1.0
        self.energy = 1.0
        self.stability = 1.0

        self.age = 0
        self.mutation_score = 0.0

        self.parents = []
        self.children = []

    def tick(self):
        self.age += 1

        # natural decay
        self.energy *= 0.98

        # instability reduces health
        if self.stability < 0.4:
            self.health -= 0.05

        # recovery
        if self.stability > 0.7:
            self.health += 0.02

        self.health = max(0.0, min(1.0, self.health))


# ============================
# ORGANISM v4
# ============================

class OmegaCognitiveOrganismV4:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

        self.energy_field = 1.0
        self.stress_map = {}
        self.growth_pressure = 0.0

    # ------------------------
    # ADD NODE
    # ------------------------
    def add_node(self, node):
        self.nodes[node.id] = node
        self.edges[node.id] = []

    # ------------------------
    # LINK NODES
    # ------------------------
    def link(self, a, b):
        self.edges[a].append(b)
        self.nodes[a].children.append(b)
        self.nodes[b].parents.append(a)

    # ------------------------
    # STRESS CALCULATION
    # ------------------------
    def compute_stress(self):
        stress = {}

        for n in self.nodes.values():
            load = len(n.children)
            instability = 1.0 - n.stability
            health_pressure = 1.0 - n.health

            stress[n.id] = load * 0.4 + instability * 0.4 + health_pressure * 0.2

        self.stress_map = stress
        return stress

    # ------------------------
    # ENERGY FLOW
    # ------------------------
    def redistribute_energy(self):
        avg = sum(n.energy for n in self.nodes.values()) / len(self.nodes)

        for n in self.nodes.values():
            if n.energy < avg:
                n.energy += 0.05
            else:
                n.energy -= 0.03

    # ------------------------
    # MUTATION ENGINE
    # ------------------------
    def mutate(self):
        for node in list(self.nodes.values()):
            stress = self.stress_map.get(node.id, 0)

            # NODE SPAWN (high stress)
            if stress > 0.8:
                new_id = f"{node.id}_mut_{random.randint(1,999)}"
                new_node = NodeV4(new_id, node.layer)

                self.add_node(new_node)
                self.link(node.id, new_id)

            # NODE MERGE (low utility)
            if stress < 0.2 and node.age > 5:
                node.stability += 0.1

    # ------------------------
    # SYSTEM TICK
    # ------------------------
    def tick(self):
        for n in self.nodes.values():
            n.tick()

        self.compute_stress()
        self.redistribute_energy()
        self.mutate()

    # ------------------------
    # VIEW
    # ------------------------
    def snapshot(self):
        print("\n🧠 OMEGA COGNITIVE ORGANISM v4\n")

        for n in self.nodes.values():
            print("────────────────────")
            print(f"NODE     : {n.id}")
            print(f"HEALTH   : {round(n.health, 3)}")
            print(f"ENERGY   : {round(n.energy, 3)}")
            print(f"STABILITY: {round(n.stability, 3)}")
            print(f"AGE      : {n.age}")


# ============================
# BOOT
# ============================

if __name__ == "__main__":
    org = OmegaCognitiveOrganismV4()

    org.add_node(NodeV4("swarm_bus", "runtime"))
    org.add_node(NodeV4("memory", "core"))
    org.add_node(NodeV4("assistant", "core"))
    org.add_node(NodeV4("emitter", "runtime"))

    org.link("swarm_bus", "memory")
    org.link("memory", "assistant")
    org.link("emitter", "swarm_bus")

    for _ in range(3):
        org.tick()

    org.snapshot()
