import time
import random

def compute_signal(state):
    # replace this with real metrics later
    return random.uniform(0.3, 0.9)

def compute_reward(signal):
    return max(0.0, min(1.0, signal + random.uniform(-0.1, 0.1)))

def analyze_system():
    signal = compute_signal({})
    reward = compute_reward(signal)

    return {
        "signal": signal,
        "reward": reward,
        "state": "ACTIVE_LEARNING" if signal > 0.5 else "OBSERVATION"
    }
