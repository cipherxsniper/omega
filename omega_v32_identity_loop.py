from omega_v32_identity_core import update_trait
from omega_v32_belief_engine import load

def evolve_identity():
    data = load()

    for belief, meta in data["beliefs"].items():
        if meta["weight"] > 5:
            update_trait(f"strong-belief:{belief}", meta["weight"] * 0.1)

    return "🧠 Identity updated from belief graph"
