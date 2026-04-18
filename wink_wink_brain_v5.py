from omega_mesh_bus_v1 import register, publish, fetch_recent, global_signal
import time
import random
import hashlib
from collections import deque

memory = set()
recent = deque(maxlen=25)
roles = deque(maxlen=10)

ROLE_SET = ["observer", "analyzer", "predictor", "stabilizer"]

def h(s):
    return hashlib.sha256(s.encode()).hexdigest()

def repetition_penalty(sentence):
    return 0.0 if h(sentence) in memory else 1.0

def role_shift():
    role = random.choice(ROLE_SET)
    roles.append(role)
    return role

def semantic_variation(role, signal, reward):
    base = [
        "System observes structural changes across memory layers.",
        "Causal patterns reorganize under evolving constraints.",
        "Predictive alignment suggests shifting behavioral drift.",
        "Stability feedback loops reinforce current system state."
    ]

    if role == "observer":
        prefix = "OBSERVATION:"
    elif role == "analyzer":
        prefix = "ANALYSIS:"
    elif role == "predictor":
        prefix = "PREDICTION:"
    else:
        prefix = "STABILITY:"

    return [f"{prefix} {b}" for b in base]

def score(sentence):
    penalty = repetition_penalty(sentence)

    recent_pressure = 0.5
    for r in recent:
        if r == sentence:
            recent_pressure -= 0.4

    return penalty + recent_pressure

def generate(signal, reward):
    role = role_shift()
    candidates = semantic_variation(role, signal, reward)

    best = None
    best_score = -999

    for c in candidates:
        s = score(c)

        if s > best_score:
            best_score = s
            best = c

    memory.add(h(best))
    recent.append(best)

    return best

def observe():
    return {
        "signal": random.uniform(0.2, 0.95),
        "reward": random.uniform(0.4, 1.0)
    }

NODE_ID = "wink_wink_brain_v5.py" 
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
    m = observe()
    publish(NODE_ID, generate(m["signal"], m["reward"]))
    time.sleep(1)
