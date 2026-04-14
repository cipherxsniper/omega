import os
import time
import json
import subprocess
from datetime import datetime, timezone

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROCESSES = {
    "ml_core": ["python", "omega_ml_core_v12.py"],
    "swarm_v30": ["python", "omega_swarm_v30_synchronized_evolution.py"],
    "internet_mesh": ["python", "omega_swarm_v27_internet_mesh.py"],
    "memory_federation": ["python", "omega_memory_federation_v28.py"],
    "self_patch": ["python", "omega_self_patch_v29_engine.py"]
}

LOG_DIR = os.path.join(BASE_DIR, "logs")
PID_FILE = os.path.join(BASE_DIR, "omega_supervisor_pids.json")

CHECK_INTERVAL = 5


# -----------------------------
# UTILS
# -----------------------------
def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)


def log(name, msg):
    line = f"[{now()}] [{name}] {msg}"
    print(line)

    with open(os.path.join(LOG_DIR, f"{name}.log"), "a") as f:
        f.write(line + "\n")


def save_pids(pids):
    try:
        with open(PID_FILE, "w") as f:
            json.dump(pids, f, indent=2)
    except Exception as e:
        log("SUPERVISOR", f"PID SAVE ERROR: {e}")


def load_pids():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


def is_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except:
        return False


# -----------------------------
# PROCESS CONTROL
# -----------------------------
def start_process(name, cmd):
    log(name, f"STARTING → {' '.join(cmd)}")

    log_file = open(os.path.join(LOG_DIR, f"{name}.out"), "a")

    process = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=log_file,
        cwd=BASE_DIR
    )

    return process.pid


# -----------------------------
# SUPERVISOR CORE
# -----------------------------
class OmegaSupervisorV14:
    def __init__(self):
        ensure_dirs()
        self.pids = load_pids()
        self.last_restart = {}

    def launch_all(self):
        for name, cmd in PROCESSES.items():

            pid = self.pids.get(name)

            if pid and is_alive(pid):
                log(name, f"ALREADY RUNNING (PID {pid})")
                continue

            new_pid = start_process(name, cmd)
            self.pids[name] = new_pid
            save_pids(self.pids)

    def can_restart(self, name):
        # prevents restart spam loops
        last = self.last_restart.get(name, 0)
        return (time.time() - last) > 3

    def monitor(self):
        while True:
            for name, cmd in PROCESSES.items():

                pid = self.pids.get(name)

                if not pid or not is_alive(pid):

                    if self.can_restart(name):
                        log(name, "DEAD → RESTARTING")
                        new_pid = start_process(name, cmd)
                        self.pids[name] = new_pid
                        self.last_restart[name] = time.time()
                        save_pids(self.pids)
                    else:
                        log(name, "RESTART BLOCKED (cooldown)")

                else:
                    log(name, f"HEALTHY (PID {pid})")

            time.sleep(CHECK_INTERVAL)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    sup = OmegaSupervisorV14()

    log("SUPERVISOR", "OMEGA v14 DAEMON STARTING")

    sup.launch_all()
    sup.monitor()
