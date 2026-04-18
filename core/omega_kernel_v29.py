import time
import importlib

BRAINS = [
    "brains.brain_00",
    "brains.brain_11",
    "brains.brain_22"
]

loaded = []

for b in BRAINS:
    loaded.append(importlib.import_module(b))

print("🧠 OMEGA v29 KERNEL ONLINE")

while True:

    for brain in loaded:
        brain.step()

    time.sleep(0.1)
