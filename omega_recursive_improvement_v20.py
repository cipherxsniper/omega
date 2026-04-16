import time
import random
import uuid
import copy
import json


class Idea:
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        self.strength = random.uniform(0.3, 1.0)

    def reinforce(self, value):
        self.strength += value
        self.strength = min(self.strength, 5.0)


class OmegaRecursive:

    def __init__(self):
        self.ideas = []
        self.tick = 0
        self.history = []

        self.params = {
            "spawn_rate": 0.3,
            "reinforce_rate": 0.05
        }

        self.current_strategy = "explore"

    def spawn(self):
        if random.random() < self.params["spawn_rate"]:
            self.ideas.append(Idea())

    def reinforce(self):
        for idea in self.ideas:
            idea.reinforce(self.params["reinforce_rate"])

    def observe(self):
        strength = 0
        if self.ideas:
            strength = sum(i.strength for i in self.ideas) / len(self.ideas)

        state = {
            "ideas": len(self.ideas),
            "strength": strength
        }

        self.history.append(copy.deepcopy(state))
        return state

    def compare(self):
        if len(self.history) < 2:
            return None

        prev = self.history[-2]
        curr = self.history[-1]

        return {
            "growth": curr["ideas"] - prev["ideas"],
            "strength_delta": curr["strength"] - prev["strength"]
        }

    def choose_strategy(self, delta):
        if not delta:
            return self.current_strategy

        if delta["growth"] < 1:
            return "growth"

        if delta["strength_delta"] < 0:
            return "stability"

        return "explore"

    def apply_strategy(self):
        if self.current_strategy == "growth":
            self.params["spawn_rate"] += 0.05

        elif self.current_strategy == "stability":
            self.params["reinforce_rate"] += 0.02

        elif self.current_strategy == "explore":
            self.params["spawn_rate"] += random.uniform(-0.02, 0.02)

    def step(self):
        self.tick += 1

        self.spawn()
        self.reinforce()

        state = self.observe()
        delta = self.compare()

        self.current_strategy = self.choose_strategy(delta)
        self.apply_strategy()

        meta = {
            "tick": self.tick,
            "strategy": self.current_strategy,
            "params": self.params,
            "state": state,
            "delta": delta
        }

        return meta


if __name__ == "__main__":
    system = OmegaRecursive()

    print("[Ω-v20] RECURSIVE SELF-IMPROVEMENT ONLINE")

    while True:
        meta = system.step()

        event = {
            "type": "v20_meta",
            "source": "omega_v20",
            "timestamp": time.time(),
            "data": meta
        }

        print(json.dumps(event))

        time.sleep(0.5)
