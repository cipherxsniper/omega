from omega_v21_core import *
import time

nodes = [
    QuantumNode("attention"),
    QuantumNode("goal"),
    QuantumNode("memory"),
    QuantumNode("stability")
]

print("🧠 OMEGA v21 RUNNING\n")

while True:
    packet, result = run_cycle(nodes)

    print("📦 Packet:", packet["id"])
    print("🔁 Routed To:", result)
    print("📊 Attractors:", omega_field["attractor_map"])
    print("-" * 50)

    time.sleep(0.8)
