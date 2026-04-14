import os
import psutil

LOCK_FILE = "/tmp/omega.lock"

def single_instance():
    if os.path.exists(LOCK_FILE):
        print("[KERNEL] Already running — exiting")
        exit()

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
from core.orchestrator import Orchestrator

if __name__ == "__main__":
    Orchestrator().boot()
