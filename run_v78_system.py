# =========================================================
# OMEGA v7.8 — UNIFIED COGNITION KERNEL (SINGLE CONTRACT)
# =========================================================

from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v78 import OmegaKernelV78
from omega_observer_v78 import OmegaObserverV78
from omega_self_model_v78 import OmegaSelfModelV78

print("[Ω] booting v7.8 unified cognition kernel...", flush=True)

# -------------------------
# EXECUTION LAYER
# -------------------------
layer = get_execution_layer()

# -------------------------
# CORE SYSTEMS
# -------------------------
kernel = OmegaKernelV78(layer)
observer = OmegaObserverV78()
self_model = OmegaSelfModelV78()

# -------------------------
# STATE
# -------------------------
tick = 0
prev_model = None

# =========================================================
# MAIN COGNITION LOOP
# =========================================================
while True:

    # 1. EXECUTE ONE COGNITION STEP (UNIFIED CONTRACT OUTPUT)
    packet = kernel.step(tick, {"drift": 40})

    # 2. OBSERVE SYSTEM STATE (NO GUESSING, PURE CONTRACT)
    print("\n========================================", flush=True)
    print(f"[Ω v7.8 | TICK {tick}]", flush=True)
    print(observer.narrate(packet), flush=True)

    # 3. SELF-MODEL (META AWARENESS LAYER)
    current_model = self_model.snapshot(packet)
    print(self_model.narrate(prev_model, current_model), flush=True)

    # 4. UPDATE STATE
    prev_model = current_model
    tick += 1
