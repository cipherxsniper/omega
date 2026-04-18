from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import time
import random
import hashlib
from collections import deque, defaultdict

# =========================
# 🧠 CORE MEMORY SYSTEM
# =========================

short_memory = deque(maxlen=30)
long_memory = deque(maxlen=500)

trajectory_graph = defaultdict(lambda: defaultdict(float))

state_history = deque(maxlen=50)

# =========================
# 🧠 UTILS
# =========================

def hash_state(s):
    return hashlib.md5(s.encode()).hexdigest()

def novelty(sentence):
    h = hash_state(sentence)
    return 0.0 if h in long_memory else 1.0

# =========================
# 🧠 TRAJECTORY UPDATER
# =========================

def update_trajectory(prev_state, new_state):
    trajectory_graph[prev_state][new_state] += 1.0

def dominant_path():
    if not trajectory_graph:
        return "initialization"

    best_from = max(trajectory_graph.items(), key=lambda x: sum(x[1].values()))[0]
    best_to = max(trajectory_graph[best_from], key=trajectory_graph[best_from].get)
    return f"{best_from} → {best_to}"

# =========================
# 🧠 STATE ENGINE
# =========================

def analyze_signal():
    base = random.uniform(0.45, 0.98)
    noise = random.uniform(-0.02, 0.02)
    return round(base + noise, 3)

def classify_state(signal):
    if signal > 0.85:
        return "high_coherence"
    elif signal > 0.6:
        return "adaptive_flow"
    elif signal > 0.4:
        return "exploratory"
    return "unstable"

# =========================
# 🧠 SENTENCE GENERATOR (NON-REPETITIVE)
# =========================

def generate_sentence(signal, state, trajectory):

    templates = [
        "System transitions through {state} with signal stability {signal}.",
        "Causal trajectory indicates movement along {trajectory}.",
        "Observational layer detects {state} dynamics at intensity {signal}.",
        "Memory-weighted inference aligns system into {state} regime.",
        "Trajectory compression reveals pathway: {trajectory}."
    ]

    candidates = []

    for t in templates:
        sentence = t.format(
            state=state,
            signal=signal,
            trajectory=trajectory
        )

        score = novelty(sentence)
        candidates.append((score, sentence))

    candidates.sort(reverse=True, key=lambda x: x[0])

    pool = [s for s in candidates if s[0] > 0]

    if not pool:
        pool = candidates

    chosen = random.choice([p[1] for p in pool])

    long_memory.append(hash_state(chosen))
    short_memory.append(chosen)

    return chosen

# =========================
# 🧠 MAIN LOOP
# =========================

prev_state = "boot"

NODE_ID = "wink_wink_brain_v8.py" 
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

    signal = analyze_signal()
    state = classify_state(signal)

    update_trajectory(prev_state, state)

    trajectory = dominant_path()

    sentence = generate_sentence(signal, state, trajectory)

    publish(NODE_ID, sentence)

    state_history.append(state)
    prev_state = state

    time.sleep(1)
