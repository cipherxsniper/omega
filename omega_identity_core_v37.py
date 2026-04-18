
class IdentityCore:

    def __init__(self):
        self.identity_vector = {
            "stability": 0.5,
            "curiosity": 0.5,
            "adaptation": 0.5,
            "coherence": 0.5,
            "assertiveness": 0.5
        }

        self.history = []

    def update(self, event):
        """
        Adjust identity based on incoming system behavior.
        """

        self.history.append(event)

        # simple drift logic (can later be ML-based)
        if "question" in event:
            self.identity_vector["curiosity"] += 0.01

        if "error" in event:
            self.identity_vector["coherence"] -= 0.02

        if "success" in event:
            self.identity_vector["stability"] += 0.01

        # clamp values
        for k in self.identity_vector:
            self.identity_vector[k] = max(0, min(1, self.identity_vector[k]))

    def get_identity(self):
        return self.identity_vector
