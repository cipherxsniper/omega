# 🧠 Omega v12.5 Cognition Competition System

import random
from collections import defaultdict


class CognitionCompetition:

    def __init__(self):

        # competing "thought agents"
        self.brains = {
            "alpha": {"bias": 0.5, "history": []},
            "beta": {"bias": 0.5, "history": []},
            "gamma": {"bias": 0.5, "history": []}
        }

        self.global_memory = []

    # -----------------------------------------
    # generate competing decisions
    # -----------------------------------------
    def propose(self, state):

        proposals = {}

        for name, brain in self.brains.items():

            noise = random.uniform(-0.05, 0.05)

            score = (
                state.get("attention", 0.3) * brain["bias"] +
                state.get("goal", 0.3) * (1 - brain["bias"]) +
                noise
            )

            proposals[name] = max(0.0, min(1.0, score))

        return proposals

    # -----------------------------------------
    # winner selection (competition collapse)
    # -----------------------------------------
    def select_winner(self, proposals):

        winner = max(proposals, key=proposals.get)

        return winner, proposals[winner]

    # -----------------------------------------
    # learning update (reinforcement drift)
    # -----------------------------------------
    def learn(self, winner, proposals):

        for name, score in proposals.items():

            brain = self.brains[name]

            brain["history"].append(score)

            if name == winner:
                brain["bias"] += 0.02
            else:
                brain["bias"] -= 0.01

            brain["bias"] = max(0.05, min(0.95, brain["bias"]))

    # -----------------------------------------
    # full cycle
    # -----------------------------------------
    def step(self, state):

        proposals = self.propose(state)
        winner, score = self.select_winner(proposals)
        self.learn(winner, proposals)

        self.global_memory.append({
            "winner": winner,
            "score": score,
            "proposals": proposals
        })

        self.global_memory = self.global_memory[-200:]

        return winner, proposals
