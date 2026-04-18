from core.omega_brain_base import OmegaBrain

class OmegaSwarm:
    def __init__(self, size=10):
        self.brains = [OmegaBrain(i) for i in range(size)]

    def step(self, events):
        results = []
        for brain in self.brains:
            results.append(brain.update(events))
        return results

    def global_state(self):
        return self.brains[0].get_state()
