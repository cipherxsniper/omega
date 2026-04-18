import requests
import time

BRAIN_URL = "http://127.0.0.1:5000/chat"


# -----------------------------
# 🧠 BELIEF MEMORY CORE
# -----------------------------
class BeliefMemory:
    def __init__(self):
        self.history = []
        self.beliefs = {
            "intent_weight": 1.0,
            "emotion_weight": 1.0,
            "structure_weight": 1.0
        }

    def update(self, msg, winner):
        self.history.append((msg, winner))

        if len(self.history) > 40:
            self.history = self.history[-40:]

        # reinforcement learning style update (safe + bounded)
        if winner == "A":
            self.beliefs["intent_weight"] += 0.02
        elif winner == "B":
            self.beliefs["emotion_weight"] += 0.02
        elif winner == "C":
            self.beliefs["structure_weight"] += 0.02

        # normalize
        total = sum(self.beliefs.values())
        for k in self.beliefs:
            self.beliefs[k] /= total

    def compress(self):
        if not self.history:
            return "empty"

        summary = {}
        for _, w in self.history:
            summary[w] = summary.get(w, 0) + 1

        return " | ".join([f"{k}:{v}" for k, v in summary.items()])


# -----------------------------
# 🧠 AGENT
# -----------------------------
class Agent:
    def __init__(self, role):
        self.role = role

    def think(self, msg):
        prompt = f"""
Omega Agent Role: {self.role}

User message:
{msg}

Respond briefly (1–2 sentences).
Be distinct from other agents.
"""

        try:
            r = requests.post(BRAIN_URL, json={
                "user_id": "agent",
                "message": prompt
            }, timeout=15)

            return r.json().get("reply", "")
        except:
            return f"[fallback {self.role}] {msg}"


# -----------------------------
# 🧠 JUDGE
# -----------------------------
class Judge:
    def decide(self, a, b, c, msg):
        prompt = f"""
You are Omega Judge.

Choose best response.

A: {a}
B: {b}
C: {c}

Return ONLY A, B, or C.
"""

        try:
            r = requests.post(BRAIN_URL, json={
                "user_id": "judge",
                "message": prompt
            }, timeout=15)

            out = r.json().get("reply", "B").strip()

            if "A" in out:
                return "A"
            if "C" in out:
                return "C"
            return "B"

        except:
            return "B"


# -----------------------------
# 🧠 RECURSIVE REFLECTION (1 PASS ONLY)
# -----------------------------
class Reflector:
    def reflect(self, msg, winner, answer):
        prompt = f"""
You are Omega Reflection Layer.

Input: {msg}
Chosen answer: {answer}

Explain WHY this answer fits best in 1 sentence.
"""

        try:
            r = requests.post(BRAIN_URL, json={
                "user_id": "reflector",
                "message": prompt
            }, timeout=15)

            return r.json().get("reply", "")
        except:
            return "reflection unavailable"


# -----------------------------
# 🧠 SWARM V7 CORE
# -----------------------------
class SwarmV7:
    def __init__(self):
        self.A = Agent("intent reasoning")
        self.B = Agent("emotional reasoning")
        self.C = Agent("structural reasoning")

        self.judge = Judge()
        self.memory = BeliefMemory()
        self.reflector = Reflector()

    def run(self, user, msg):

        # 1. parallel thinking
        a = self.A.think(msg)
        b = self.B.think(msg)
        c = self.C.think(msg)

        # 2. decision
        winner = self.judge.decide(a, b, c, msg)
        chosen = {"A": a, "B": b, "C": c}[winner]

        # 3. reflection (ONLY ONCE → prevents recursion explosion)
        reflection = self.reflector.reflect(msg, winner, chosen)

        # 4. memory update
        self.memory.update(msg, winner)

        # 5. output
        return f"""
🧠 SWARM v7 RECURSIVE LOOP

A: {a}
B: {b}
C: {c}

🏁 WINNER: {winner}

🧠 FINAL:
{chosen}

🧠 REFLECTION:
{reflection}

📦 BELIEF STATE:
{self.memory.beliefs}

📊 MEMORY:
{self.memory.compress()}
"""
