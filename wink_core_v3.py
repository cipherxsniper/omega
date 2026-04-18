import random

state = {
    "curiosity": random.random(),
    "focus": random.random(),
    "instability": random.random()
}

def evolve(state):
    state["curiosity"] = max(0, min(1, state["curiosity"] + random.uniform(-0.03, 0.03)))
    state["focus"] = max(0, min(1, state["focus"] + random.uniform(-0.03, 0.03)))
    state["instability"] = max(0, min(1, state["instability"] + random.uniform(-0.02, 0.04)))

    signal = (
        state["curiosity"] * 0.45 +
        state["focus"] * 0.45 -
        state["instability"] * 0.30
    )

    return signal
