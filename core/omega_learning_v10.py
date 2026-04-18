import json
import os

STATE_FILE = "omega_state.json"

def safe_load():
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r") as f:
            data = f.read().strip()

            if not data:
                return {}

            # HARD GUARD: prevent multi-json corruption crash
            return json.loads(data.splitlines()[0])

    except Exception:
        return {}

def safe_save(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def step():
    state = safe_load()

    # fake RL step (safe mode)
    state["tick"] = state.get("tick", 0) + 1
    state["reward"] = state.get("reward", 0) * 0.99

    safe_save(state)

    print("🧠 OMEGA SAFE STEP", state)

if __name__ == "__main__":
    while True:
        step()
