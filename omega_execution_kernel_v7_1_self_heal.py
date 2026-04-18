import subprocess
import time
import os

CORE_NODES = [
    "omega_bus",
    "node_memory",
    "node_goal",
    "node_attention",
    "node_stability"
]

processes = {}

def start_node(node):
    file = f"{node}.py"
    if not os.path.exists(file):
        print(f"⚠ missing: {node}")
        return

    p = subprocess.Popen(["python", file])
    processes[node] = p
    print(f"🚀 started: {node}")

def monitor():
    while True:
        for node, proc in list(processes.items()):
            if proc.poll() is not None:
                print(f"❌ crashed: {node} → restarting")
                start_node(node)

        time.sleep(2)

if __name__ == "__main__":
    print("🧠 OMEGA v7.1 SELF-HEALING KERNEL")

    for n in CORE_NODES:
        start_node(n)

    monitor()
