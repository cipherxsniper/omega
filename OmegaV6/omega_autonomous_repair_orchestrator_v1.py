import subprocess
import time
from pathlib import Path

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
# MOCK RISK INPUT (replace later with collapse engine)
# =========================
def get_risk_snapshot():
    return {
        "swarm_bus": 0.85,
        "memory": 0.60,
        "assistant": 0.25,
        "emitter": 0.40
    }

# =========================
# PROCESS CHECK
# =========================
def is_running(name):
    try:
        out = subprocess.check_output(["pgrep", "-f", name])
        return len(out.strip()) > 0
    except Exception:
        return False

# =========================
# SAFE STARTER
# =========================
def start_process(path, label):
    if not path:
        return False

    cmd = f"nohup python {path} > {LOGS}/{label}.log 2>&1 &"
    subprocess.Popen(cmd, shell=True)
    print(f"[REPAIR] STARTED → {label}")
    return True

# =========================
# SAFE STOPPER
# =========================
def stop_process(name):
    try:
        subprocess.call(["pkill", "-f", name])
        print(f"[REPAIR] STOPPED → {name}")
    except Exception:
        pass

# =========================
# MODULE PATH MAP (fallback safe)
# =========================
MODULE_PATHS = {
    "swarm_bus": "OmegaV6/runtime_v7/core/v9_9_swarm_bus_v14.py",
    "memory": "omega_swarm_memory_bridge_v9.py",
    "assistant": "omega_unified_brain_v22.py",
    "emitter": "OmegaV6/runtime_v7/core/test_swarm_emitter.py"
}

# =========================
# POLICY ENGINE
# =========================
def decide(module, risk):
    exec_type = EXEC_TYPE[module]

    if risk > 0.75:
        return "RESTART_SERVICE" if exec_type == "SERVICE" else "RETRY_TASK"

    if risk > 0.5:
        return "SOFT_RESTART" if exec_type == "SERVICE" else "DEFER_TASK"

    if risk > 0.3:
        return "MONITOR"

    return "NO_ACTION"

# =========================
# REPAIR ENGINE
# =========================
def repair(module, action):
    path = MODULE_PATHS[module]

    if action == "RESTART_SERVICE":
        stop_process(module)
        time.sleep(1)
        start_process(path, module)

    elif action == "SOFT_RESTART":
        stop_process(module)
        time.sleep(2)
        start_process(path, module)

    elif action == "RETRY_TASK":
        start_process(path, module)

    elif action == "DEFER_TASK":
        print(f"[REPAIR] DEFERRED → {module}")

    elif action == "MONITOR":
        print(f"[REPAIR] MONITORING → {module}")

    elif action == "NO_ACTION":
        print(f"[REPAIR] STABLE → {module}")

# =========================
# MAIN LOOP
# =========================
def run():
    print("\n🧠 OMEGA AUTONOMOUS REPAIR ORCHESTRATOR v1\n")

    while True:
        risks = get_risk_snapshot()

        for module, risk in risks.items():
            action = decide(module, risk)

            print(f"\n────────────────────")
            print(f"MODULE : {module}")
            print(f"RISK   : {risk}")
            print(f"ACTION : {action}")

            repair(module, action)

        print("\n🧠 CYCLE COMPLETE — sleeping...\n")
        time.sleep(10)

if __name__ == "__main__":
    run()
