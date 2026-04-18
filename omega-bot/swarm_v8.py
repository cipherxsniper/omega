import requests
from meta_core_v8 import AgentProfile, MetaJudge, BeliefGraph

BRAIN_URL = "http://127.0.0.1:5000/chat"


# -----------------------------
# 🧠 AGENTS (SELF-MODIFYING PROMPTS)
# -----------------------------
class SwarmV8:
    def __init__(self):
        self.A = AgentProfile("A", "Intent reasoning agent (logical decision maker)")
        self.B = AgentProfile("B", "Emotional reasoning agent (human context)")
        self.C = AgentProfile("C", "Structural reasoning agent (language analysis)")

        self.judge = MetaJudge()
        self.graph = BeliefGraph()

    def think(self, profile, msg):
        prompt = profile.dynamic_prompt() + f"\nUser: {msg}"

        try:
            r = requests.post(BRAIN_URL, json={
                "user_id": profile.name,
                "message": prompt
            }, timeout=15)

            return r.json().get("reply", "")
        except:
            return f"[fallback {profile.name}] {msg}"

    def run(self, user, msg):

        a = self.think(self.A, msg)
        b = self.think(self.B, msg)
        c = self.think(self.C, msg)

        # 🧠 META EVALUATION (SELF-MODIFICATION SIGNAL)
        score_a = self.judge.score(a)
        score_b = self.judge.score(b)
        score_c = self.judge.score(c)

        scores = {"A": score_a, "B": score_b, "C": score_c}
        winner = max(scores, key=scores.get)

        chosen = {"A": a, "B": b, "C": c}[winner]

        # -----------------------------
        # 🧠 EVOLUTION SIGNAL
        # -----------------------------
        self.A.evolve(winner == "A")
        self.B.evolve(winner == "B")
        self.C.evolve(winner == "C")

        self.graph.update(msg, winner)

        return f"""
🧠 OMEGA v8 SELF-MODIFYING SYSTEM

A:
{a}

B:
{b}

C:
{c}

🏁 WINNER: {winner}

🧠 FINAL OUTPUT:
{chosen}

📊 EVOLUTION STATE:
A: {self.A.evolution_score:.2f}
B: {self.B.evolution_score:.2f}
C: {self.C.evolution_score:.2f}

🧠 BELIEF GRAPH:
{self.graph.summary()}
"""
