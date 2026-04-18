import random

class QuantumSim:

    def superposition(self, options):
        return random.sample(options, k=min(2, len(options)))

    def collapse(self, options):
        return random.choice(options)
