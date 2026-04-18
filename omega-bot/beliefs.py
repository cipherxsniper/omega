import json

beliefs = {
    "self": "Omega is a multi-agent reasoning system",
    "goal": "understand user intent and generate structured insight",
    "confidence": 0.5
}

def update_belief(key, value, confidence=0.5):
    beliefs[key] = value
    beliefs["confidence"] = (beliefs.get("confidence", 0.5) + confidence) / 2

def get_beliefs():
    return beliefs
