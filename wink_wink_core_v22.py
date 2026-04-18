# 🧠 WINK_WINK CORE v22 — shared memory + sentence intelligence

import hashlib
import random
from collections import deque

# ----------------------------
# GLOBAL MEMORY (shared across versions)
# ----------------------------

_sentence_memory = deque(maxlen=500)
_state_memory = deque(maxlen=200)
_reward_memory = deque(maxlen=200)

# ----------------------------
# UTILITIES
# ----------------------------

def hash_text(t):
    return hashlib.md5(t.encode()).hexdigest()

def remember_sentence(sentence):
    _sentence_memory.append(hash_text(sentence))

def seen_before(sentence):
    return hash_text(sentence) in _sentence_memory

def remember_state(state, reward):
    _state_memory.append(state)
    _reward_memory.append(reward)

# ----------------------------
# NOVELTY ENGINE
# ----------------------------

def novelty(sentence):
    return 0.0 if seen_before(sentence) else 1.0

# ----------------------------
# SENTENCE ENGINE (ANTI-REPEAT + STATE DRIVEN)
# ----------------------------

def generate_thought(data):
    added = data.get("added", 0)
    removed = data.get("removed", 0)
    modified = data.get("modified", 0)
    signal = data.get("signal", 0.5)
    reward = data.get("reward", 0.5)
    state = data.get("state", "unknown")

    templates = [
        "System observes structural change: {a} added, {r} removed, {m} modified under signal {s}.",
        "Causal mesh evaluation indicates state {state} with reward stability {rw}.",
        "Adaptive system processing signal {s} with evolving structural feedback loops.",
        "Memory-driven inference detects transition behavior in state {state}.",
        "Graph intelligence aligns execution flow under reward pressure {rw}."
    ]

    best = []

    for t in templates:
        sentence = t.format(
            a=added,
            r=removed,
            m=modified,
            s=round(signal, 4),
            state=state,
            rw=round(reward, 4)
        )

        score = novelty(sentence)
        best.append((score, sentence))

    best.sort(reverse=True, key=lambda x: x[0])

    pool = [s for score, s in best if score > 0]

    if not pool:
        pool = [s for _, s in best]

    chosen = random.choice(pool)

    remember_sentence(chosen)
    return chosen

# ----------------------------
# PUBLIC API
# ----------------------------

def core_think(data):
    remember_state(data.get("state", None), data.get("reward", 0))
    return generate_thought(data)
