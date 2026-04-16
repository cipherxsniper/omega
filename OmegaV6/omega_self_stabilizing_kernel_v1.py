import subprocess
import time
from pathlib import Path
from collections import defaultdict, deque

ROOT = Path.home() / "Omega"
LOGS = ROOT / "logs"

# =========================
# EXECUTION MODEL
# =========================
EXEC_TYPE = {
    "swarm_bus": "SERVICE",
    "memory": "TASK",
    "assistant": "SERVICE",
    "emitter": "TASK"
}

# =========================
# MODULE PATH MAP
# =========================
MODULE_PATHS = {
    "swarm_bus": "OmegaV6/runtime_v7/core/v9_9_swarm_bus_v14.py",
    "memory": "omega_swarm_memory_bridge_v9.py",
    "assistant": "omega_unified_brain_v22.py",
    "emitter": "OmegaV6/runtime_v7/core/test_swarm_emitter.py"
}

# =========================
# KERNEL STATE MEMORY
# =========================
state_history = defaultdict(lambda: deque(maxlen=5))
cooldowns = defaultdict(int)

COOLDOWN_TICKS = 3

# =========================
# RUNTIME DETECTION
# =========================
def is_running(signature):
    try:
        out = subprocess.check_output(["pgrep", "-f", signature])
        return len(out.strip()) > 0
    except Exception:
        return False

# =========================
# SEMANTIC RISK MODEL (simple v1)
# =========================
def compute_risk(module):
    running = is_running(module)

    if running:
        return 0.2
    else:
        return 0.85

# =========================
# TREND ENGINE
# =========================
def update_history(module, value):
    state_history[module].append(value)

def trend(module):
    h = list(state_history[module])
    if len(h) < 3:
        return "UNKNOWN"

    if h[-1] > h[-2] > h[-3]:
        return "WORSENING"
    if h[-1] < h[-2] < h[-3]:
        return "STABILIZING"
    return "FLAT"

# =========================
# DECISION ENGINE
# =========================
def decide(module, risk):
    t = trend(module)

    # prevent infinite restart loops
    if cooldowns[module] > 0:
        cooldowns[module] -= 1
        return "COOLDOWN"

    if risk > 0.75:
        return "HARD_RESTART"

    if risk > 0.5:
        if t == "WORSENING":
            return "SOFT_RESTART"
        return "MONITOR"

    if risk > 0.3:
        return "MONITOR"

    return "NO_ACTION"

# =========================
# ACTION ENGINE
# =========================
def stop(module):
    subprocess.call(["pkill", "-f", module])

def start(module):
    path = MODULE_PATHS[module]
    cmd = f"nohup python {path} > {LOGS}/{module}.log 2>&1 &"
    subprocess.Popen(cmd, shell=True)
    print(f"[KERNEL] START → {module}")

def execute(module, action):
    if action == "HARD_RESTART":
        stop(module)
        time.sleep(1)
        start(module)
        cooldowns[module] = COOLDOWN_TICKS
        print(f"[KERNEL] HARD RESTART → {module}")

    elif action == "SOFT_RESTART":
        stop(module)
        time.sleep(2)
        start(module)
        cooldowns[module] = COOLDOWN_TICKS
        print(f"[KERNEL] SOFT RESTART → {module}")

    elif action == "MONITOR":
        print(f"[KERNEL] MONITOR → {module}")

    elif action == "COOLDOWN":
        print(f"[KERNEL] COOLDOWN ACTIVE → {module}")

    elif action == "NO_ACTION":
        print(f"[KERNEL] STABLE → {module}")

# =========================
# KERNEL LOOP
# =========================
def run():
    print("\n🧠 OMEGA SELF-STABILIZING KERNEL v1\n")

    cycle = 0

    while True:
        cycle += 1
        print(f"\n──────── CYCLE {cycle} ────────")

        for module in MODULE_PATHS.keys():
            risk = compute_risk(module)
            update_history(module, risk)

            action = decide(module, risk)

            print(f"\nMODULE : {module}")
            print(f"RISK   : {risk}")
            print(f"TREND  : {trend(module)}")
            print(f"ACTION : {action}")

            execute(module, action)

        print("\n🧠 KERNEL CYCLE COMPLETE\n")
        time.sleep(10)

if __name__ == "__main__":
    run()
