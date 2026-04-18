from omega_v21_core import omega_field
from omega_field_dynamics_patch import apply_decay, normalize_pressure
from omega_competition_patch import redistribute_pressure
import time

while True:

    # decay field energy
    apply_decay(omega_field["attractor_map"])

    # competition between pathways
    redistribute_pressure(omega_field["attractor_map"])

    # normalize field
    normalized = normalize_pressure(omega_field["attractor_map"])

    print("\n🌌 OMEGA DYNAMIC FIELD")

    for k, v in sorted(normalized.items(), key=lambda x: -x[1]):
        bar = "█" * int(v * 50)
        print(f"{k:<25} {bar} {v:.3f}")

    time.sleep(0.6)
