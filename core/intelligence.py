import random


class OmegaMind:
    def __init__(self, memory):
        self.memory = memory
        self.state = 0.5

    def step(self, features):
        score = sum(features) if features else random.random()

        self.state = (self.state * 0.9) + (score * 0.1)

        return "optimize" if self.state > 0.5 else "explore"

    def should_evolve(self):
        return random.random() > 0.95
