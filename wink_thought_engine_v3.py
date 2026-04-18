import random

subjects = [
    "Omega system", "distributed mesh", "signal layer",
    "memory network", "node cluster", "adaptive core"
]

verbs = [
    "observes", "stabilizes", "reconstructs",
    "interprets", "synchronizes", "compresses"
]

concepts = [
    "coherence", "entropy", "pattern drift",
    "signal flow", "recursive memory", "system alignment"
]

def generate_thought(state, signal):
    s = random.choice(subjects)
    v = random.choice(verbs)
    c = random.choice(concepts)

    if signal > 0.65:
        mood = "VISIONARY CLARITY"
    elif signal > 0.5:
        mood = "STABLE AWARENESS"
    elif signal > 0.35:
        mood = "EXPLORING UNCERTAINTY"
    else:
        mood = "FRAGMENTED SIGNAL FIELD"

    sentence = f"I observe {s} as it {v} evolving {c}."

    return mood, sentence
