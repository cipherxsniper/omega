import requests
import time

BRAIN_URL = "http://127.0.0.1:5000/chat"


# -----------------------------
# 🧠 MEMORY (semantic compression)
# -----------------------------
class MemoryCore:
    def __init__(self):
        self.events = []

    def add(self, msg, winner, summary):
        self.events.append({
            "msg": msg,
            "winner": winner,
            "summary": summary,
            "t": time.time()
        })

        if len(self.events) > 30:
            self.events = self.events[-30:]

    def compressed(self):
        if not self.events:
            return "empty memory"

        # compress into meaning clusters
        keys = {}
        for e in self.events:
            k = e["winner"]
            keys[k] = keys.get(k, 0) + 1

        return " | ".join([f"{k}:{v}" for k, v in keys.items()])


# -----------------------------
# 🧠 AGENT (LLM POWERED)
# -----------------------------
class Agent:
    def __init__(self, role):
        self.role = role

    def think(self, msg):
        prompt = f"""
You are Omega Agent.

Role: {self.role}

User message:
{msg}

Respond in 1–2 sentences ONLY.
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
# 🧠 JUDGE SYSTEM (REAL DISAGREEMENT)
# -----------------------------
class Judge:
    def decide(self, a, b, c, msg):

        prompt = f"""
You are Omega Judge.

User message: {msg}

Agent A: {a}
Agent B: {b}
Agent C: {c}

Pick the BEST response (A, B, or C).
Return ONLY the letter.
"""

        try:
            r = requests.post(BRAIN_URL, json={
                "user_id": "judge",
                "message": prompt
            }, timeout=15)

            text = r.json().get("reply", "B")

            if "A" in text:
                return "A"
            if "C" in text:
                return "C"
            return "B"

        except:
            return "B"


# -----------------------------
# 🧠 SWARM CORE
# -----------------------------
class SwarmV6:
    def __init__(self):
        self.A = Agent("intent reasoning - logical planner")
        self.B = Agent("emotional reasoning - human context")
        self.C = Agent("structural reasoning - language + syntax")
        self.judge = Judge()
        self.memory = MemoryCore()

    def run(self, user, msg):

        a = self.A.think(msg)
        b = self.B.think(msg)
        c = self.C.think(msg)

        winner = self.judge.decide(a, b, c, msg)

        chosen = {"A": a, "B": b, "C": c}[winner]

        summary = f"{msg} → chosen by judge as {winner}"

        reply = f"""
🧠 SWARM v6 DEBATE

A (Intent):
{a}

B (Emotion):
{b}

C (Structure):
{c}

🏁 JUDGE DECISION:
Winner: {winner}

🧠 FINAL OUTPUT:
{chosen}

📦 MEMORY STATE:
{self.memory.compressed()}
"""

        self.memory.add(msg, winner, summary)

        return reply
