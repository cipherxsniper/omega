import os
import time
import requests

# -----------------------------
# CONFIG (no API key required if you use local fallback brain)
# -----------------------------
BRAIN_URL = "http://127.0.0.1:5000/chat"

# -----------------------------
# 🧠 MEMORY WITH WEIGHT EVOLUTION
# -----------------------------
class MemoryCore:
    def __init__(self):
        self.log = []
        self.weights = {"A": 1.0, "B": 1.0, "C": 1.0}

    def add(self, msg, winner):
        self.log.append({"msg": msg, "winner": winner})

        if len(self.log) > 30:
            self.log = self.log[-30:]

        # evolution: reinforce winner
        self.weights[winner] += 0.05

        # normalize
        total = sum(self.weights.values())
        for k in self.weights:
            self.weights[k] /= total

    def summary(self):
        return f"Weights: {self.weights}"


# -----------------------------
# 🧠 LLM AGENTS
# -----------------------------
class Agent:
    def __init__(self, style):
        self.style = style

    def think(self, msg):
        prompt = f"""
You are Omega Agent with style: {self.style}

User message: {msg}

Respond in 1–2 sentences only.
Focus ONLY on your perspective.
"""

        try:
            r = requests.post(BRAIN_URL, json={
                "user_id": "agent",
                "message": prompt
            }, timeout=10)

            return r.json().get("reply", "no response")
        except:
            return f"[{self.style}] fallback response"


# -----------------------------
# 🧠 SWARM ORCHESTRATOR
# -----------------------------
class SwarmV5:
    def __init__(self):
        self.A = Agent("intent reasoning (logical decision maker)")
        self.B = Agent("emotional reasoning (human context understanding)")
        self.C = Agent("structural reasoning (language + syntax analyzer)")
        self.memory = MemoryCore()

    def score(self, text):
        # simple heuristic scoring (can later be LLM judge)
        return len(text.split()) + (0.1 * len(text))

    def run(self, user, msg):

        a = self.A.think(msg)
        b = self.B.think(msg)
        c = self.C.think(msg)

        scores = {
            "A": self.score(a) * self.memory.weights["A"],
            "B": self.score(b) * self.memory.weights["B"],
            "C": self.score(c) * self.memory.weights["C"]
        }

        winner = max(scores, key=scores.get)

        responses = {"A": a, "B": b, "C": c}

        reply = f"""
🧠 SWARM v5 DEBATE

A (Intent):
{a}

B (Emotion):
{b}

C (Structure):
{c}

🏁 WINNER: {winner}

🧠 FINAL RESPONSE:
{responses[winner]}

📊 EVOLUTION STATE:
{self.memory.summary()}
"""

        self.memory.add(msg, winner)

        return reply
