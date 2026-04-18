from omega_v21_core import *
from omega_v21_field_patch import decay_field, normalize_field
import time

nodes = [
    QuantumNode("attention"),
    QuantumNode("goal"),
    QuantumNode("memory"),
    QuantumNode("stability")
]

print("🧠 OMEGA v21 LIVING FIELD ONLINE\n")

while True:

    packet, result = run_cycle(nodes)

    # 🔁 FIELD EVOLUTION (CRITICAL ADDITION)
    decay_field(omega_field["attractor_map"])
    normalized = normalize_field(omega_field["attractor_map"])

    print("📦 Packet:", packet["id"])
    print("🔁 Routed To:", result)

    print("\n🌌 FIELD INTENSITY MAP")
    for k, v in sorted(normalized.items(), key=lambda x: -x[1]):
        bar = "█" * int(v * 40)
        print(f"{k:<25} {bar} {v:.3f}")

    print("-" * 60)

    time.sleep(0.7)
