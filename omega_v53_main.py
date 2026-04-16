import time
import random
from collections import defaultdict, deque


# =========================
# 🧠 BIOSPHERE MEMORY FIELD
# =========================
class BiosphereMemory:
    def __init__(self):
        self.global_memory = deque(maxlen=2000)
        self.hazard_map = defaultdict(float)
        self.success_map = defaultdict(float)

    def record(self, event):
        self.global_memory.append(event)

        key = event["type"]
        score = event.get("score", 0.5)

        if score < 0.4:
            self.hazard_map[key] += 0.1
        else:
            self.success_map[key] += 0.1

    def get_pressure(self, key):
        return self.success_map[key] - self.hazard_map[key]


# =========================
# 🪐 PLANET
# =========================
class Planet:
    def __init__(self, name):
        self.name = name
        self.species = defaultdict(list)
        self.entropy = random.uniform(0.5, 1.5)

    def update_entropy(self):
        self.entropy += random.uniform(-0.1, 0.1)
        self.entropy = max(0.1, min(2.0, self.entropy))


# =========================
# 🌱 SPECIES NODE
# =========================
class Species:
    def __init__(self, name):
        self.name = name
        self.energy = random.uniform(0.5, 1.5)
        self.adaptability = random.uniform(0.4, 1.2)

    def evolve(self, entropy_pressure):
        self.energy += random.uniform(-0.2, 0.3)

        # entropy resistance
        self.energy -= entropy_pressure * 0.1

        self.energy = max(0.05, self.energy)

    def migration_score(self):
        return self.energy * self.adaptability


# =========================
# 🌍 V53 ECOSYSTEM ENGINE
# =========================
class V53Biosphere:
    def __init__(self):
        self.biosphere = BiosphereMemory()

        self.planets = {
            "earth": Planet("earth"),
            "mars": Planet("mars"),
            "venus": Planet("venus")
        }

        # seed species
        for p in self.planets.values():
            for i in range(3):
                sp = Species(f"{p.name}_species_{i}")
                p.species[p.name].append(sp)

        self.tick = 0

    # -------------------------
    # MIGRATION SYSTEM
    # -------------------------
    def migrate(self):
        for planet in self.planets.values():
            for species_list in planet.species.values():
                for sp in species_list[:]:
                    score = sp.migration_score()

                    if score > 1.2 and random.random() < 0.1:
                        target = random.choice(list(self.planets.values()))

                        if target.name != planet.name:
                            species_list.remove(sp)
                            target.species[target.name].append(sp)

                            self.biosphere.record({
                                "type": "migration",
                                "score": score,
                                "from": planet.name,
                                "to": target.name
                            })

    # -------------------------
    # EVOLUTION STEP
    # -------------------------
    def evolve(self):
        for planet in self.planets.values():
            planet.update_entropy()

            for species_list in planet.species.values():
                for sp in species_list:
                    sp.evolve(planet.entropy)

    # -------------------------
    # GLOBAL UPDATE
    # -------------------------
    def step(self):
        self.tick += 1

        self.evolve()
        self.migrate()

        total_species = sum(
            len(s) for p in self.planets.values() for s in p.species.values()
        )

        avg_entropy = sum(p.entropy for p in self.planets.values()) / len(self.planets)

        print(
            f"[V53] tick={self.tick} "
            f"| planets={len(self.planets)} "
            f"| species={total_species} "
            f"| entropy={avg_entropy:.3f}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V53] BIOSPHERE + CROSS-PLANET NETWORK ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    V53Biosphere().run()
