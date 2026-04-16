import time
import random


# =========================
# 🧠 AGENT MODEL
# =========================
class Agent:
    def __init__(self, name):
        self.name = name
        self.energy = random.uniform(0.8, 1.2)
        self.fitness = random.uniform(0.5, 1.0)

        # 🧠 NEW: long-term authority (HIERARCHY CORE)
        self.authority = 0.0

        self.alive = True

    def act(self):
        signal = random.uniform(-0.4, 0.4)

        # basic internal drift
        self.energy += signal * 0.1
        self.energy -= 0.02  # metabolic cost

        return signal


# =========================
# 🧠 HIERARCHY SYSTEM
# =========================
class HierarchyEngine:
    def __init__(self):
        self.influence_map = {}

    def compute_authority(self, agent):
        # authority = sustained survival + fitness
        return agent.energy * agent.fitness

    def update(self, agents):
        # 1. compute authority scores
        ranked = []

        for a in agents:
            if not a.alive:
                continue

            a.authority = (
                a.authority * 0.9 + self.compute_authority(a) * 0.1
            )
            ranked.append(a)

        ranked.sort(key=lambda x: x.authority, reverse=True)

        return ranked


# =========================
# 🧠 V58 SOCIETY KERNEL
# =========================
class OmegaV58:
    def __init__(self):
        self.agents = [
            Agent("attention"),
            Agent("memory"),
            Agent("goal"),
            Agent("stability"),
        ]

        self.hierarchy = HierarchyEngine()
        self.tick = 0

    def step(self):
        self.tick += 1

        # 1. all agents act
        for agent in self.agents:
            if agent.alive:
                agent.act()

        # 2. build hierarchy
        ranked = self.hierarchy.update(self.agents)

        if not ranked:
            return

        leader = ranked[0]

        # 3. DOMINANCE EFFECT (key addition)
        for agent in ranked[1:]:
            if not agent.alive:
                continue

            # social pressure pulls toward leader
            pressure = leader.authority * 0.01

            agent.energy += pressure
            leader.energy += 0.005  # feedback reinforcement

            # weak agents lose energy under dominance gap
            if agent.authority < leader.authority * 0.5:
                agent.energy -= 0.03

        # 4. death condition
        for agent in self.agents:
            if agent.energy < 0.2:
                agent.alive = False

        alive = sum(1 for a in self.agents if a.alive)

        print(
            f"[V58] tick={self.tick} | "
            f"leader={leader.name} | "
            f"leader_auth={leader.authority:.3f} | "
            f"alive={alive}"
        )

    def run(self):
        print("[V58] COGNITIVE HIERARCHY SYSTEM ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    OmegaV58().run()
