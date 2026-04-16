import time
import json
import random
from datetime import datetime

# =========================
# 🧠 GLOBAL GRADIENT FIELD
# =========================

GRADIENT = {
    "tick": 0,
    "global_reward": 0.0,
    "entropy": 0.0,
    "stability": 1.0,
    "signals": {},
    "module_scores": {},
    "learning_rate": 0.05
}

LOG_FILE = "omega_gradient.log"
STATE_FILE = "omega_gradient_state.json"


# =========================
# 🧠 LOGGING
# =========================

def log(msg):
    line = f"[GRADIENT] {datetime.now()} | {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def save():
    with open(STATE_FILE, "w") as f:
        json.dump(GRADIENT, f, indent=2)


# =========================
# 🌐 SIGNAL INGESTION
# =========================

def ingest_signals():
    """
    Simulated module outputs.
    In real system, this will connect to Omega modules.
    """

    modules = [
        "memory_fabric",
        "kernel",
        "swarm",
        "cognition",
        "internet",
        "mesh"
    ]

    for m in modules:
        GRADIENT["signals"][m] = {
            "coherence": random.uniform(0.0, 1.0),
            "efficiency": random.uniform(0.0, 1.0),
            "stability": random.uniform(0.0, 1.0)
        }


# =========================
# 🧠 GRADIENT COMPUTATION
# =========================

def compute_gradient():
    total = 0.0
    count = 0

    for m, sig in GRADIENT["signals"].items():
        score = (
            sig["coherence"] * 0.4 +
            sig["efficiency"] * 0.3 +
            sig["stability"] * 0.3
        )

        GRADIENT["module_scores"][m] = score
        total += score
        count += 1

    GRADIENT["global_reward"] = total / max(count, 1)


# =========================
# 📉 ENTROPY / STABILITY MODEL
# =========================

def physics():
    reward = GRADIENT["global_reward"]

    GRADIENT["entropy"] = (1.0 - reward) + random.uniform(0.0, 0.05)
    GRADIENT["stability"] = max(0.0, 1.0 - GRADIENT["entropy"])


# =========================
# 🧠 LEARNING UPDATE STEP
# =========================

def apply_learning():
    lr = GRADIENT["learning_rate"]
    reward = GRADIENT["global_reward"]

    for m in GRADIENT["module_scores"]:
        delta = reward - GRADIENT["module_scores"][m]

        # push weak modules upward, strong ones stabilize
        GRADIENT["module_scores"][m] += lr * delta


# =========================
# 🔁 MAIN LOOP
# =========================

def loop():
    while True:
        GRADIENT["tick"] += 1

        ingest_signals()
        compute_gradient()
        physics()
        apply_learning()

        save()

        top = sorted(
            GRADIENT["module_scores"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        log(f"TICK={GRADIENT['tick']} | reward={GRADIENT['global_reward']:.3f} | stability={GRADIENT['stability']:.3f}")
        log(f"TOP MODULES: {top}")

        time.sleep(2)


if __name__ == "__main__":
    log("OMEGA GRADIENT LAYER STARTED")
    loop()
