import subprocess
import time

print("🧠 OMEGA v12 INITIALIZING...")

NODES = {
    "observer": "python3 ~/Omega/omega_observer_v12.py",
    "memory": "python3 ~/Omega/omega_memory_fusion_v12.py",
    "reinforce": "python3 ~/Omega/omega_reinforcement_v12.py"
}

processes = []

for name, cmd in NODES.items():
    print(f"🚀 Starting {name}")
    processes.append(subprocess.Popen(cmd, shell=True))

print("✅ OMEGA v12 ONLINE")

while True:
    time.sleep(10)
