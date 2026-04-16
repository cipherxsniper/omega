import time
import random
from collections import defaultdict


# =========================
# 🧠 SOCIETY MEMORY BUS
# =========================
class SocietyBus:
    def __init__(self):
        self.messages = []

    def broadcast(self, sender, msg):
        self.messages.append((sender, msg))

    def collect(self, receiver):
        # return recent messages not from self
        return [m for m in self.messages[-10:] if m[0] != receiver]


# =========================
# 🧠 AGENT (SOCIAL ENTITY)
# =========================
class Agent:
    def __init__(self, name):
        self.name = name
        self.energy = random.uniform(0.8, 1.2)
        self.memory = []
        self.fitness = random.uniform(0.5, 1.0)
        self.alive = True

    def perceive(self, bus):
        msgs = bus.collect(self.name)
        influence = sum(m[1] for m in msgs if isinstance(m[1], (int, float)))
        return influence * 0.05

    def act(self, bus):
        if not self.alive:
            return 0

        social_influence = self.perceive(bus)

        decision = (
            random.uniform(-0.3, 0.3)
            + social_influence
            + self.fitness * 0.1
        )

        # memory
        self.memory.append(decision)
        if len(self.memory) > 20:
            self.memory.pop(0)

        # energy dynamics (SURVIVAL PRESSURE)
        self.energy += decision * 0.1
        self.energy -= 0.02  # metabolic cost

        # communication
        bus.broadcast(self.name, decision)

        # death condition
        if self.energy <= 0:
            self.alive = False

        return decision


# =========================
# 🧠 SOCIETY ENGINE
# =========================
class CognitiveSocietyV57:
    def __init__(self):
        self.bus = SocietyBus()
        self.agents = [
            Agent("attention"),
            Agent("memory"),
            Agent("goal"),
            Agent("stability"),
        ]
        self.tick = 0

    def step(self):
        self.tick += 1

        alive_agents = 0
        total_energy = 0

        for agent in self.agents:
            agent.act(self.bus)
            if agent.alive:
                alive_agents += 1
                total_energy += agent.energy

        avg_energy = total_energy / max(alive_agents, 1)

        # reproduction pressure (emergence)
        if alive_agents < 4 and avg_energy > 1.0:
            new_agent = Agent(f"spawn_{self.tick}")
            self.agents.append(new_agent)

        print(
            f"[V57] tick={self.tick} | "
            f"alive={alive_agents} | "
            f"avg_energy={avg_energy:.3f}"
        )

    def run(self):
        print("[V57] COGNITIVE SOCIETY LAYER ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    CognitiveSocietyV57().run()
