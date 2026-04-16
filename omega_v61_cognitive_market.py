import random
from collections import defaultdict


# =========================
# 💰 MARKET PRICE FIELD
# =========================
class PriceField:
    def __init__(self):
        self.prices = {
            "explorer": 1.0,
            "stabilizer": 1.0,
            "dominator": 1.0,
            "adapter": 1.0
        }

    def update(self, role_counts, avg_energy):
        total = sum(role_counts.values()) + 1e-9

        for role in self.prices:
            scarcity = 1.0 / (role_counts.get(role, 1) + 1e-9)

            # energy pressure affects inflation/deflation
            energy_factor = 1.0 + (1.0 - avg_energy)

            self.prices[role] = max(
                0.1,
                min(5.0, scarcity * energy_factor)
            )


# =========================
# 🧠 AGENT
# =========================
class MarketAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.energy = random.uniform(0.8, 1.2)
        self.memory = random.uniform(0.5, 1.0)
        self.influence = 1.0

    def choose_role(self, prices):
        # utility = memory + energy + market pressure
        scores = {}

        for role, price in prices.items():
            utility = (
                self.memory * 0.4 +
                self.energy * 0.4 +
                price * 0.2
            )
            scores[role] = utility

        return max(scores, key=scores.get)

    def act(self, role):
        cost = 0.02 * random.random()
        gain = 0.05 * self.memory * random.random()

        self.energy += gain - cost
        self.memory *= (0.99 + random.uniform(-0.01, 0.02))

        return role


# =========================
# 🧠 MARKET SYSTEM
# =========================
class CognitiveMarketSystem:
    def __init__(self):
        self.agents = [MarketAgent(i) for i in range(6)]
        self.market = PriceField()
        self.tick = 0

    def collapse_check(self):
        self.agents = [a for a in self.agents if a.energy > 0.2]

        if len(self.agents) < 4:
            self.agents.append(MarketAgent(self.tick))

    def step(self):
        self.tick += 1

        role_counts = defaultdict(int)

        chosen_roles = []

        # agents act
        for a in self.agents:
            role = a.choose_role(self.market.prices)
            chosen_roles.append(role)

            a.act(role)
            role_counts[role] += 1

        avg_energy = sum(a.energy for a in self.agents) / len(self.agents)

        # update market
        self.market.update(role_counts, avg_energy)

        # collapse + recovery dynamics
        self.collapse_check()

        print(
            f"[V61] tick={self.tick} "
            f"agents={len(self.agents)} "
            f"avg_energy={avg_energy:.3f} "
            f"prices={dict(self.market.prices)} "
            f"roles={dict(role_counts)}"
        )


# =========================
# 🚀 RUN LOOP
# =========================
if __name__ == "__main__":
    system = CognitiveMarketSystem()
    while True:
        system.step()
