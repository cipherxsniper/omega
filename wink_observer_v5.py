import random

verbs = ["analyzing", "compressing", "balancing", "synchronizing", "evaluating", "mapping"]
reasons = ["signal drift", "instability rise", "curiosity expansion", "focus fragmentation", "node variance"]

def generate_observation(nodes, avg_signal, instability):
    verb = random.choice(verbs)
    reason = random.choice(reasons)

    summary = (
        f"The system is {verb} internal state across {len(nodes)} nodes. "
        f"Signal behavior indicates {reason}. "
        f"Curiosity drives exploration, focus provides directional stability, and instability introduces randomness. "
        f"The system is currently {'self-correcting' if instability < 0.5 else 'stabilizing'} toward coherence."
    )

    return summary
