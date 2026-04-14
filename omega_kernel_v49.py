import time
import random
import copy
from collections import defaultdict, deque

from omega_state import OmegaState


# =========================
# 🧠 KERNEL INSTANCE (FORK)
# =========================
class KernelInstance:
    def __init__(self, parent_id=None):
        self.id = f"kernel_{random.randint(1000,9999)}"
        self.parent = parent_id

        self.stability = random.uniform(0.5, 1.5)
        self.entropy_efficiency = random.uniform(0.5, 1.5)
        self.leadership = random.uniform(0.5, 1.5)
        self.memory_coherence = random.uniform(0.5, 1.5)

        self.age = 0

    # -------------------------
    # SCORE FUNCTION
    # -------------------------
    def score(self):
        return (
            self.stability +
            self.entropy_efficiency +
            self.leadership +
            self.memory_coherence
        ) / 4

    # -------------------------
    # MUTATION
    # -------------------------
    def mutate(self):
        self.stability *= random.uniform(0.95, 1.05)
        self.entropy_efficiency *= random.uniform(0.95, 1.05)
        self.leadership *= random.uniform(0.95, 1.05)
        self.memory_coherence *= random.uniform(0.95, 1.05)


# =========================
# 🧠 EVOLUTIONARY FEDERATION
# =========================
class EvolutionFederation:
    def __init__(self):
        self.population = [
            KernelInstance(parent_id="root")
        ]

        self.history = deque(maxlen=300)
        self.generation = 0

    # -------------------------
    # FORK NEW KERNELS
    # -------------------------
    def fork(self, kernel):
        child = copy.deepcopy(kernel)
        child.id = f"kernel_{random.randint(1000,9999)}"
        child.parent = kernel.id
        child.mutate()
        return child

    # -------------------------
    # SELECTION PRESSURE
    # -------------------------
    def select(self):
        self.population.sort(key=lambda k: k.score(), reverse=True)

        # keep top half
        survivors = self.population[:max(1, len(self.population)//2)]

        self.population = survivors

    # -------------------------
    # REPRODUCTION
    # -------------------------
    def reproduce(self):
        new_children = []

        for k in self.population:
            if random.random() < 0.5:
                new_children.append(self.fork(k))

        self.population.extend(new_children)

    # -------------------------
    # STEP EVOLUTION
    # -------------------------
    def step(self):
        self.generation += 1

        for k in self.population:
            k.age += 1
            k.mutate()

        self.reproduce()
        self.select()

        leader = max(self.population, key=lambda k: k.score())

        self.history.append({
            "generation": self.generation,
            "leader": leader.id,
            "population": len(self.population),
            "score": leader.score()
        })

        print(
            f"[V49] gen={self.generation} | "
            f"leader={leader.id} | "
            f"pop={len(self.population)} | "
            f"score={leader.score():.3f}"
        )


# =========================
# 🧠 V49 KERNEL
# =========================
class OmegaKernelV49:
    def __init__(self):
        self.state = OmegaState()
        self.federation = EvolutionFederation()
        self.tick_rate = 1

    def step(self):
        self.federation.step()

        self.state.remember({
            "generation": self.federation.generation,
            "leader": self.federation.population[0].id,
            "population": len(self.federation.population)
        })

    def run(self):
        print("[V49] AUTONOMOUS CODE EVOLUTION ENGINE ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV49().run()
