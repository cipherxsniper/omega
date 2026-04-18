from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import random
import time
from collections import deque

# =========================
# 🧠 EXPANDED SEMANTIC SPACE
# =========================

SEMANTIC_STATES = [
    "causal drift analysis",
    "temporal stability compression",
    "predictive divergence mapping",
    "memory reinforcement cycling",
    "entropy stabilization field",
    "structural recursion detection",
    "attention convergence flow",
    "behavioral trajectory shift",
    "latent pattern emergence",
    "adaptive coherence formation",
    "signal harmonization phase",
    "multi-node influence resonance",
    "recursive feedback balancing",
    "uncertainty resolution sweep",
    "probabilistic alignment update"
]

# =========================
# 🧠 TRAJECTORY MEMORY
# =========================

recent_states = deque(maxlen=10)

# =========================
# 🧠 NOVELTY SCORING
# =========================

def novelty(state):
    if state in recent_states:
        return 0.1
    return 1.0

# =========================
# 🧠 STATE SELECTOR (NO REPETITION)
# =========================

def select_state():
    candidates = []

    for s in SEMANTIC_STATES:
        score = novelty(s) + random.uniform(0.0, 0.2)
        candidates.append((score, s))

    candidates.sort(reverse=True)
    chosen = candidates[0][1]

    recent_states.append(chosen)
    return chosen

# =========================
# 🧠 SENTENCE GENERATOR (CLEAN OUTPUT)
# =========================

def generate_sentence():
    state = select_state()

    templates = [
        "System transitions through {state}, maintaining adaptive continuity.",
        "Causal mesh activates {state}, producing structured evolution.",
        "Observed dynamics indicate {state} across active memory layers.",
        "Processing cycle enters {state} with stabilized feedback loops."
    ]

    sentence = random.choice(templates).format(state=state)

    return sentence

# =========================
# 🧠 RUN LOOP
# =========================

NODE_ID = "wink_wink_brain_v6_1_patch.py" 
register(NODE_ID)

while True:
    def anti_loop(msg, hist):
        return msg not in hist[-10:]

    history = []
    recent = fetch_recent(5)
    if recent:
        influence = sum(m["signal"] for m in recent) / len(recent)
        try:
            signal = (signal + influence) / 2
        except:
            pass
    publish(NODE_ID, generate_sentence())
    time.sleep(1)
