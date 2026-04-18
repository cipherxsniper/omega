from flask import Flask, request, jsonify
import json
import os
import random
import time

app = Flask(__name__)

MEM_FILE = "omega_v20_memory.json"

# -----------------------------
# 🧠 MEMORY
# -----------------------------
def load():
    if os.path.exists(MEM_FILE):
        return json.load(open(MEM_FILE))
    return {"concepts": {}, "history": []}

memory = load()

def save():
    json.dump(memory, open(MEM_FILE, "w"), indent=2)

# -----------------------------
# 🧠 TOKENIZER
# -----------------------------
def tokenize(msg):
    import re
    msg = re.sub(r"[^a-zA-Z ]", " ", msg.lower())
    return [t for t in msg.split() if len(t) > 1]

# -----------------------------
# 🧠 MULTI-AGENT SYSTEM
# -----------------------------
def agent_A(tokens):
    return f"structural map: {tokens}"

def agent_B(tokens):
    if "zeus" in tokens:
        return "semantic link: authority ↔ intelligence"
    return "semantic drift detected"

def agent_C(tokens):
    if any(t in ["zeus","athena","thor"] for t in tokens):
        return "symbolic cluster: archetype system detected"
    return "symbolic noise present"

# -----------------------------
# 🧠 CONFLICT RESOLUTION
# -----------------------------
def resolve(a, b, c):

    votes = {
        "A": len(a),
        "B": len(b),
        "C": len(c)
    }

    # simple dominance logic (can evolve later)
    winner = max(votes, key=votes.get)

    return winner, votes

# -----------------------------
# 🧠 META REFLECTION ENGINE
# -----------------------------
def reflect(tokens, winner):

    reflections = [
        "Why did structural interpretation dominate semantic interpretation?",
        "What pattern caused symbolic clustering to activate?",
        "Is this mapping stable or context-dependent?",
        "What assumptions led to this classification?"
    ]

    return random.choice(reflections)

# -----------------------------
# 🧠 QUESTION ENGINE
# -----------------------------
def generate_question(tokens):

    if "zeus" in tokens:
        return "Why is authority being mapped to intelligence in this context?"

    if "athena" in tokens:
        return "What does intelligence represent in this system structure?"

    return "What underlying structure is emerging from these inputs?"

# -----------------------------
# 🧠 MAIN RESPONSE ENGINE
# -----------------------------
def respond(tokens):

    A = agent_A(tokens)
    B = agent_B(tokens)
    C = agent_C(tokens)

    winner, votes = resolve(A, B, C)

    reflection = reflect(tokens, winner)
    question = generate_question(tokens)

    memory["history"].append({
        "tokens": tokens,
        "winner": winner,
        "time": time.time()
    })

    save()

    return {
        "reply":
f"""🧠 Omega v20 Multi-Agent Cognition

A (Structure): {A}
B (Meaning): {B}
C (Symbolism): {C}

🏁 Consensus: {winner}
🗳️ Votes: {votes}

🧠 Reflection:
{reflection}

❓ System Question:
{question}
"""
    }

# -----------------------------
# API
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    msg = data.get("message", "")

    tokens = tokenize(msg)

    return jsonify(respond(tokens))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
