import os
import subprocess
import time
from pathlib import Path

OMEGA_ROOT = Path.home() / "Omega"
OMEGA_V6 = OMEGA_ROOT / "OmegaV6"
CORE_DIR = OMEGA_V6 / "runtime_v7" / "core"

LOG_DIR = OMEGA_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# -----------------------------
# RESOLVER
# -----------------------------
def safe_find(patterns, search_paths=None):
    search_paths = search_paths or [OMEGA_ROOT, OMEGA_V6, CORE_DIR]
    results = []

    for base in search_paths:
        for pattern in patterns:
            try:
                results.extend(base.rglob(pattern))
            except:
                pass

    results = sorted(set(results))
    return str(results[-1]) if results else None


# -----------------------------
# TRACK PROCESS START TIME
# -----------------------------
process_start_times = {}


def launch(name, cmd):
    if not cmd:
        return

    subprocess.Popen(cmd, shell=True)
    process_start_times[name] = time.time()


def is_alive_long_enough(name, min_age=5):
    """Only consider process valid if it has survived X seconds"""
    start = process_start_times.get(name)
    if not start:
        return False
    return (time.time() - start) > min_age


# -----------------------------
# STACK
# -----------------------------
def resolve_stack():
    return {
        "swarm_bus": safe_find(["*swarm_bus*.py", "*event_bus*.py", "*omega_bus*.py"]),
        "memory": safe_find(["omega_*memory*.py", "*memory*.py"]),
        "assistant": safe_find(["omega_*brain*.py", "omega_assistant*.py"]),
        "emitter": str(CORE_DIR / "test_swarm_emitter.py")
    }


def boot_all():
    stack = resolve_stack()

    print("\n🧠 V11.1 STABLE BOOT\n")

    launch("swarm_bus", f"nohup python {stack['swarm_bus']} > logs/bus.log 2>&1 &")
    launch("memory", f"nohup python {stack['memory']} > logs/memory.log 2>&1 &")
    launch("assistant", f"nohup python {stack['assistant']} > logs/assistant.log 2>&1 &")
    launch("emitter", f"nohup python {stack['emitter']} > logs/emitter.log 2>&1 &")


def watchdog():
    print("\n🛡️ STABILITY WATCHDOG ACTIVE\n")

    while True:

        # ONLY RESTART IF IT FAILS AFTER STABILIZATION
        if not is_alive_long_enough("swarm_bus"):
            print("[WARN] swarm_bus unstable → waiting before restart")
            boot_all()

        time.sleep(10)


if __name__ == "__main__":
    boot_all()
    watchdog()
