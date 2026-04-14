import random
import math
from collections import defaultdict

class CognitiveEconomyAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.energy = random.uniform(0.8, 1.2)
        self.influence = 1.0
        self.memory = random.uniform(0.5, 1.0)
        self.role_bias = {
            "explorer": 0.25,
            "stabilizer": 0.25,
            "dominator": 0.25,
            "adapter": 0.25
        }

    def compute_value(self):
        return (self.energy * 0.5 +
                self.influence * 0.3 +
                self.memory * 0.2)

    def act(self):
        role = max(self.role_bias, key=self.role_bias.get)

        cost = 0.03 + (1.0 - self.memory) * 0.02
        self.energy -= cost

        gain = random.uniform(0.01, 0.08) * self.memory

        self.energy += gain

        # memory drift
        self.memory *= (0.99 + random.uniform(-0.01, 0.02))

        return role


class CognitiveEconomySystem:
    def __init__(self):
        self.agents = [CognitiveEconomyAgent(i) for i in range(6)]
        self.tick = 0

    def trade(self):
        # pairwise influence exchange
        for a in self.agents:
            partner = random.choice(self.agents)

            delta = (a.compute_value() - partner.compute_value()) * 0.01

            a.influence += delta
            partner.influence -= delta

    def collapse_check(self):
        # remove weak agents
        self.agents = [a for a in self.agents if a.energy > 0.2]

        # regeneration pressure
        if len(self.agents) < 4:
            self.agents.append(CognitiveEconomyAgent(self.tick))

    def step(self):
        self.tick += 1

        roles = defaultdict(int)

        for a in self.agents:
            role = a.act()
            roles[role] += 1

        self.trade()
        self.collapse_check()

        print(
            f"[V60] tick={self.tick} "
            f"agents={len(self.agents)} "
            f"roles={dict(roles)} "
            f"avg_energy={sum(a.energy for a in self.agents)/len(self.agents):.3f}"
        )


if __name__ == "__main__":
    system = CognitiveEconomySystem()
    while True:
        system.step()
