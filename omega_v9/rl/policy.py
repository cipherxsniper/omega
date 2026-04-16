class PolicyGradient:
    def __init__(self):
        self.weights = {"explore": 0.5, "exploit": 0.5}

    def update(self, action, reward):
        lr = 0.05
        self.weights[action] += lr * reward
        self.weights[action] = max(0.05, min(0.95, self.weights[action]))

    def decide(self):
        return "explore" if self.weights["explore"] > self.weights["exploit"] else "exploit"
