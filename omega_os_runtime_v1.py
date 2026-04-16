import os
import time
import json
import subprocess
from collections import defaultdict

# =========================
# OMEGA OS RUNTIME v1
# =========================

BASE_DIR = os.path.dirname(__file__)
STATE_FILE = os.path.join(BASE_DIR, "omega_os_runtime_state.json")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

CHECK_INTERVAL = 8
MAX_RESTARTS = 3


class RuntimeState:
    def __init__(self):
        self.state = {
            "processes": {},
            "restarts": {},
            "health": {},
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

    def update_process(self, name, pid):
        self.state["processes"][name] = pid
        self.state["health"][name] = "running"

    def mark_dead(self, name):
        self.state["health"][name] = "dead"

    def inc_restart(self, name):
        self.state["restarts"][name] = self.state["restarts"].get(name, 0) + 1
        return self.state["restarts"][name]


class ProcessManager:
    def __init__(self, state: RuntimeState):
        self.state = state
        self.procs = {}

    def launch(self, module):
        log_path = os.path.join(LOG_DIR, f"{module}.log")

        with open(log_path, "a") as log:
            p = subprocess.Popen(
                ["python", module],
                stdout=log,
                stderr=log,
                preexec_fn=os.setpgrp
            )

        self.procs[module] = p
        self.state.update_process(module, p.pid)

        print(f"🚀 LAUNCH: {module} PID={p.pid}")

    def alive(self, module):
        p = self.procs.get(module)
        return p and p.poll() is None

    def restart(self, module):
        count = self.state.inc_restart(module)

        if count > MAX_RESTARTS:
            print(f"🛑 KILL LIMIT REACHED: {module}")
            self.state.mark_dead(module)
            return

        print(f"♻️ RESTART [{count}]: {module}")
        self.launch(module)


class OmegaRuntime:
    def __init__(self):
        self.state = RuntimeState()
        self.pm = ProcessManager(self.state)

        # CORE CONTROL LAYER (ONLY STABLE SYSTEMS)
        self.core = [
            "omega_unified_kernel_v15.py",
            "omega_identity_kernel_v25.py",
            "omega_execution_engine_v7.py",
            "omega_meta_brain_v10.py",
            "omega_unified_brain_v22.py",
            "omega_swarm_memory_bridge_v9.py",
            "omega_mesh_superintelligence_v12.py",
            "omega_process_supervisor_v2.py"
        ]

    def boot(self):
        print("\n🧠 OMEGA OS RUNTIME v1 ONLINE\n")

        # STEP 1: launch core
        for m in self.core:
            self.pm.launch(m)
            time.sleep(0.5)

        # STEP 2: runtime loop
        while True:
            self.state.state["tick"] += 1

            for module in list(self.pm.procs.keys()):
                if not self.pm.alive(module):
                    print(f"⚠️ DEAD DETECTED: {module}")
                    self.state.mark_dead(module)
                    self.pm.restart(module)

            if self.state.state["tick"] % 5 == 0:
                print(f"🟢 RUNTIME TICK {self.state.state['tick']} ACTIVE")

            self.state.save()
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    OmegaRuntime().boot()
