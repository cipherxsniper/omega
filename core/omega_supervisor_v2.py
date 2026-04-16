# OMEGA SUPERVISOR v2 (DISTRIBUTED CLUSTER MANAGER)

import time
import subprocess
import threading
from omega_event_router_v2 import ROUTER, start_listener

WORKER_PORTS = [6001, 6002, 6003]

HEARTBEAT = {}
KILL_SWITCH = False


def launch_workers():
    procs = []
    for port in WORKER_PORTS:
        p = subprocess.Popen(["python3", "omega_worker_node.py", str(port)])
        procs.append(p)
    return procs


def monitor_cluster():
    global KILL_SWITCH

    while not KILL_SWITCH:
        time.sleep(5)

        for port in WORKER_PORTS:
            last = HEARTBEAT.get(port, 0)

            if time.time() - last > 10:
                print(f"[Ω SUPERVISOR] worker {port} DOWN → restart")
                subprocess.Popen(["python3", "omega_worker_node.py", str(port)])


def handle_event(event):
    if event["type"] == "heartbeat":
        HEARTBEAT[event["payload"]["port"]] = time.time()


def start():
    print("[Ω SUPERVISOR v2] booting distributed cluster")

    start_listener(5055, handle_event)

    launch_workers()

    threading.Thread(target=monitor_cluster, daemon=True).start()

    while not KILL_SWITCH:
        time.sleep(1)


if __name__ == "__main__":
    start()
