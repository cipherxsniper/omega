import random

class EvolutionEngine:

    def mutate(self, brain):

        if random.random() < 0.3:
            brain.weight += random.uniform(-0.1, 0.1)

        if random.random() < 0.3:
            brain.specialization += random.uniform(-0.1, 0.1)

        brain.weight = max(0.01, min(1.0, brain.weight))
        brain.specialization = max(0.01, min(1.0, brain.specialization))

    def selection_pressure(self, brains):

        # keep top performers
        sorted_b = sorted(brains, key=lambda b: b.energy, reverse=True)

        return sorted_b[:max(2, len(brains)//2)]
