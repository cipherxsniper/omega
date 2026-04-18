def agent_intent(msg):
    return {
        "name": "intent_agent",
        "signal": "intent",
        "output": f"User intent likely: {msg.lower()}"
    }

def agent_emotion(msg):
    tone = "neutral"

    if any(w in msg.lower() for w in ["help", "why", "confused", "?", "what"]):
        tone = "seeking clarity"
    if any(w in msg.lower() for w in ["hello", "hi"]):
        tone = "greeting"

    return {
        "name": "emotion_agent",
        "signal": "emotion",
        "output": f"Emotional context: {tone}"
    }

def agent_structure(msg):
    words = len(msg.split())

    return {
        "name": "structure_agent",
        "signal": "structure",
        "output": f"Structural complexity: {words} tokens"
    }
