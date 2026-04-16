from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79
from omega_observer_v79 import OmegaObserverV79
from omega_self_model_v79 import OmegaSelfModelV79

print("[Ω] booting v7.9 strict cognition kernel...", flush=True)

layer = get_execution_layer()
kernel = OmegaKernelV79(layer)

observer = OmegaObserverV79()
self_model = OmegaSelfModelV79()

tick = 0
prev = None

while True:

    event = kernel.safe_step(tick, {"drift": 40})

    curr = self_model.snapshot(layer, event, tick)

    print(f"\n[Ω v7.9 | TICK {tick}]", flush=True)
    print("EVENT:", event["event_type"], flush=True)

    print(observer.narrate(event), flush=True)
    print(self_model.narrate(prev, curr), flush=True)

    prev = curr
    tick += 1
