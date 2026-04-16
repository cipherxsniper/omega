import os
import time
import json
import subprocess
import threading

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCK_FILE = os.path.join(BASE_DIR, ".omega_v14.lock")

MODULES = {
    "ml": "python omega_ml_core_v12.py",
    "swarm": "python omega_swarm_v30_synchronized_evolution.py",
    "memory": "python omega_memory_federation_v28.py"
}

STATE_FILE = os.path.join(BASE_DIR, "omega_v14_state.json")


# -----------------------------
# LOCK SYSTEM (NO CRASH / NO /tmp ISSUES)
# -----------------------------
def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = f.read().strip()
            if pid:
                print(f"[V14] Already running (PID {pid}) → exiting")
            return False
        except:
            pass

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True


def release_lock():
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass


# -----------------------------
# AUTONOMOUS CONTROL KERNEL
# -----------------------------
class OmegaV14Kernel:
    def __init__(self):
        self.processes = {}
        self.state = self.load_state()
        self.running = True

    # -----------------------------
    # STATE
    # -----------------------------
    def load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        return {
            "ticks": 0,
            "health": {},
            "last_restart": {}
        }

    def save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    # -----------------------------
    # MODULE CONTROL
    # -----------------------------
    def start_module(self, name, cmd):
        if name in self.processes and self.processes[name].poll() is None:
            return

        print(f"[V14] Starting module: {name}")

        self.processes[name] = subprocess.Popen(
            cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

    def monitor_module(self, name):
        proc = self.processes.get(name)
        if not proc:
            return

        if proc.poll() is not None:
            print(f"[V14] Module crashed: {name} → restarting")
            self.start_module(name, MODULES[name])

    # -----------------------------
    # MAIN LOOP
    # -----------------------------
    def run(self):
        print("[V14] AUTONOMOUS CONTROL KERNEL ONLINE")

        # start all modules
        for name, cmd in MODULES.items():
            self.start_module(name, cmd)

        while self.running:
            self.state["ticks"] += 1

            for name in MODULES:
                self.monitor_module(name)

            self.save_state()

            print(f"[V14] tick {self.state['ticks']} | modules={len(self.processes)}")

            time.sleep(2)


# -----------------------------
# SHUTDOWN SAFETY
# -----------------------------
def shutdown(kernel):
    print("\n[V14] Shutting down safely...")
    kernel.running = False
    release_lock()


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    if not acquire_lock():
        exit()

    kernel = OmegaV14Kernel()

    try:
        kernel.run()
    except KeyboardInterrupt:
        shutdown(kernel)
