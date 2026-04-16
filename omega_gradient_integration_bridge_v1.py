import json
import time
import psutil
import os
from datetime import datetime

# =========================
# 🧠 SHARED STATE LINKS
# =========================

GRADIENT_FILE = "omega_gradient_state.json"
KERNEL_STATE_FILE = "omega_unified_state.json"
MEMORY_FILE = "omega_persistent_weights.json"


# =========================
# 🧠 LOAD HELPERS
# =========================

def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# =========================
# 🌐 TELEMETRY SYSTEM (REAL SIGNALS)
# =========================

def collect_telemetry():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "process_count": len(psutil.pids()),
        "load": os.getloadavg()[0] if hasattr(os, "getloadavg") else 0
    }


# =========================
# 🧠 UPDATE KERNEL FROM GRADIENT
# =========================

def update_kernel_from_gradient(kernel, gradient):
    reward = gradient.get("global_reward", 0.5)

    # kernel self-adjusts physics parameters
    kernel["entropy"] = kernel.get("entropy", 0.5)
    kernel["stability"] = kernel.get("stability", 0.5)

    kernel["entropy"] += (1 - reward) * 0.05
    kernel["stability"] = max(0.0, 1.0 - kernel["entropy"] * 0.4)

    kernel["adaptation_signal"] = reward


# =========================
# 🧠 UPDATE SCHEDULER (INTELLIGENT PRIORITY SHIFT)
# =========================

def update_scheduler(gradient):
    scores = gradient.get("module_scores", {})

    sorted_nodes = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    scheduler = {
        "priority_queue": sorted_nodes[:5],
        "tick": gradient.get("tick", 0)
    }

    return scheduler


# =========================
# 🧠 PERSISTENT MEMORY WEIGHTS
# =========================

def update_memory_weights(memory, gradient):
    lr = 0.05

    for module, score in gradient.get("module_scores", {}).items():
        old = memory.get(module, 0.5)
        memory[module] = old + lr * (score - old)

    return memory


# =========================
# 🔁 MAIN LOOP
# =========================

def loop():
    print("🧠 OMEGA INTEGRATION BRIDGE STARTED")

    while True:
        gradient = load_json(GRADIENT_FILE, {})
        kernel = load_json(KERNEL_STATE_FILE, {})
        memory = load_json(MEMORY_FILE, {})

        telemetry = collect_telemetry()

        # inject real telemetry into gradient system
        gradient["telemetry"] = telemetry

        update_kernel_from_gradient(kernel, gradient)

        scheduler = update_scheduler(gradient)

        memory = update_memory_weights(memory, gradient)

        save_json(KERNEL_STATE_FILE, kernel)
        save_json(MEMORY_FILE, memory)
        save_json("omega_scheduler.json", scheduler)

        print(
            f"[OMEGA-INT] reward={gradient.get('global_reward', 0):.3f} "
            f"| stability={kernel.get('stability', 0):.3f} "
            f"| cpu={telemetry['cpu']}%"
        )

        time.sleep(2)


if __name__ == "__main__":
    loop()
