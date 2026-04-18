import subprocess
import time
import json
import os

from omega_registry_v11 import snapshot
from omega_observer_translator_v11 import translate_registry

print("🧠 OMEGA v11 BOOTSTRAP ONLINE")

# Start core processes ONCE (no duplication)
processes = [
    "python3 ~/Omega/omega_observer.py",
    "node ~/Omega/core/observer.js",
    "node ~/Omega/core/heartbeat.js",
    "python3 ~/Omega/python/heartbeat.py"
]

for cmd in processes:
    subprocess.Popen(cmd, shell=True)

time.sleep(2)

while True:
    reg = snapshot()
    print("\n" + translate_registry(reg))
    time.sleep(5)
