import subprocess
import time

print("🧠 OMEGA v13 NEURAL SYSTEM ONLINE")

NODES = [
    "python3 ~/Omega/omega_observer_v13.py",
    "python3 ~/Omega/omega_self_heal_v13.py"
]

for cmd in NODES:
    subprocess.Popen(cmd, shell=True)

time.sleep(2)

print("🌐 Memory + Learning Loop ACTIVE")

while True:
    time.sleep(10)
