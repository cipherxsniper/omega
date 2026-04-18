from omega_v32_belief_engine import reinforce
from omega_v32_contradiction_engine import detect_conflict

def evolve(belief_a, belief_b):
    conflict = detect_conflict(belief_a, belief_b)

    if conflict["conflict"]:
        reinforce(belief_a, 0.2)
        reinforce(belief_b, 0.2)
        return "⚠️ Conflict balanced, weights adjusted"

    merged = belief_a + " + " + belief_b
    reinforce(merged, 1.0)

    return f"🧠 New belief formed: {merged}"
