import os
import time
import subprocess

print("[Ω] OMEGA OS SHELL BOOTING...\n")

time.sleep(1)

# 1. registry
os.system("python3 omega_neural_registry_v9.py")

# 2. start balancer in background
subprocess.Popen(["python3", "omega_swarm_balancer_v9.py"])

time.sleep(1)

# 3. open chat
os.system("python3 omega_chat_assistant_v9.py")
