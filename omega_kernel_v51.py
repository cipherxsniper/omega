import time
import random
import math
from collections import defaultdict, deque


# =========================
# 🌪 COGNITIVE CLIMATE FIELD
# =========================
class CognitiveClimate:
    def __init__(self):
        self.pressure_map = defaultdict(float)
        self.storm_level = 0.0
        self.history = deque(maxlen=200)

    def update(self, signals):
        total = sum(signals.values()) + 1e-9

        # pressure field = normalized demand per node
        for k, v in signals.items():
            self.pressure_map[k] = v / total

        # storm detection (entropy proxy)
        variance = sum((v - 1/len(signals))**2 for v in signals.values())
        self.storm_level = math.sqrt(variance)

        self.history.append(self.storm_level)

    def is_storm(self):
        return self.storm_level > 0.35


# =========================
# 🧬 SPECIES LAYER
# =========================
class CognitiveSpecies:
    def __init__(self, name):
        self.name = name
        self.fitness = 1.0
        self.population = 5

    def evolve(self, climate_pressure):
        self.fitness *= (1.0 + climate_pressure - 0.5)

        # population drift
        if self.fitness > 1.5:
            self.population += 1
        elif self.fitness < 0.7:
            self.population -= 1

        self.population = max(1, min(50, self.population))


# =========================
# 🌍 GLOBAL V51 KERNEL
# =========================
class OmegaKernelV51:
    def __init__(self):
        self.tick = 0

        self.species = {
            "v40_core": CognitiveSpecies("v40_core"),
            "v42_federation": CognitiveSpecies("v42_federation"),
            "v48_compiler": CognitiveSpecies("v48_compiler"),
        }

        self.climate = CognitiveClimate()

        self.memory = deque(maxlen=300)

    # -------------------------
    # SIGNAL GENERATION
    # -------------------------
    def generate_signals(self):
        return {
            "attention": random.random(),
            "memory": random.random(),
            "goal": random.random(),
            "stability": random.random()
        }

    # -------------------------
    # COLLAPSE EVENT
    # -------------------------
    def collapse(self):
        print("💥 [V51] EXTINCTION EVENT TRIGGERED")

        for s in self.species.values():
            s.population = max(1, s.population // 2)
            s.fitness *= 0.8

        self.memory.clear()

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        self.tick += 1

        signals = self.generate_signals()
        self.climate.update(signals)

        # evolve species based on climate pressure
        for s in self.species.values():
            avg_pressure = sum(self.climate.pressure_map.values())
            s.evolve(avg_pressure)

        # collapse condition
        if self.climate.is_storm() and random.random() < 0.15:
            self.collapse()

        # log state
        state = {
            "tick": self.tick,
            "storm": self.climate.storm_level,
            "species": {k: v.population for k, v in self.species.items()}
        }

        self.memory.append(state)

        print(
            f"[V51] tick={self.tick} | "
            f"storm={self.climate.storm_level:.3f} | "
            f"v40={self.species['v40_core'].population} | "
            f"v42={self.species['v42_federation'].population} | "
            f"v48={self.species['v48_compiler'].population}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V51] GLOBAL COGNITIVE CLIMATE ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    OmegaKernelV51().run()
