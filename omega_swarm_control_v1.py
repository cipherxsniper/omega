import os
import signal
import time
import json
import multiprocessing

PID_FILE = "omega_swarm_pids.json"


# =========================
# 🧠 PID TRACKER
# =========================
def save_pid(pid_list):
    with open(PID_FILE, "w") as f:
        json.dump(pid_list, f)


def load_pid():
    if not os.path.exists(PID_FILE):
        return []
    with open(PID_FILE, "r") as f:
        return json.load(f)


# =========================
# ⚡ SHUTDOWN SYSTEM
# =========================
def kill_swarm():

    pids = load_pid()

    print("[Ω-CONTROL] shutting down swarm...")

    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"[Ω-CONTROL] stopped process {pid}")
        except:
            pass

    print("[Ω-CONTROL] swarm offline")


# =========================
# 🚀 LAUNCH WRAPPER
# =========================
def launch(command: str):

    pid = os.fork()

    if pid == 0:
        os.execl("/bin/bash", "bash", "-c", command)

    return pid


# =========================
# 🧠 MAIN CONTROL MODE
# =========================
if __name__ == "__main__":

    print("===================================")
    print("Ω SWARM CONTROL SYSTEM v1")
    print("===================================")

    while True:

        cmd = input("\nΩ-CONTROL > ").strip()

        if cmd == "start":

            pids = []

            pids.append(launch("python omega_mesh_os_v11.py"))
            pids.append(launch("python omega_brain_bridge_v1.py"))
            pids.append(launch("python omega_kernel_v5.py"))

            save_pid(pids)

            print("[Ω-CONTROL] swarm started")

        elif cmd == "stop":
            kill_swarm()

        elif cmd == "status":
            print(load_pid())

        elif cmd == "exit":
            break

        else:
            print("commands: start | stop | status | exit")
