import os
import time
import json
import subprocess
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROCESSES = {
    "ml_core": "python omega_ml_core_v12.py",
    "swarm_v30": "python omega_swarm_v30_synchronized_evolution.py",
    "internet_mesh": "python omega_swarm_v27_internet_mesh.py",
    "memory_federation": "python omega_memory_federation_v28.py",
    "self_patch": "python omega_self_patch_v29_engine.py"
}

LOG_DIR = os.path.join(BASE_DIR, "logs")
PID_FILE = os.path.join(BASE_DIR, "omega_supervisor_pids.json")

CHECK_INTERVAL = 5


# -----------------------------
# UTILS
# -----------------------------
def now():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dirs():
    os.makedirs(LOG_DIR, exist_ok=True)


def log(name, msg):
    line = f"[{now()}] [{name}] {msg}"
    print(line)

    with open(os.path.join(LOG_DIR, f"{name}.log"), "a") as f:
        f.write(line + "\n")


def save_pids(pids):
    with open(PID_FILE, "w") as f:
        json.dump(pids, f, indent=2)


def load_pids():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


# -----------------------------
# PROCESS CONTROL
# -----------------------------
def start_process(name, cmd):
    log(name, f"STARTING → {cmd}")

    with open(os.path.join(LOG_DIR, f"{name}.out"), "a") as out:
        process = subprocess.Popen(
            cmd.split(),
            stdout=out,
            stderr=out
        )

    return process.pid


def is_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except:
        return False


# -----------------------------
# SUPERVISOR CORE
# -----------------------------
class OmegaSupervisorV13:
    def __init__(self):
        ensure_dirs()
        self.pids = load_pids()

    def launch_all(self):
        for name, cmd in PROCESSES.items():

            pid = self.pids.get(name)

            if pid and is_alive(pid):
                log(name, f"ALREADY RUNNING (PID {pid})")
                continue

            pid = start_process(name, cmd)
            self.pids[name] = pid
            save_pids(self.pids)

    def monitor(self):
        while True:
            for name, cmd in PROCESSES.items():

                pid = self.pids.get(name)

                if not pid or not is_alive(pid):
                    log(name, "DEAD → RESTARTING")
                    new_pid = start_process(name, cmd)
                    self.pids[name] = new_pid
                    save_pids(self.pids)

                else:
                    log(name, f"HEALTHY (PID {pid})")

            time.sleep(CHECK_INTERVAL)


# -----------------------------
# BOOT
# -----------------------------
if __name__ == "__main__":
    sup = OmegaSupervisorV13()

    log("SUPERVISOR", "OMEGA v13 DAEMON STARTING")

    sup.launch_all()
    sup.monitor()
