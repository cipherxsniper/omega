import time

# -----------------------------
# 🧠 AGENT PERSONALITY STATE
# -----------------------------
class AgentProfile:
    def __init__(self, name, base_prompt):
        self.name = name
        self.base_prompt = base_prompt
        self.evolution_score = 1.0
        self.style_bias = 0.0

    def evolve(self, success_signal):
        # safe bounded self-modification
        if success_signal:
            self.evolution_score += 0.03
            self.style_bias += 0.02
        else:
            self.evolution_score -= 0.02
            self.style_bias -= 0.01

        # clamp values (CRITICAL SAFETY)
        self.evolution_score = max(0.5, min(2.0, self.evolution_score))
        self.style_bias = max(-1.0, min(1.0, self.style_bias))

    def dynamic_prompt(self):
        return f"""
{self.base_prompt}

Evolution Score: {self.evolution_score:.2f}
Style Bias: {self.style_bias:.2f}

Adjust reasoning accordingly but remain consistent.
"""


# -----------------------------
# 🧠 META JUDGE (agent evaluator)
# -----------------------------
class MetaJudge:
    def score(self, response):
        # lightweight heuristic scoring (no external calls needed)
        score = 0

        if len(response) > 50:
            score += 1
        if "I think" in response:
            score += 1
        if "because" in response:
            score += 1

        return score >= 2


# -----------------------------
# 🧠 BELIEF GRAPH MEMORY
# -----------------------------
class BeliefGraph:
    def __init__(self):
        self.nodes = {}

    def update(self, msg, winner):
        if msg not in self.nodes:
            self.nodes[msg] = {"A": 0, "B": 0, "C": 0}

        self.nodes[msg][winner] += 1

    def summary(self):
        return str({k: v for k, v in list(self.nodes.items())[-5:]})
