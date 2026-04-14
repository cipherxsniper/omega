import os
import time
import subprocess
from collections import defaultdict, deque

print("\n🧠 OMEGA SYSTEMD v4 EXECUTION GOVERNOR ONLINE\n")

OMEGA_ROOT = os.path.expanduser("~/Omega")


# =========================
# DISCOVERY
# =========================
def discover_modules():
    modules = []
    for root, _, files in os.walk(OMEGA_ROOT):
        for f in files:
            if f.endswith(".py") and "omega_" in f:
                modules.append(os.path.join(root, f))
    return modules


# =========================
# EXECUTION TYPES (OS LAW LAYER)
# =========================
EXEC_TYPE = {
    "run_": "task",
    "fix_": "task",
    "patch": "task",
    "launcher": "task",
    "kernel": "kernel",
    "identity": "service",
    "engine": "service",
    "brain": "daemon",
    "swarm": "daemon",
    "mesh": "daemon",
    "orchestrator": "service",
}


def classify(name):
    for k, v in EXEC_TYPE.items():
        if k in name:
            return v
    return "service"


# =========================
# GOVERNANCE RULES (OS CONSTRAINTS)
# =========================
MAX_CONCURRENT = {
    "task": 20,
    "service": 15,
    "daemon": 10,
    "kernel": 5
}

RESTART_POLICY = {
    "task": "never",
    "service": "backoff",
    "daemon": "backoff",
    "kernel": "always"
}

BACKOFF_BASE = 3


# =========================
# STATE ENGINE
# =========================
class State:
    def __init__(self):
        self.processes = {}
        self.counts = defaultdict(int)
        self.restarts = defaultdict(int)
        self.last_start = {}

STATE = State()


# =========================
# CAN WE START THIS?
# =========================
def allowed(name, exec_type):
    if STATE.counts[exec_type] >= MAX_CONCURRENT[exec_type]:
        return False
    return True


# =========================
# LAUNCH PROCESS
# =========================
def launch(path):
    name = os.path.basename(path)
    exec_type = classify(name)

    if not allowed(name, exec_type):
        print(f"⛔ LIMIT HIT [{exec_type}]: {name}")
        return None

    print(f"🚀 START [{exec_type}]: {name}")

    try:
        p = subprocess.Popen(
            ["python", path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        STATE.processes[name] = (p, path, exec_type)
        STATE.counts[exec_type] += 1
        STATE.last_start[name] = time.time()

        return p

    except Exception as e:
        print(f"❌ FAIL {name}: {e}")
        return None


# =========================
# SHOULD RESTART?
# =========================
def should_restart(name, exec_type, code):
    policy = RESTART_POLICY[exec_type]

    if exec_type == "task":
        return False

    if code == 0:
        return False

    if policy == "never":
        return False

    return True


# =========================
# BACKOFF
# =========================
def backoff(name):
    delay = BACKOFF_BASE * (STATE.restarts[name] + 1)
    print(f"⏳ BACKOFF {delay}s → {name}")
    time.sleep(delay)


# =========================
# BOOT ENGINE
# =========================
def boot():
    modules = discover_modules()

    print(f"📦 Modules discovered: {len(modules)}")

    # safety cap for stability
    modules = modules[:25]

    print("\n🧩 INITIAL GOVERNED BOOT (MAX 25)\n")

    # =========================
    # INITIAL LAUNCH
    # =========================
    for m in modules:
        launch(m)
        time.sleep(0.2)

    print("\n🟢 SYSTEMD v4 ACTIVE\n")

    # =========================
    # GOVERNOR LOOP
    # =========================
    while True:
        time.sleep(5)

        for name, (proc, path, exec_type) in list(STATE.processes.items()):

            code = proc.poll()

            if code is None:
                continue

            # process died
            print(f"\n⚠️ DEAD [{exec_type}]: {name} code={code}")

            # cleanup counter
            STATE.counts[exec_type] = max(0, STATE.counts[exec_type] - 1)

            if should_restart(name, exec_type, code):

                STATE.restarts[name] += 1
                backoff(name)

                new_proc = launch(path)

                if new_proc:
                    print(f"🔁 RESTARTED: {name}")
            else:
                print(f"🛑 NO RESTART (policy): {name}")
                STATE.processes.pop(name, None)


if __name__ == "__main__":
    boot()
