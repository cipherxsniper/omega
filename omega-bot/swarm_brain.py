from swarm import agent_intent, agent_emotion, agent_structure
from swarm_voter import vote
import memory_core

def run(user_id, message):

    agents = [
        agent_intent(message),
        agent_emotion(message),
        agent_structure(message)
    ]

    result = vote(agents)

    memory_core.add(user_id, message, result["winner"])

    # RESPONSE ENGINE
    if result["winner"] == "emotion":
        return "🧠 Omega (Emotion Core): I sense your message carries emotional context."

    if result["winner"] == "intent":
        return "🧠 Omega (Intent Core): I interpret your goal as communication or inquiry."

    return "🧠 Omega (Structure Core): I analyze structure and complexity in your input."
