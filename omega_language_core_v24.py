import hashlib
import random
from collections import deque

memory = deque(maxlen=2000)

def h(x):
    return hashlib.sha256(x.encode()).hexdigest()

def novelty(x):
    return 0.0 if h(x) in memory else 1.0

def speak(metrics, context="omega"):
    signal = metrics.get("signal", 0)
    reward = metrics.get("reward", 0)
    state = metrics.get("state", "unknown")

    if signal == 0 and reward == 0:
        tone = "inactive sensing mode"
    elif signal > 0.75:
        tone = "high adaptive motion"
    elif signal > 0.4:
        tone = "moderate learning drift"
    else:
        tone = "low exploratory stabilization"

    templates = [
        f"[{context}] signal={signal:.3f}, reward={reward:.3f}, state={state} in {tone}.",
        f"[{context}] system transitions through {tone} with causal continuity.",
        f"[{context}] observed behavior reflects {tone} across active nodes.",
        f"[{context}] memory-weighted interpretation confirms {state} phase."
    ]

    scored = [(novelty(t), t) for t in templates]
    scored.sort(reverse=True, key=lambda x: x[0])

    pool = [t for s, t in scored if s > 0]

    if not pool:
        pool = [t for _, t in scored]

    chosen = random.choice(pool)
    memory.append(h(chosen))

    return chosen
