import random

class ReinforcementEngine:
    def __init__(self, state):
        self.state = state

    def reward_node(self, node_id, value):
        self.state["rewards"][node_id] = \
            self.state["rewards"].get(node_id, 0) + value

    def compute_fitness(self, node_id):
        reward = self.state["rewards"].get(node_id, 0)
        entropy_penalty = random.uniform(0.0, 0.1)

        fitness = reward - entropy_penalty
        self.state["fitness"][node_id] = fitness

        return fitness
