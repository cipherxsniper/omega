import os
import time
import subprocess
from pathlib import Path

OMEGA_ROOT = Path.home() / "Omega"
OMEGA_V6 = OMEGA_ROOT / "OmegaV6"
CORE_DIR = OMEGA_V6 / "runtime_v7" / "core"

LOG_DIR = OMEGA_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)


# -----------------------------
# STATE MEMORY (CRITICAL FIX)
# -----------------------------
state = {
    "last_restart": {},
    "failure_count": {},
    "cooldown": 15  # seconds
}


# -----------------------------
# FIND FILES
# -----------------------------
def safe_find(patterns):
    results = []

    for base in [OMEGA_ROOT, OMEGA_V6, CORE_DIR]:
        for p in patterns:
            try:
                results.extend(base.rglob(p))
            except:
                pass

    results = sorted(set(results))
    return str(results[-1]) if results else None


# -----------------------------
# LAUNCH
# -----------------------------
def launch(name, path):
    if not path:
        return False

    now = time.time()
    last = state["last_restart"].get(name, 0)

    # ⛔ COOLDOWN GATE
    if now - last < state["cooldown"]:
        print(f"[COOLDOWN] {name} blocked (too frequent restarts)")
        return False

    cmd = f"nohup python {path} > logs/{name}.log 2>&1 &"
    subprocess.Popen(cmd, shell=True)

    state["last_restart"][name] = now
    state["failure_count"][name] = state["failure_count"].get(name, 0)

    return True


# -----------------------------
# DIAGNOSE
# -----------------------------
def diagnose(name, path):
    if not path:
        return "MISSING"

    log_path = LOG_DIR / f"{name}.log"

    try:
        if log_path.exists():
            data = log_path.read_text(errors="ignore")

            if "ModuleNotFoundError" in data:
                return "IMPORT_ERROR"

            if "Traceback" in data:
                return "CRASH"

            if len(data.strip()) < 10:
                return "SILENT_EXIT"

    except:
        pass

    return "OK"


# -----------------------------
# REPAIR DECISION
# -----------------------------
def should_restart(name, cause):
    count = state["failure_count"].get(name, 0)

    if cause == "OK":
        return False

    # increment failure count
    state["failure_count"][name] = count + 1

    # ⛔ STOP IF TOO MANY FAILURES
    if state["failure_count"][name] > 5:
        print(f"[BLOCKED] {name} exceeded failure threshold")
        return False

    return True


# -----------------------------
# STACK
# -----------------------------
def resolve_stack():
    return {
        "swarm_bus": safe_find(["*swarm_bus*.py", "*event_bus*.py"]),
        "memory": safe_find(["omega_*memory*.py", "*memory*.py"]),
        "assistant": safe_find(["omega_*brain*.py", "omega_assistant*.py"]),
        "emitter": str(CORE_DIR / "test_swarm_emitter.py")
    }


# -----------------------------
# BOOT
# -----------------------------
def boot():
    stack = resolve_stack()

    print("\n🧠 V12.1 STABILITY ENGINE STARTED\n")

    for name, path in stack.items():
        launch(name, path)


# -----------------------------
# WATCHDOG
# -----------------------------
def watchdog():
    print("\n🛡️ STABILITY WATCHDOG ACTIVE\n")

    while True:
        stack = resolve_stack()

        for name, path in stack.items():

            cause = diagnose(name, path)

            if should_restart(name, cause):
                print(f"[RECOVER] {name} → {cause}")
                launch(name, path)

        time.sleep(8)


if __name__ == "__main__":
    boot()
    watchdog()
