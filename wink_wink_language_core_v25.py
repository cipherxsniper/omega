import random
from wink_wink_persistent_memory_v1 import novelty, update_memory

def generate_sentence(metrics):
    signal = metrics.get("signal", 0)
    reward = metrics.get("reward", 0)
    state = metrics.get("state", "unknown")

    tone = (
        "high adaptation drift" if signal > 0.7 else
        "moderate learning flow" if signal > 0.4 else
        "stable observation mode"
    )

    templates = [
        f"System operates in {tone}, signal={signal:.3f}, reward={reward:.3f}.",
        f"Causal evaluation indicates {state} with adaptive continuity.",
        f"Behavioral drift detected under {tone}.",
        f"Memory-aligned interpretation confirms ongoing system transition."
    ]

    scored = [(novelty(t), t) for t in templates]
    scored.sort(reverse=True, key=lambda x: x[0])

    pool = [t for s, t in scored if s > 0]

    if not pool:
        pool = templates

    chosen = random.choice(pool)

    update_memory(chosen, reward)

    return chosen
