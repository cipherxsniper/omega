import random

class ConsensusEngine:

    def __init__(self):
        self.votes = {}

    def vote(self, agent, proposal):

        if proposal not in self.votes:
            self.votes[proposal] = {"A": 0, "B": 0, "C": 0}

        choice = random.choice(["A", "B", "C"])
        self.votes[proposal][choice] += 1

    def decide(self, proposal):

        v = self.votes.get(proposal, {})

        if not v:
            return "NO_DECISION"

        winner = max(v, key=v.get)

        return {
            "winner": winner,
            "votes": v
        }
