from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79
from omega_observer_guard_v79 import ObserverGuardV79
from omega_self_model_v78 import OmegaSelfModelV78

print("[Ω] booting v7.9 strict cognition kernel...", flush=True)

layer = get_execution_layer()
kernel = OmegaKernelV79(layer)

observer = ObserverGuardV79(__import__("omega_observer_v75").OmegaObserverV75())

self_model = OmegaSelfModelV78()
prev = None
tick = 0

while True:

    packet = kernel.safe_step(tick, {"drift": 40})

    curr = self_model.snapshot(layer, packet, tick)

    print(f"\n[Ω v7.9 | TICK {tick}]", flush=True)
    print("NODE:", packet["node"], flush=True)
    print("TRACE LENGTH:", len(packet["trace"]), flush=True)

    print(observer.narrate(prev, curr), flush=True)

    prev = curr
    tick += 1
