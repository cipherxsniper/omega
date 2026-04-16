import time
import random
from collections import defaultdict, deque

from omega_state import OmegaState


# =========================
# 🧠 SPECIES MODEL
# =========================
class Species:
    def __init__(self, name):
        self.name = name

        self.population = random.randint(2, 6)

        self.stability_bias = random.uniform(0.4, 1.5)
        self.exploration_bias = random.uniform(0.4, 1.5)
        self.memory_strength = random.uniform(0.4, 1.5)
        self.reproduction_rate = random.uniform(0.4, 1.5)

        self.energy = random.uniform(10.0, 30.0)

        self.age = 0

    # -------------------------
    # FITNESS SCORE
    # -------------------------
    def fitness(self):
        return (
            self.stability_bias +
            self.exploration_bias +
            self.memory_strength +
            self.reproduction_rate
        ) * (self.energy / (self.population + 1))

    # -------------------------
    # EVOLVE INTERNAL TRAITS
    # -------------------------
    def mutate(self):
        self.stability_bias *= random.uniform(0.95, 1.05)
        self.exploration_bias *= random.uniform(0.95, 1.05)
        self.memory_strength *= random.uniform(0.95, 1.05)
        self.reproduction_rate *= random.uniform(0.95, 1.05)

    # -------------------------
    # POPULATION DYNAMICS
    # -------------------------
    def reproduce(self):
        if self.energy > 5:
            births = int(self.reproduction_rate * random.uniform(0.5, 1.2))
            self.population += max(0, births)

    def die_off(self):
        loss = random.randint(0, max(1, int(self.population * 0.2)))
        self.population = max(1, self.population - loss)

    # -------------------------
    # ENERGY UPDATE
    # -------------------------
    def consume(self, env_energy):
        share = env_energy * (self.population / 50.0)
        self.energy += share - (self.population * 0.2)


# =========================
# 🧠 ENVIRONMENT
# =========================
class Environment:
    def __init__(self):
        self.energy_pool = 100.0
        self.decay_rate = 0.97

    def step(self):
        self.energy_pool *= self.decay_rate

        # random regeneration spikes
        if random.random() < 0.2:
            self.energy_pool += random.uniform(5, 15)

        self.energy_pool = min(150.0, self.energy_pool)


# =========================
# 🧠 V50 FEDERATION ENGINE
# =========================
class SpeciesFederation:
    def __init__(self):
        self.species = [
            Species("memory"),
            Species("attention"),
            Species("goal"),
            Species("stability"),
            Species("explorer")
        ]

        self.env = Environment()

        self.history = deque(maxlen=300)
        self.tick = 0

    # -------------------------
    # INTER-SPECIES COMPETITION
    # -------------------------
    def compete(self):
        for s in self.species:
            s.consume(self.env.energy_pool)

        # redistribute energy based on fitness dominance
        total_fitness = sum(s.fitness() for s in self.species)

        for s in self.species:
            share = (s.fitness() / (total_fitness + 1e-9))
            s.energy += share * 5

    # -------------------------
    # SELECTION PRESSURE
    # -------------------------
    def selection(self):
        self.species.sort(key=lambda s: s.fitness(), reverse=True)

        # weakest lose population
        for s in self.species[-2:]:
            s.die_off()

        # strongest expand
        self.species[0].reproduce()

    # -------------------------
    # EVOLUTION STEP
    # -------------------------
    def step(self):
        self.tick += 1

        self.env.step()

        for s in self.species:
            s.age += 1
            s.mutate()

        self.compete()
        self.selection()

        leader = max(self.species, key=lambda s: s.fitness())

        self.history.append({
            "tick": self.tick,
            "leader": leader.name,
            "energy_pool": self.env.energy_pool,
            "populations": {s.name: s.population for s in self.species}
        })

        print(
            f"[V50] tick={self.tick} | "
            f"leader={leader.name} | "
            f"energy={self.env.energy_pool:.2f} | "
            f"pop={sum(s.population for s in self.species)}"
        )


# =========================
# 🧠 V50 KERNEL
# =========================
class OmegaKernelV50:
    def __init__(self):
        self.state = OmegaState()
        self.federation = SpeciesFederation()
        self.tick_rate = 1

    def step(self):
        self.federation.step()

        self.state.remember({
            "tick": self.federation.tick,
            "leader": self.federation.species[0].name,
            "total_population": sum(s.population for s in self.federation.species)
        })

    def run(self):
        print("[V50] COGNITIVE SPECIES EVOLUTION SYSTEM ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV50().run()
