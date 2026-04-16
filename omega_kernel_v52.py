import time
import random
import math
from collections import defaultdict, deque


# =========================
# 🌍 PLANETARY MEMORY STATE
# =========================
class PlanetState:
    def __init__(self):
        self.tick = 0
        self.memory = deque(maxlen=500)
        self.species = defaultdict(set)
        self.global_entropy = 1.0
        self.climate_temperature = 1.0

    def step(self):
        self.tick += 1
        return self.tick


# =========================
# 🧠 COGNITIVE NODE
# =========================
class Node:
    def __init__(self, name):
        self.name = name
        self.energy = random.uniform(0.5, 1.5)
        self.age = 0

    def update(self, climate):
        self.age += 1

        # environmental adaptation
        self.energy += random.uniform(-0.1, 0.2) * climate

        # decay pressure
        self.energy *= 0.995

        return self.energy


# =========================
# 🌱 SPECIES CLUSTER
# =========================
class Species:
    def __init__(self, name):
        self.name = name
        self.nodes = {}
        self.fitness = 1.0

    def add_node(self, node):
        self.nodes[node.name] = node

    def evaluate(self):
        if not self.nodes:
            return 0.0

        self.fitness = sum(n.energy for n in self.nodes.values()) / len(self.nodes)
        return self.fitness


# =========================
# 🌍 PLANETARY COGNITION ENGINE
# =========================
class PlanetaryCognition:
    def __init__(self):
        self.state = PlanetState()

        self.species = {
            "attention": Species("attention"),
            "memory": Species("memory"),
            "goal": Species("goal"),
            "stability": Species("stability")
        }

        # seed nodes
        for s in self.species.values():
            for i in range(2):
                s.add_node(Node(f"{s.name}_{i}"))

    # -------------------------
    # CLIMATE MODEL
    # -------------------------
    def update_climate(self):
        all_energy = []

        for s in self.species.values():
            for n in s.nodes.values():
                all_energy.append(n.energy)

        if not all_energy:
            return

        avg = sum(all_energy) / len(all_energy)

        # entropy = variance pressure
        variance = sum((x - avg) ** 2 for x in all_energy) / len(all_energy)
        entropy = math.sqrt(variance)

        self.state.global_entropy = entropy

        # climate feedback loop
        self.state.climate_temperature = 1.0 + entropy

    # -------------------------
    # EVOLUTION STEP
    # -------------------------
    def evolve(self):
        for species in self.species.values():
            species.evaluate()

            # extinction pressure
            if species.fitness < 0.3:
                # collapse event
                if random.random() < 0.2:
                    species.nodes.clear()

            # reproduction pressure
            if species.fitness > 1.2:
                new_node = Node(f"{species.name}_mut_{random.randint(0,999)}")
                species.add_node(new_node)

    # -------------------------
    # MIGRATION SYSTEM
    # -------------------------
    def migrate(self):
        all_nodes = []

        for s in self.species.values():
            for n in list(s.nodes.values()):
                all_nodes.append((s.name, n))

        if len(all_nodes) < 2:
            return

        for origin, node in all_nodes:
            if random.random() < 0.05:
                target_species = random.choice(list(self.species.values()))
                self.species[origin].nodes.pop(node.name, None)
                target_species.add_node(node)

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        tick = self.state.step()

        # update nodes
        for species in self.species.values():
            for node in species.nodes.values():
                node.update(self.state.climate_temperature)

        # system dynamics
        self.update_climate()
        self.evolve()
        self.migrate()

        # log
        total_nodes = sum(len(s.nodes) for s in self.species.values())

        print(
            f"[V52] tick={tick} "
            f"| entropy={self.state.global_entropy:.3f} "
            f"| temp={self.state.climate_temperature:.3f} "
            f"| nodes={total_nodes}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V52] PLANETARY COGNITION ECOLOGY ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    PlanetaryCognition().run()
