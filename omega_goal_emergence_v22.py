import time
import random
import math
from collections import defaultdict, Counter

class OmegaGoalEmergenceV22:
    def __init__(self):
        self.history = []
        self.goals = []
        self.goal_weights = defaultdict(float)
        self.step = 0

    # --------------------------
    # MEMORY INGESTION
    # --------------------------
    def ingest(self, state):
        self.history.append({
            "step": self.step,
            "state": state,
            "ts": time.time()
        })

        if len(self.history) > 300:
            self.history = self.history[-300:]

    # --------------------------
    # PATTERN DETECTION
    # --------------------------
    def detect_patterns(self):
        if len(self.history) < 10:
            return []

        top_chain = [h["state"]["top"] for h in self.history[-20:]]

        freq = Counter(top_chain)

        patterns = []

        # dominance lock detection
        most_common = freq.most_common(1)[0]
        if most_common[1] > 12:
            patterns.append("dominance_lock_" + most_common[0])

        # oscillation detection
        if len(set(top_chain[-6:])) >= 3:
            patterns.append("high_oscillation")

        # stagnation detection
        scores = self.history[-1]["state"]["scores"]
        variance = max(scores.values()) - min(scores.values())
        if variance < 0.02:
            patterns.append("stagnation_state")

        return patterns

    # --------------------------
    # GOAL GENERATION
    # --------------------------
    def generate_goals(self, patterns):
        new_goals = []

        for p in patterns:
            if p.startswith("dominance_lock"):
                new_goals.append("increase_exploration")

            elif p == "high_oscillation":
                new_goals.append("stabilize_convergence")

            elif p == "stagnation_state":
                new_goals.append("increase_diversity")

        return list(set(new_goals))

    # --------------------------
    # GOAL WEIGHTING
    # --------------------------
    def prioritize(self, goals):
        for g in goals:
            self.goal_weights[g] += 1.0

        # decay old goals
        for k in list(self.goal_weights.keys()):
            self.goal_weights[k] *= 0.97
            if self.goal_weights[k] < 0.05:
                del self.goal_weights[k]

        ranked = sorted(self.goal_weights.items(), key=lambda x: x[1], reverse=True)

        return ranked

    # --------------------------
    # MAIN LOOP
    # --------------------------
    def step_cycle(self, state):
        self.step += 1

        self.ingest(state)

        patterns = self.detect_patterns()
        goals = self.generate_goals(patterns)
        ranked_goals = self.prioritize(goals)

        return {
            "step": self.step,
            "patterns": patterns,
            "active_goals": goals,
            "ranked_goals": ranked_goals[:5]
        }
