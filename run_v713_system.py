from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79
from omega_observer_v75 import OmegaObserverV75

print("[Ω] booting v7.13 unified kernel binding...", flush=True)

layer = get_execution_layer()
kernel = OmegaKernelV79(layer)
observer = OmegaObserverV75()

tick = 0

while True:
    try:
        packet = kernel.step(tick, {"drift": 40})

        event = {
            "event_type": "state_update",
            "raw": packet
        }

        print(f"\n[Ω v7.13 | TICK {tick}]", flush=True)
        print("NODE:", packet.get("node"), flush=True)
        print("TRACE:", len(packet.get("trace", [])), flush=True)

        print(observer.narrate(event, packet), flush=True)

        tick += 1

    except Exception as e:
        err_event = {
            "event_type": "route_error",
            "raw": str(e)
        }

        print(observer.narrate(err_event, {}), flush=True)
        tick += 1
