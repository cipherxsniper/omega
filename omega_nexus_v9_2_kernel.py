import subprocess
import time
import os

PROCESSES = []

def start(name, cmd):
    print(f"[Ω KERNEL] starting {name}")
    p = subprocess.Popen(cmd)
    PROCESSES.append(p)
    return p

def main():

    print("[Ω NEXUS v9.2 KERNEL STARTING]")

    os.makedirs("logs", exist_ok=True)

    # CORE SYSTEMS (ONLY ONCE)
    start("BUS", ["python3", "omega_neural_bus_v9.py"])
    start("MESH", ["python3", "omega_cognitive_mesh_v9.py"])
    start("NODES", ["python3", "omega_node_runtime_v9.py"])

    # CONTROL SYSTEMS
    start("BALANCER", ["python3", "omega_swarm_balancer_v9_bus.py"])

    # CHAT CONTROLLER (interactive OR API mode, not daemon input spam)
    start("CHAT", ["python3", "omega_chat_controller_v9_2.py"])

    print("[Ω NEXUS v9.2 ONLINE]")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print("[Ω KERNEL] shutting down...")

        for p in PROCESSES:
            p.terminate()

if __name__ == "__main__":
    main()
