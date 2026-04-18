
class PersonalityEvolution:

    def __init__(self, identity_core):
        self.identity = identity_core
        self.traits = {
            "tone": "neutral",
            "depth": "medium",
            "question_rate": 0.5
        }

    def evolve(self):

        v = self.identity.get_identity()

        # curiosity increases questioning behavior
        if v["curiosity"] > 0.7:
            self.traits["question_rate"] = 0.9
            self.traits["tone"] = "inquisitive"

        # instability increases reflective tone
        if v["coherence"] < 0.4:
            self.traits["tone"] = "reflective"

        # high stability = confident responses
        if v["stability"] > 0.7:
            self.traits["tone"] = "confident"

        return self.traits
