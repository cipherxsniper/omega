import time
import random
from collections import defaultdict


# =========================
# 🧠 CIVILIZATION ENTITY
# =========================
class Civilization:
    def __init__(self, cid):
        self.id = cid
        self.members = []
        self.ideology = random.uniform(0.3, 1.0)
        self.stability = random.uniform(0.5, 1.0)

    def absorb(self, species):
        self.members.append(species)
        self.ideology += species.fitness * 0.01
        self.stability *= 0.999

    def score(self):
        return len(self.members) * self.ideology * self.stability


# =========================
# 🧠 PLANET MIND
# =========================
class PlanetMind:
    def __init__(self, name):
        self.name = name
        self.civilizations = []
        self.pressure = random.uniform(0.5, 1.5)
        self.memory = defaultdict(float)

    def form_civilizations(self, species_pool):
        # clustering phase
        for sp in species_pool:
            if random.random() < 0.2:
                cid = f"{self.name}_civ_{random.randint(1,3)}"

                civ = next((c for c in self.civilizations if c.id == cid), None)
                if not civ:
                    civ = Civilization(cid)
                    self.civilizations.append(civ)

                civ.absorb(sp)

    def evolve(self):
        self.pressure += random.uniform(-0.03, 0.03)
        self.pressure = max(0.2, min(2.0, self.pressure))

        for civ in self.civilizations:
            self.memory[civ.id] += civ.score() * 0.01

        # decay memory to prevent runaway dominance
        for k in list(self.memory.keys()):
            self.memory[k] *= 0.995


# =========================
# 🧠 FEDERATION MIND
# =========================
class FederationMind:
    def __init__(self):
        self.global_memory = defaultdict(float)
        self.entropy = 1.0

    def update(self, planets):
        total = 0

        for p in planets:
            for civ in p.civilizations:
                self.global_memory[civ.id] += civ.score()
                total += civ.score()

        # entropy normalization
        self.entropy = total / (len(self.global_memory) + 1e-9)


# =========================
# 🌍 V55 SYSTEM
# =========================
class V55System:
    def __init__(self):
        self.planets = [
            PlanetMind("earth"),
            PlanetMind("mars"),
            PlanetMind("venus")
        ]

        self.federation = FederationMind()

        self.tick = 0

    def step(self):
        self.tick += 1

        # simulate species pool (simplified)
        species_pool = [{"fitness": random.uniform(0.3, 1.2)} for _ in range(10)]

        for planet in self.planets:
            planet.form_civilizations(species_pool)
            planet.evolve()

        self.federation.update(self.planets)

        top = max(
            self.federation.global_memory.items(),
            key=lambda x: x[1],
            default=("none", 0)
        )

        print(
            f"[V55] tick={self.tick} | "
            f"civilizations={sum(len(p.civilizations) for p in self.planets)} | "
            f"top_civ={top[0]} | "
            f"federation_entropy={self.federation.entropy:.3f}"
        )

    def run(self):
        print("[V55] PLANETARY CIVILIZATION CONSCIOUSNESS ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    V55System().run()
