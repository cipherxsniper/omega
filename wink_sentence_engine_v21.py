from collections import deque
import hashlib
import random

sentence_memory = deque(maxlen=50)

def hash_sentence(s):
    return hashlib.md5(s.encode()).hexdigest()

def novelty_score(sentence):
    h = hash_sentence(sentence)
    if h in sentence_memory:
        return 0.0
    return 1.0

def generate_sentence(added, removed, modified, evo, state):

    base_templates = [
        "The system observes {a} additions, {r} removals, and {m} modifications shaping structural evolution.",
        "Causal mesh registers {e} evolution signal indicating {state} system dynamics.",
        "File topology shift detected: {a} added, {m} modified, suggesting directional drift.",
        "Omega interprets current state as {state}, driven by evolution intensity {e}.",
        "Structural inference: system activity reflects {state} behavior across distributed mesh."
    ]

    if evo > 100:
        tone = "highly volatile transition phase"
    elif evo > 10:
        tone = "active adaptive restructuring"
    elif evo > 0:
        tone = "low-level structural drift"
    else:
        tone = "stable equilibrium with no observed change"

    candidates = []

    for t in base_templates:
        s = t.format(
            a=len(added),
            r=len(removed),
            m=len(modified),
            e=round(evo, 3),
            state=tone
        )

        score = novelty_score(s)
        candidates.append((score, s))

    candidates.sort(reverse=True, key=lambda x: x[0])

    best_pool = [c[1] for c in candidates if c[0] > 0]

    if not best_pool:
        best_pool = [c[1] for c in candidates]

    chosen = random.choice(best_pool)

    sentence_memory.append(hash_sentence(chosen))

    return chosen
