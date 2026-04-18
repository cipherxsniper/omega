import random

class PolicySimulator:
    def simulate(self, node, score):
        volatility = random.uniform(-0.2, 0.2)
        projected = score + volatility

        if projected > 0.8:
            return "HIGH_GAIN"
        elif projected > 0.5:
            return "STABLE"
        else:
            return "RISK"
