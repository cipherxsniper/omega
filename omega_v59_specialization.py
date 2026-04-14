import time
import random


# =========================
# 🧠 AGENT (ROLE-DRIVEN)
# =========================
class Agent:
    def __init__(self, name):
        self.name = name
        self.energy = random.uniform(0.9, 1.1)

        # 🧠 ROLE VECTOR (emergent identity)
        self.role = {
            "explorer": random.random(),
            "stabilizer": random.random(),
            "dominator": random.random(),
            "adapter": random.random()
        }

        self.fitness = random.uniform(0.5, 1.0)
        self.alive = True

    # -------------------------
    # ROLE NORMALIZATION
    # -------------------------
    def normalize_roles(self):
        total = sum(self.role.values())
        for k in self.role:
            self.role[k] /= total

    # -------------------------
    # ROLE-INFLUENCED ACTION
    # -------------------------
    def act(self):
        self.normalize_roles()

        r = self.role

        # behavior emerges from role mix
        signal = (
            random.uniform(-0.4, 0.4) * r["explorer"]
            - random.uniform(0, 0.3) * r["stabilizer"]
            + random.uniform(0, 0.5) * r["dominator"]
            + random.uniform(-0.2, 0.2) * r["adapter"]
        )

        self.energy += signal * 0.1
        self.energy -= 0.02

        return signal


# =========================
# 🧠 ROLE EVOLUTION ENGINE
# =========================
class RoleEvolution:
    def evolve(self, agent, performance):
        # reinforce successful roles
        if performance > 0:
            agent.role["dominator"] += 0.01 * performance
            agent.role["adapter"] += 0.005

        else:
            agent.role["stabilizer"] += 0.01
            agent.role["explorer"] += 0.005

        # natural decay (prevents lock-in)
        for k in agent.role:
            agent.role[k] *= 0.995


# =========================
# 🧠 V59 SOCIETY ENGINE
# =========================
class OmegaV59:
    def __init__(self):
        self.agents = [
            Agent("A"),
            Agent("B"),
            Agent("C"),
            Agent("D"),
        ]

        self.evolver = RoleEvolution()
        self.tick = 0

    def step(self):
        self.tick += 1

        performances = []

        # 1. agents act
        for agent in self.agents:
            if not agent.alive:
                continue

            signal = agent.act()

            performance = agent.energy * signal
            performances.append((performance, agent))

        # 2. role evolution feedback loop
        for perf, agent in performances:
            self.evolver.evolve(agent, perf)

        # 3. survival pressure
        for agent in self.agents:
            if agent.energy < 0.2:
                agent.alive = False

        # 4. summary stats
        alive = sum(1 for a in self.agents if a.alive)

        avg_roles = {
            "explorer": sum(a.role["explorer"] for a in self.agents) / len(self.agents),
            "stabilizer": sum(a.role["stabilizer"] for a in self.agents) / len(self.agents),
            "dominator": sum(a.role["dominator"] for a in self.agents) / len(self.agents),
            "adapter": sum(a.role["adapter"] for a in self.agents) / len(self.agents),
        }

        dominant_role = max(avg_roles, key=avg_roles.get)

        print(
            f"[V59] tick={self.tick} | "
            f"alive={alive} | "
            f"dominant_role={dominant_role} | "
            f"roles={ {k: round(v,3) for k,v in avg_roles.items()} }"
        )

    def run(self):
        print("[V59] COGNITIVE SPECIALIZATION SYSTEM ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    OmegaV59().run()
