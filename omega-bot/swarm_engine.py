import json
import time

# -----------------------------
# 🧠 MEMORY COMPRESSION LAYER
# -----------------------------
class MemoryCore:
    def __init__(self):
        self.memory = []

    def add(self, user, message, reply):
        self.memory.append({
            "u": user,
            "m": message,
            "r": reply,
            "t": time.time()
        })

        # keep memory compact (last 25 only)
        if len(self.memory) > 25:
            self.memory = self.memory[-25:]

    def summary(self):
        if not self.memory:
            return "No memory yet."

        # compress into meaning, not logs
        topics = {}
        for item in self.memory:
            key = item["m"].lower()
            topics[key] = topics.get(key, 0) + 1

        return " | ".join([f"{k}:{v}" for k, v in topics.items()])


# -----------------------------
# 🧠 SWARM AGENTS
# -----------------------------
class AgentA:
    def think(self, msg):
        return f"Intent-focused interpretation: user wants {msg}"

class AgentB:
    def think(self, msg):
        return f"Emotional-context: user emotion around '{msg}' is curiosity/engagement"

class AgentC:
    def think(self, msg):
        return f"Structural parsing: message structure = {len(msg)} chars, tokens simplified"


# -----------------------------
# 🧠 DEBATE ENGINE
# -----------------------------
class Swarm:
    def __init__(self):
        self.A = AgentA()
        self.B = AgentB()
        self.C = AgentC()
        self.memory = MemoryCore()

    def run(self, user, msg):

        a = self.A.think(msg)
        b = self.B.think(msg)
        c = self.C.think(msg)

        # simple scoring system (NOT random chaos)
        scores = {
            "A": len(msg.split()) * 0.8,
            "B": len(msg) * 0.05,
            "C": len(msg) * 0.3
        }

        winner = max(scores, key=scores.get)

        consensus_map = {
            "A": "Intent-driven response prioritized",
            "B": "Emotion-driven response prioritized",
            "C": "Structure-driven response prioritized"
        }

        reflection = f"Omega compresses meaning: {msg} → {consensus_map[winner]}"

        reply = f"""🧠 SWARM DEBATE
A: {a}
B: {b}
C: {c}

🏁 CONSENSUS:
{winner}: {consensus_map[winner]}

🧠 REFLECTION LAYER
{reflection}

📦 MEMORY SUMMARY
{self.memory.summary()}
"""

        self.memory.add(user, msg, reply)
        return reply
