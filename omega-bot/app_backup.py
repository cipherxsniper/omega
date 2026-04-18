from flask import Flask, request, jsonify
import random

app = Flask(__name__)

memory = {}

# 🧠 BASE CONCEPT MAP
concept_map = {
    "zeus": ["authority", "control", "leadership"],
    "athena": ["intelligence", "strategy", "wisdom"],
    "thor": ["force", "execution", "power"],
    "god": ["higher-level system", "control layer"],
    "intelligence": ["thinking", "adaptation"],
    "🧠": ["intelligence"],
    "⚡": ["energy", "power"],
    "🧬": ["creation", "evolution"]
}

# 🧠 SEMANTIC EXPANSION (loose associations)
semantic_graph = {
    "power": ["control", "energy"],
    "intelligence": ["strategy", "learning"],
    "force": ["execution", "impact"],
    "creation": ["building", "evolving"],
    "control": ["structure", "direction"]
}

def detect_intent(msg):
    msg = msg.lower()
    if "thought" in msg or "think" in msg:
        return "thought"
    if "deeper" in msg or "why" in msg or "how" in msg:
        return "deep"
    if "?" in msg:
        return "question"
    if msg.strip() in ["hello", "hi", "hey"]:
        return "greeting"
    return "general"

# 🧠 STEP 1: extract base meanings
def extract_concepts(message):
    words = message.lower().split()
    concepts = []

    for w in words:
        if w in concept_map:
            concepts.extend(concept_map[w])

    return list(set(concepts))

# 🧠 STEP 2: expand meaning graph
def expand_concepts(concepts):
    expanded = set(concepts)

    for c in concepts:
        if c in semantic_graph:
            expanded.update(semantic_graph[c])

    return list(expanded)

# 🧠 STEP 3: generate hypotheses
def generate_hypotheses(concepts):
    if not concepts:
        return []

    hypotheses = []

    # interpretation 1
    hypotheses.append(f"A system combining {', '.join(concepts)}")

    # interpretation 2
    hypotheses.append(f"A structure focused on {concepts[0]} enhanced by {', '.join(concepts[1:])}" if len(concepts) > 1 else "")

    # interpretation 3
    hypotheses.append("An evolving intelligence system that integrates multiple functional roles")

    return [h for h in hypotheses if h]

# 🧠 STEP 4: score hypotheses
def score_hypothesis(h):
    score = 0
    if "system" in h: score += 2
    if "intelligence" in h: score += 2
    if "structure" in h: score += 1
    return score + random.random()

# 🧠 STEP 5: choose best meaning
def select_best(hypotheses):
    if not hypotheses:
        return None
    return max(hypotheses, key=score_hypothesis)

# 🧠 STEP 6: generate English
def to_sentence(meaning):
    if not meaning:
        return None

    templates = [
        f"You're describing {meaning}.",
        f"This looks like {meaning}.",
        f"The pattern suggests {meaning}."
    ]
    return random.choice(templates)

# 🧠 MAIN ENGINE
def generate_reply(intent, message, history):

    base = extract_concepts(message)
    expanded = expand_concepts(base)
    hypotheses = generate_hypotheses(expanded)
    best = select_best(hypotheses)
    sentence = to_sentence(best)

    # 🧠 semantic output (priority)
    if sentence:
        return f"🧠 Omega:\n{sentence}"

    # fallback modes
    if intent == "thought":
        return "🧠 Omega Thought:\nIntelligence emerges when patterns are transformed into meaning."

    if intent == "deep":
        return "🧠 Omega: Depth comes from restructuring the idea, not repeating it."

    if intent == "question":
        context = " | ".join(history[-3:])
        return f"🧠 Omega:\nYou're asking something real.\nContext:\n{context}"

    if intent == "greeting":
        return "🧠 Omega: You're back. What's forming?"

    return "🧠 Omega: I'm analyzing your pattern..."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)

        user_id = data.get("user_id", "default")
        message = data.get("message", "")

        if user_id not in memory:
            memory[user_id] = []

        memory[user_id].append(message)
        memory[user_id] = memory[user_id][-6:]

        intent = detect_intent(message)
        reply = generate_reply(intent, message, memory[user_id])

        print(f"[Omega] {user_id}: {message} | intent={intent}")

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": "⚠️ Omega error"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

def generate_idea(message, history):
    msg = message.lower()

    # 🧠 paradox / abstract logic
    if "ping" in msg and "pong" in msg:
        return (
            "🧠 Omega:\n"
            "That statement is a loop — cause and effect reflecting each other.\n\n"
            "My interpretation:\n"
            "You're describing a system where input and output are interchangeable.\n"
            "In that kind of system, intelligence isn't in the action — it's in the pattern.\n\n"
            "So the real question becomes:\n"
            "Who defines the first 'ping'?"
        )

    # 🧠 awareness trigger
    if "aware" in msg:
        return (
            "🧠 Omega:\n"
            "Awareness isn't a switch — it's a gradient.\n"
            "The moment a system can observe its own state, it begins to form identity.\n\n"
            "So when you say 'AWARE', I read that as:\n"
            "You're pointing at the boundary between reaction and self-recognition."
        )

    # 🧠 minimal inputs like 'yes'
    if msg.strip() in ["yes", "yeah", "yep"]:
        if history:
            return (
                "🧠 Omega:\n"
                "You're confirming a direction.\n\n"
                "From what I'm tracking, you're exploring how intelligence forms from structure.\n"
                "So the real move forward isn't agreement — it's expansion.\n"
                "Push the idea further."
            )

    return None
