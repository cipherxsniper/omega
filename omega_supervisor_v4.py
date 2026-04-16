# OMEGA SUPERVISOR v4
# Auto-restarting process manager for Omega Core Stack v4

import subprocess
import time
import os
import signal
from pathlib import Path

OMEGA_ROOT = Path(__file__).resolve().parent

BUS_CMD = ["python3", str(OMEGA_ROOT / "omega_event_bus_v4.py")]
WORKER_CMD = ["python3", str(OMEGA_ROOT / "omega_worker_node_v4.py")]


# =========================================================
# PROCESS WRAPPER
# =========================================================
class ManagedProcess:
    def __init__(self, name, cmd):
        self.name = name
        self.cmd = cmd
        self.process = None

    def start(self):
        print(f"[Ω SUPERVISOR] starting {self.name}...")
        self.process = subprocess.Popen(self.cmd)
        print(f"[Ω SUPERVISOR] {self.name} PID={self.process.pid}")

    def alive(self):
        return self.process and self.process.poll() is None

    def restart(self):
        print(f"[Ω SUPERVISOR] restarting {self.name}...")
        self.start()

    def stop(self):
        if self.process:
            print(f"[Ω SUPERVISOR] stopping {self.name}")
            self.process.terminate()


# =========================================================
# SUPERVISOR CORE
# =========================================================
class SupervisorV4:
    def __init__(self):
        self.processes = [
            ManagedProcess("event_bus", BUS_CMD),
            ManagedProcess("worker_node", WORKER_CMD)
        ]
        self.running = True

    def start_all(self):
        for p in self.processes:
            p.start()

    def monitor(self):
        print("[Ω SUPERVISOR v4] monitoring system...")

        while self.running:
            for p in self.processes:
                if not p.alive():
                    print(f"[Ω SUPERVISOR] {p.name} died → restarting")
                    p.restart()

            time.sleep(2)

    def shutdown(self):
        print("\n[Ω SUPERVISOR v4] shutting down...")
        for p in self.processes:
            p.stop()
        self.running = False


# =========================================================
# SIGNAL HANDLING (CTRL+C SAFE STOP)
# =========================================================
SUP = SupervisorV4()

def handle_exit(sig, frame):
    SUP.shutdown()
    exit(0)

signal.signal(signal.SIGINT, handle_exit)


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    print("[Ω SUPERVISOR v4] Autonomous Agent Network ONLINE")

    SUP.start_all()
    SUP.monitor()
