import time
import random
from collections import defaultdict

from omega_state import OmegaState


# =========================
# 🧠 SOCIETY ECONOMY CORE
# =========================
class CognitiveSociety:
    def __init__(self):
        self.wealth = defaultdict(lambda: 1.0)
        self.influence = defaultdict(float)
        self.coalitions = []
        self.history = []

        self.society_pool = 100.0  # shared attention currency

    # -------------------------
    # RESOURCE ALLOCATION
    # -------------------------
    def distribute_resources(self, nodes):
        share = self.society_pool / len(nodes)

        for n in nodes:
            self.wealth[n] += share * random.uniform(0.8, 1.2)

    # -------------------------
    # INFLUENCE SCORING
    # -------------------------
    def compute_influence(self):
        for n, w in self.wealth.items():
            self.influence[n] = w * random.uniform(0.9, 1.1)

    # -------------------------
    # COALITION FORMATION
    # -------------------------
    def form_coalitions(self, nodes):
        shuffled = nodes[:]
        random.shuffle(shuffled)

        self.coalitions = [
            shuffled[i:i+2] for i in range(0, len(shuffled), 2)
        ]

    # -------------------------
    # NEGOTIATION MODEL
    # -------------------------
    def negotiate(self):
        agreements = []

        for group in self.coalitions:
            if not group:
                continue

            total_influence = sum(self.influence[n] for n in group)

            leader = max(group, key=lambda n: self.influence[n])

            agreements.append({
                "leader": leader,
                "members": group,
                "power": total_influence
            })

        return agreements

    # -------------------------
    # SOCIETY UPDATE LOOP
    # -------------------------
    def step(self, nodes):
        self.distribute_resources(nodes)
        self.compute_influence()
        self.form_coalitions(nodes)

        agreements = self.negotiate()

        # update society pool (feedback loop)
        self.society_pool *= 0.99

        # reinforcement: strongest coalition grows influence
        if agreements:
            strongest = max(agreements, key=lambda x: x["power"])
            self.wealth[strongest["leader"]] += 2.0

        self.history.append(agreements)

        return agreements


# =========================
# 🧠 V45 KERNEL
# =========================
class OmegaKernelV45:
    def __init__(self):
        self.state = OmegaState()

        self.nodes = ["attention", "memory", "goal", "stability"]

        self.society = CognitiveSociety()

        self.tick_rate = 1

    # -------------------------
    # SIGNAL GENERATION
    # -------------------------
    def generate_signals(self):
        return {
            n: random.uniform(0.5, 2.0)
            for n in self.nodes
        }

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        signals = self.generate_signals()

        agreements = self.society.step(self.nodes)

        leader = max(self.society.wealth.items(), key=lambda x: x[1])[0]

        self.state.remember({
            "tick": tick,
            "leader": leader,
            "wealth": dict(self.society.wealth),
            "agreements": agreements
        })

        print(
            f"[V45] tick={tick} | "
            f"leader={leader} | "
            f"coalitions={len(self.society.coalitions)} | "
            f"pool={self.society.society_pool:.2f}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V45] COGNITIVE SOCIETY LAYER ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV45().run()
