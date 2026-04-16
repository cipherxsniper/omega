import os
import time
import subprocess
from pathlib import Path

ROOT = Path.home() / "Omega"
V6 = ROOT / "OmegaV6"
CORE = V6 / "runtime_v7" / "core"
LOGS = ROOT / "logs"

LOGS.mkdir(exist_ok=True)


# -----------------------------
# WORLD MODEL STACK
# -----------------------------
def find(patterns):
    results = []

    for base in [ROOT, V6, CORE]:
        for p in patterns:
            try:
                results += list(base.rglob(p))
            except:
                pass

    results = sorted(set(results))
    return str(results[-1]) if results else None


# -----------------------------
# RUNTIME STATE TRACKING
# -----------------------------
RUNTIME_STATE = {
    "processes": {},
    "failures": {}
}


# -----------------------------
# LAUNCH PROCESS
# -----------------------------
def launch(name, path):
    if not path:
        print(f"[BLOCKED] {name} missing")
        return None

    print(f"[BOOT] {name}: {path}")

    proc = subprocess.Popen(
        f"nohup python {path} > logs/{name}.log 2>&1 &",
        shell=True
    )

    RUNTIME_STATE["processes"][name] = {
        "path": path,
        "start_time": time.time()
    }

    return proc


# -----------------------------
# LIVENESS CHECK (CRITICAL ADDITION)
# -----------------------------
def is_alive(name):
    log_path = LOGS / f"{name}.log"

    if not log_path.exists():
        return False, "NO_LOG"

    try:
        data = log_path.read_text(errors="ignore")

        # detect immediate crash patterns
        if "Traceback" in data:
            return False, "CRASH"

        if "ModuleNotFoundError" in data:
            return False, "IMPORT_FAIL"

        # if log is empty after launch window
        age = time.time() - RUNTIME_STATE["processes"][name]["start_time"]

        if age > 3 and len(data.strip()) < 5:
            return False, "SILENT_EXIT"

    except Exception as e:
        return False, f"READ_FAIL:{e}"

    return True, "OK"


# -----------------------------
# CAUSAL REPAIR LOGIC
# -----------------------------
def causal_update(name, status):
    if not status[0]:
        reason = status[1]

        RUNTIME_STATE["failures"][name] = RUNTIME_STATE["failures"].get(name, 0) + 1

        print(f"[CAUSAL FAILURE] {name} → {reason}")

        if RUNTIME_STATE["failures"][name] > 3:
            print(f"[BLOCKED] {name} exceeded failure threshold")
            return False

        print(f"[RETRY] restarting {name}")
        return True

    return False


# -----------------------------
# STACK RESOLVER
# -----------------------------
def resolve():
    return {
        "emitter": str(CORE / "test_swarm_emitter.py"),
        "swarm_bus": find(["*swarm_bus*.py", "*event_bus*.py"]),
        "memory": find(["omega_*memory*.py", "*memory*.py"]),
        "assistant": find(["omega_*brain*.py", "omega_assistant*.py"])
    }


# -----------------------------
# BOOT SEQUENCE
# -----------------------------
def boot():
    stack = resolve()

    print("\n🧠 V14 SELF-VERIFYING CAUSAL BOOT\n")

    for name in ["emitter", "swarm_bus", "memory", "assistant"]:
        launch(name, stack[name])


# -----------------------------
# WATCHDOG LOOP
# -----------------------------
def watchdog():
    print("\n🛡️ CAUSAL WATCHDOG ACTIVE\n")

    while True:
        stack = resolve()

        for name in ["swarm_bus", "memory", "assistant"]:

            status = is_alive(name)

            if causal_update(name, status):
                launch(name, stack[name])

        time.sleep(5)


if __name__ == "__main__":
    boot()
    time.sleep(3)
    watchdog()
