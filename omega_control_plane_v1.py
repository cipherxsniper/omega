import os
import time
import json
import signal
import subprocess
from collections import defaultdict

# =========================
# OMEGA CONTROL PLANE v1
# =========================

BASE_DIR = os.path.dirname(__file__)
STATE_FILE = os.path.join(BASE_DIR, "omega_control_plane_state.json")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

CHECK_INTERVAL = 5

# -------------------------
# SYSTEM POLICY (CORE RULES)
# -------------------------

MAX_TOTAL_PROCESSES = 60
MAX_PER_CATEGORY = {
    "kernel": 8,
    "brain": 10,
    "swarm": 10,
    "mesh": 10,
    "memory": 8,
    "engine": 8,
    "default": 6
}

PRIORITY_ORDER = [
    "kernel",
    "identity",
    "execution",
    "brain",
    "swarm",
    "mesh",
    "memory",
    "engine"
]


# -------------------------
# CONTROL STATE
# -------------------------

class ControlState:
    def __init__(self):
        self.state = {
            "processes": {},   # name -> pid
            "category_map": {}, # name -> category
            "tick": 0
        }
        self.load()

    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    self.state = json.load(f)
            except:
                pass

    def save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)


# -------------------------
# CLASSIFIER
# -------------------------

def classify(module_name: str) -> str:
    name = module_name.lower()

    if "kernel" in name:
        return "kernel"
    if "brain" in name:
        return "brain"
    if "swarm" in name:
        return "swarm"
    if "mesh" in name:
        return "mesh"
    if "memory" in name:
        return "memory"
    if "engine" in name:
        return "engine"
    if "identity" in name:
        return "kernel"

    return "default"


# -------------------------
# PROCESS CONTROL LAYER
# -------------------------

class ProcessControl:
    def __init__(self, state: ControlState):
        self.state = state
        self.procs = {}

    def count_by_category(self):
        counts = defaultdict(int)
        for name in self.state.state["category_map"].values():
            counts[name] += 1
        return counts

    def can_start(self, category):
        counts = self.count_by_category()

        if len(self.procs) >= MAX_TOTAL_PROCESSES:
            return False

        limit = MAX_PER_CATEGORY.get(category, MAX_PER_CATEGORY["default"])
        return counts[category] < limit

    def launch(self, module):
        category = classify(module)

        if not self.can_start(category):
            print(f"⛔ BLOCKED ({category} limit): {module}")
            return

        log_path = os.path.join(LOG_DIR, f"{module}.log")

        with open(log_path, "a") as log:
            p = subprocess.Popen(
                ["python", module],
                stdout=log,
                stderr=log,
                preexec_fn=os.setpgrp
            )

        self.procs[module] = p
        self.state.state["processes"][module] = p.pid
        self.state.state["category_map"][module] = category

        print(f"🚀 LAUNCH [{category}]: {module} PID={p.pid}")

    def kill(self, module):
        p = self.procs.get(module)
        if p:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                print(f"🛑 KILLED: {module}")
            except:
                pass


# -------------------------
# CONTROL PLANE CORE
# -------------------------

class OmegaControlPlane:
    def __init__(self):
        self.state = ControlState()
        self.pc = ProcessControl(self.state)

        # SAFE CORE SET (NO EXPLOSION RISK)
        self.core = [
            "omega_unified_kernel_v15.py",
            "omega_identity_kernel_v25.py",
            "omega_execution_engine_v7.py",
            "omega_meta_brain_v10.py",
            "omega_unified_brain_v22.py",
            "omega_swarm_memory_bridge_v9.py",
            "omega_mesh_superintelligence_v12.py",
            "omega_process_supervisor_v2.py",
            "omega_os_runtime_v1.py"
        ]

    def boot(self):
        print("\n🧠 OMEGA CONTROL PLANE v1 ONLINE\n")

        # STEP 1: ordered boot (priority aware)
        for module in self.core:
            self.pc.launch(module)
            time.sleep(0.6)

        # STEP 2: enforcement loop
        while True:
            self.state.state["tick"] += 1

            # enforce system limits continuously
            if len(self.pc.procs) > MAX_TOTAL_PROCESSES:
                print("⚠️ SYSTEM OVERLOAD — throttling required")

            # health scan
            for module, p in list(self.pc.procs.items()):
                if p.poll() is not None:
                    print(f"⚠️ DEAD PROCESS: {module}")
                    self.pc.launch(module)

            if self.state.state["tick"] % 10 == 0:
                print(f"🟢 CONTROL PLANE TICK {self.state.state['tick']}")

            self.state.save()
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    OmegaControlPlane().boot()
