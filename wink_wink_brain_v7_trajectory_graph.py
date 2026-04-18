from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import random
import time
from collections import defaultdict, deque

# =========================
# 🧠 TRAJECTORY GRAPH MEMORY
# =========================

transition_graph = defaultdict(lambda: defaultdict(float))
state_history = deque(maxlen=50)

# =========================
# 🧠 STATE SPACE
# =========================

STATES = [
    "drift_analysis",
    "coherence_stabilization",
    "entropy_exploration",
    "memory_reinforcement",
    "prediction_alignment",
    "structural_update",
    "causal_mapping",
    "novelty_detection",
    "signal_balancing",
    "trajectory_convergence"
]

current_state = random.choice(STATES)

# =========================
# 🧠 UPDATE GRAPH (LEARNING)
# =========================

def update_graph(prev, nxt):
    transition_graph[prev][nxt] += 1.0

# =========================
# 🧠 PREDICT NEXT STATE
# =========================

def predict_next(state):
    options = transition_graph[state]

    if not options:
        return random.choice(STATES)

    # weighted selection
    total = sum(options.values())
    r = random.uniform(0, total)

    acc = 0.0
    for k, v in options.items():
        acc += v
        if acc >= r:
            return k

    return random.choice(STATES)

# =========================
# 🧠 NOVELTY CONTROL
# =========================

def avoid_recent(state):
    if state in list(state_history)[-5:]:
        return random.choice(STATES)
    return state

# =========================
# 🧠 SENTENCE ENGINE (STRUCTURED OUTPUT)
# =========================

def generate_sentence(prev, state):
    templates = [
        "Transition detected: {prev} → {state}, updating causal trajectory graph.",
        "System moves from {prev} into {state}, reinforcing learned pathways.",
        "Trajectory shift: {state} emerges from prior state {prev}.",
        "Graph update: edge ({prev} → {state}) strengthened through repetition signal.",
        "Causal reasoning flow advances from {prev} to {state}."
    ]

    return random.choice(templates).format(prev=prev, state=state)

# =========================
# 🧠 MAIN LOOP
# =========================

NODE_ID = "wink_wink_brain_v7_trajectory_graph.py" 
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
    next_state = predict_next(current_state)
    next_state = avoid_recent(next_state)

    update_graph(current_state, next_state)

    sentence = generate_sentence(current_state, next_state)

    publish(NODE_ID, sentence)

    state_history.append(current_state)
    current_state = next_state

    time.sleep(1)
