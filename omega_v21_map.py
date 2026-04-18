import os
import time
from omega_v21_core import omega_field

def render():
    os.system("clear")
    print("🧠 OMEGA v21 ATTRACTOR MAP\n")

    for k, v in omega_field["attractor_map"].items():
        bar = "█" * min(int(v), 40)
        print(f"{k:<25} {bar} {v}")

while True:
    render()
    time.sleep(1)
