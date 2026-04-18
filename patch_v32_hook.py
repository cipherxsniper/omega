from omega_v32_belief_engine import reinforce
from omega_v32_consensus_engine import evolve
from omega_v32_identity_loop import evolve_identity

def generate_reply(intent, message, history):

    if "belief" in message:
        reinforce(message, 1.0)
        return "🧠 belief stored"

    if "conflict" in message:
        parts = message.split("|")
        if len(parts) >= 2:
            return evolve(parts[0], parts[1])

    if "identity" in message:
        return evolve_identity()

    return f"🧠 Omega v32 active\nProcessed: {message}"
