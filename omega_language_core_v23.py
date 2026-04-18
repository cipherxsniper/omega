import hashlib
import json
import random
from collections import deque

memory = deque(maxlen=5000)

def h(x):
    return hashlib.sha256(x.encode()).hexdigest()

def novelty(x):
    return 0.0 if h(x) in memory else 1.0

def speak(metrics, context="omega"):
    signal = metrics.get("signal", 0)
    reward = metrics.get("reward", 0)
    state = metrics.get("state", "unknown")

    tone = (
        "high volatility adaptation"
        if signal > 0.8 else
        "active learning drift"
        if signal > 0.5 else
        "stable observational mode"
    )

    templates = [
        f"[{context}] system reports signal={signal:.3f}, reward={reward:.3f} under {tone}.",
        f"[{context}] causal evaluation indicates {state} with emergent behavioral drift.",
        f"[{context}] structured interpretation: system operating in {tone} phase.",
        f"[{context}] memory-weighted analysis suggests continuity across recent state transitions."
    ]

    scored = [(novelty(t), t) for t in templates]
    scored.sort(reverse=True, key=lambda x: x[0])

    pool = [t for s, t in scored if s > 0]
    if not pool:
        pool = [t for _, t in scored]

    chosen = random.choice(pool)
    memory.append(h(chosen))

    return chosen
