import json
import os

MEM_FILE = "wink_wink_memory_v22.json"
POLICY_FILE = "wink_wink_policy_v23.json"

# --------------------------
# LOAD MEMORY
# --------------------------

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# --------------------------
# POLICY (THIS IS THE "LEARNING BRAIN")
# --------------------------

policy = load_json(POLICY_FILE, {
    "state_bias": {
        "HIGH COHERENCE": 1.0,
        "STABLE EXPLORATION": 1.0,
        "ACTIVE DRIFT": 1.0,
        "FRAGMENTED STATE": 1.0
    },
    "reward_sensitivity": 1.0,
    "novelty_weight": 1.0
})

# --------------------------
# MEMORY ANALYSIS
# --------------------------

def analyze_memory():
    data = load_json(MEM_FILE, {"state_history": []})

    states = data["state_history"][-200:]

    if not states:
        return {}

    stats = {
        "avg_signal": sum(x["signal"] for x in states) / len(states),
        "avg_reward": sum(x["reward"] for x in states) / len(states),
        "state_counts": {}
    }

    for x in states:
        s = x["state"]
        stats["state_counts"][s] = stats["state_counts"].get(s, 0) + 1

    return stats

# --------------------------
# LEARNING UPDATE RULE (IMPORTANT)
# --------------------------

def update_policy(stats):

    if not stats:
        return policy

    # reinforce frequent states
    for state, count in stats["state_counts"].items():
        if state in policy["state_bias"]:
            policy["state_bias"][state] += count * 0.001

    # normalize biases
    total = sum(policy["state_bias"].values())

    for k in policy["state_bias"]:
        policy["state_bias"][k] /= total

    # adapt reward sensitivity
    if stats["avg_reward"] > 0.95:
        policy["reward_sensitivity"] *= 1.01
    else:
        policy["reward_sensitivity"] *= 0.99

    # clamp
    policy["reward_sensitivity"] = max(0.5, min(2.0, policy["reward_sensitivity"]))

    save_json(POLICY_FILE, policy)

    return policy

# --------------------------
# APPLY POLICY TO SYSTEM
# --------------------------

def modulate_state(state):
    bias = policy["state_bias"].get(state, 1.0)

    if bias > 1.2:
        return state + " (reinforced)"
    elif bias < 0.8:
        return state + " (decaying)"
    return state

# --------------------------
# EXPORT API
# --------------------------

def get_policy():
    return policy

def learn():
    stats = analyze_memory()
    return update_policy(stats)
