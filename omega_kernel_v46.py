import time
import random
from collections import defaultdict, deque

from omega_state import OmegaState


# =========================
# 🧠 SOCIETY ENTITY
# =========================
class Society:
    def __init__(self, name):
        self.name = name
        self.energy = random.uniform(5.0, 15.0)
        self.stability = random.uniform(0.5, 1.0)
        self.influence = random.uniform(0.5, 1.5)

        self.memory = deque(maxlen=100)
        self.trade_balance = 0.0

    def evolve(self):
        drift = random.uniform(-0.05, 0.05)

        self.energy = max(0.1, self.energy + drift)
        self.stability = min(1.0, max(0.1, self.stability + drift * 0.5))

    def score(self):
        return self.energy * self.stability * self.influence


# =========================
# 🧠 FEDERATION LAYER
# =========================
class OmegaFederation:
    def __init__(self):
        self.societies = {}

        # treat kernels as civilizations
        self.kernel_map = [
            "omega_kernel_v28",
            "omega_kernel_v37",
            "omega_kernel_v40",
            "omega_kernel_v43",
            "omega_kernel_v45"
        ]

        for k in self.kernel_map:
            self.societies[k] = Society(k)

        self.global_memory = deque(maxlen=300)

        self.tick = 0

    # -------------------------
    # INTER-SOCIETY TRADE
    # -------------------------
    def trade(self):
        names = list(self.societies.keys())
        random.shuffle(names)

        for i in range(len(names) - 1):
            a = self.societies[names[i]]
            b = self.societies[names[i + 1]]

            transfer = (a.score() - b.score()) * 0.01

            a.energy -= transfer
            b.energy += transfer

            a.trade_balance += transfer
            b.trade_balance -= transfer

    # -------------------------
    # EVOLUTION STEP
    # -------------------------
    def evolve(self):
        for s in self.societies.values():
            s.evolve()

    # -------------------------
    # LEADER ELECTION (FEDERATION LEVEL)
    # -------------------------
    def leader(self):
        return max(self.societies.values(), key=lambda s: s.score())

    # -------------------------
    # MEMORY AGGREGATION
    # -------------------------
    def aggregate_memory(self):
        snapshot = {
            name: s.score()
            for name, s in self.societies.items()
        }

        self.global_memory.append(snapshot)

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        self.tick += 1

        self.evolve()
        self.trade()
        self.aggregate_memory()

        leader = self.leader()

        print(
            f"[V46] tick={self.tick} | "
            f"leader={leader.name} | "
            f"societies={len(self.societies)}"
        )


# =========================
# 🧠 V46 KERNEL
# =========================
class OmegaKernelV46:
    def __init__(self):
        self.state = OmegaState()
        self.federation = OmegaFederation()
        self.tick_rate = 1

    def step(self):
        self.federation.step()

        self.state.remember({
            "tick": self.federation.tick,
            "leader": self.federation.leader().name,
            "societies": list(self.federation.societies.keys())
        })

    def run(self):
        print("[V46] MULTI-SOCIETY EVOLUTION LAYER ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV46().run()
