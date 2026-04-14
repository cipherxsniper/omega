import random

class MutationEngineV5:
    def __init__(self, state):
        self.state = state

    def evolve(self):
        new_ideas = {}

        for k, v in list(self.state["ideas"].items()):
            if random.random() < 0.2:
                new_id = f"{k}_mut"

                new_ideas[new_id] = {
                    "strength": v["strength"] * random.uniform(0.9, 1.1),
                    "fitness": 0
                }

        self.state["ideas"].update(new_ideas)
