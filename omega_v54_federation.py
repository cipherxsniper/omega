import time
import random
from collections import defaultdict, deque


# =========================
# 🧠 FEDERATION MEMORY LATTICE
# =========================
class CognitionLattice:
    def __init__(self):
        self.global_knowledge = defaultdict(float)
        self.inhibitors = defaultdict(float)
        self.lineage = defaultdict(list)

    def reinforce(self, key, value):
        self.global_knowledge[key] += value

    def inhibit(self, key, value):
        self.inhibitors[key] += value

    def score(self, key):
        return self.global_knowledge[key] - self.inhibitors[key]


# =========================
# ⚖️ FEDERATION ARBITER
# =========================
class Federation:
    def __init__(self, lattice):
        self.lattice = lattice

    def decide_migration(self, species_score, target_pressure):
        if species_score > target_pressure + 0.2:
            return "allow"
        elif species_score < target_pressure:
            return "block"
        else:
            return "mutate"


# =========================
# 🪐 PLANET
# =========================
class Planet:
    def __init__(self, name):
        self.name = name
        self.species = []
        self.pressure = random.uniform(0.4, 1.4)

    def update_pressure(self):
        self.pressure += random.uniform(-0.05, 0.05)
        self.pressure = max(0.1, min(2.0, self.pressure))


# =========================
# 🌱 SPECIES
# =========================
class Species:
    def __init__(self, name):
        self.name = name
        self.energy = random.uniform(0.5, 1.5)
        self.fitness = random.uniform(0.4, 1.2)
        self.age = 0

    def evolve(self, pressure):
        self.age += 1
        self.energy += random.uniform(-0.1, 0.2)
        self.energy -= pressure * 0.05
        self.energy = max(0.05, self.energy)

    def score(self):
        return self.energy * self.fitness


# =========================
# 🌌 V54 FEDERATED SYSTEM
# =========================
class V54FederationSystem:
    def __init__(self):
        self.lattice = CognitionLattice()
        self.federation = Federation(self.lattice)

        self.planets = {
            "earth": Planet("earth"),
            "mars": Planet("mars"),
            "venus": Planet("venus"),
            "io": Planet("io")
        }

        # seed species
        for p in self.planets.values():
            for i in range(3):
                p.species.append(Species(f"{p.name}_sp_{i}"))

        self.tick = 0

    # -------------------------
    # FEDERATION UPDATE
    # -------------------------
    def federation_cycle(self):
        for planet in self.planets.values():
            planet.update_pressure()

            for sp in planet.species:
                sp.evolve(planet.pressure)

                score = sp.score()

                # feed lattice
                self.lattice.reinforce(planet.name, score)

                # migration attempt
                target = random.choice(list(self.planets.values()))
                decision = self.federation.decide_migration(
                    score,
                    target.pressure
                )

                if decision == "allow":
                    planet.species.remove(sp)
                    target.species.append(sp)
                    self.lattice.reinforce("migration_success", 1)

                elif decision == "block":
                    self.lattice.inhibit("migration_block", 1)

                elif decision == "mutate":
                    sp.fitness *= random.uniform(0.95, 1.05)
                    self.lattice.reinforce("mutation_event", 1)

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        self.tick += 1
        self.federation_cycle()

        total_species = sum(len(p.species) for p in self.planets.values())

        top_signal = max(
            self.lattice.global_knowledge.items(),
            key=lambda x: x[1],
            default=("none", 0)
        )

        print(
            f"[V54] tick={self.tick} | "
            f"species={total_species} | "
            f"top_signal={top_signal[0]} | "
            f"signal_strength={top_signal[1]:.3f}"
        )

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V54] INTERPLANETARY INTELLIGENCE FEDERATION ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    V54FederationSystem().run()
