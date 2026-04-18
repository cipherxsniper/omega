from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import time
import random
import hashlib
from collections import deque, defaultdict

# -----------------------------
# MEMORY SYSTEM
# -----------------------------

recent_sentences = deque(maxlen=25)
long_term_memory = defaultdict(int)

states = ["observation", "analysis", "prediction", "reflection"]
state_index = 0

# -----------------------------
# HELPERS
# -----------------------------

def hash_text(t):
    return hashlib.md5(t.encode()).hexdigest()

def similarity_penalty(sentence):
    """simple repetition penalty"""
    h = hash_text(sentence)
    return long_term_memory[h] * 0.25

def rotate_state():
    global state_index
    state_index = (state_index + 1) % len(states)
    return states[state_index]

# -----------------------------
# CORE SENTENCE ENGINE
# -----------------------------

def generate_sentence(signal, reward, state):

    base_templates = [
        "System transitions through {state} with signal stability {signal:.3f}.",
        "Memory-weighted analysis suggests structural drift under {state} conditions.",
        "Causal evaluation indicates evolving behavior during {state} phase.",
        "Predictive alignment adjusts system interpretation in {state} mode.",
        "Observational layer detects pattern reorganization during {state} activity."
    ]

    novelty_pressure = random.random()

    candidates = []

    for t in base_templates:
        sentence = t.format(state=state, signal=signal)

        penalty = similarity_penalty(sentence)
        score = novelty_pressure - penalty

        candidates.append((score, sentence))

    candidates.sort(key=lambda x: x[0], reverse=True)
    chosen = candidates[0][1]

    h = hash_text(chosen)
    recent_sentences.append(chosen)
    long_term_memory[h] += 1

    return chosen

# -----------------------------
# SIMULATION LOOP
# -----------------------------

def run():
    signal = 0.5
    reward = 0.5

NODE_ID = "wink_wink_brain_v10.py" 
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
        state = rotate_state()

        signal += random.uniform(-0.01, 0.01)
        reward = max(0, min(1, reward + random.uniform(-0.02, 0.02)))

        sentence = generate_sentence(signal, reward, state)
        publish(NODE_ID, sentence)

        time.sleep(1)

if __name__ == "__main__":
    run()
