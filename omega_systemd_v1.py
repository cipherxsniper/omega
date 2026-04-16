import subprocess
import time
import json
import os
from collections import defaultdict

print("\n🧠 OMEGA SYSTEMD v1 ONLINE\n")


# =========================
# LOAD MODULE LIST
# =========================
OMEGA_ROOT = os.path.expanduser("~/Omega")

def discover_modules():
    modules = []
    for root, _, files in os.walk(OMEGA_ROOT):
        for f in files:
            if f.endswith(".py") and "omega_" in f:
                modules.append(os.path.join(root, f))
    return modules


# =========================
# LIFECYCLE CONTRACT
# =========================
LIFECYCLE = {
    "default": {
        "restart": "backoff",   # none | always | backoff
        "backoff_base": 3,
        "max_restarts": 3,
        "min_runtime": 5
    }
}


# =========================
# PROCESS STATE TRACKER
# =========================
class ProcessState:
    def __init__(self):
        self.processes = {}
        self.restarts = defaultdict(int)
        self.last_start = {}

    def can_restart(self, name):
        policy = LIFECYCLE["default"]

        if self.restarts[name] >= policy["max_restarts"]:
            print(f"⛔ MAX RESTARTS HIT: {name}")
            return False

        last = self.last_start.get(name, 0)
        if time.time() - last < policy["min_runtime"]:
            return False

        return True

    def record_start(self, name):
        self.last_start[name] = time.time()
        self.restarts[name] += 1


STATE = ProcessState()


# =========================
# LAUNCH MODULE
# =========================
def launch(module_path):
    name = os.path.basename(module_path)

    if not STATE.can_restart(name):
        print(f"⏸️ BLOCKED (policy): {name}")
        return None

    print(f"🚀 START: {name}")

    try:
        p = subprocess.Popen(
            ["python", module_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        STATE.processes[name] = p
        STATE.record_start(name)

        return p

    except Exception as e:
        print(f"❌ FAILED: {name} -> {e}")
        return None


# =========================
# HEALTH CHECK
# =========================
def check_processes():
    dead = []

    for name, proc in STATE.processes.items():
        if proc.poll() is not None:
            dead.append(name)

    return dead


# =========================
# BACKOFF RESTART
# =========================
def restart_with_backoff(name, module_path):
    delay = LIFECYCLE["default"]["backoff_base"] * STATE.restarts[name]

    print(f"⏳ BACKOFF {delay}s for {name}")
    time.sleep(delay)

    launch(module_path)


# =========================
# BOOT SYSTEM
# =========================
def boot():
    modules = discover_modules()

    print(f"📦 Modules discovered: {len(modules)}\n")

    # limit to safe batch
    modules = modules[:25]

    print("🧩 INITIAL BOOT (MAX 25 MODULES)\n")

    for m in modules:
        launch(m)
        time.sleep(0.3)

    print("\n🟢 OMEGA SYSTEMD v1 RUNNING\n")

    # main loop
    while True:
        time.sleep(5)

        dead = check_processes()

        if dead:
            print(f"\n⚠️ DEAD PROCESSES: {len(dead)}")

        for name in dead:
            # find module path again
            for m in modules:
                if name in m:
                    restart_with_backoff(name, m)

        print("🟢 SYSTEM HEALTH OK")


if __name__ == "__main__":
    boot()

# =========================
# MODULE TYPE INTELLIGENCE LAYER
# =========================

MODULE_CLASSIFICATION = {
    "run_omega": "task",
    "launcher": "task",
    "fix_": "task",
    "brain": "brain",
    "mesh": "service",
    "kernel": "daemon",
    "engine": "service",
    "orchestrator": "service",
}

def classify(module_name):
    for key, val in MODULE_CLASSIFICATION.items():
        if key in module_name:
            return val
    return "service"


def should_restart(module_name, exit_code):
    mtype = classify(module_name)

    # TASKS NEVER RESTART
    if mtype == "task":
        return False

    # NORMAL EXIT IS NOT FAILURE
    if exit_code == 0:
        return False

    return True

