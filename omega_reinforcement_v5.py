import random

class ReinforcementEngineV5:
    def __init__(self, state):
        self.state = state

    def reward(self, idea_id, value):
        ideas = self.state["ideas"]
        if idea_id not in ideas:
            ideas[idea_id] = {"strength": 1.0, "fitness": 0.0}

        ideas[idea_id]["fitness"] = ideas[idea_id].get("fitness", 0) + value

    def decay_and_select(self):
        to_delete = []

        for i, idea in self.state["ideas"].items():
            fitness = idea.get("fitness", 0)

            # decay pressure
            idea["strength"] *= (0.98 + random.uniform(-0.01, 0.01))

            # survival rule
            if fitness < -0.5:
                to_delete.append(i)

        for i in to_delete:
            del self.state["ideas"][i]
