from omega_bootstrap_v75 import get_execution_layer
from omega_bus_v710 import OmegaBusV710
from omega_kernel_v710 import OmegaKernelV710
from omega_observer_v710 import OmegaObserverV710

print("[Ω] booting v7.10 event cognition bus...", flush=True)

layer = get_execution_layer()

bus = OmegaBusV710()
observer = OmegaObserverV710()

kernel = OmegaKernelV710(layer, bus)

bus.subscribe(observer.handle)

tick = 0

while True:

    events = kernel.step(tick, {"drift": 40})

    print(f"\n[Ω v7.10 | TICK {tick}]", flush=True)

    # 🔥 THIS IS THE MISSING PIECE (NARRATION OUTPUT)
    for event in events:
        narration = observer.handle(event)
        print(narration, flush=True)

    tick += 1
