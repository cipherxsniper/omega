from omega_bootstrap_v75 import get_execution_layer
from omega_bus_v710 import OmegaBusV710
from omega_kernel_v710 import OmegaKernelV710

from omega_observer_v711 import OmegaObserverV711
from omega_self_model_v711 import OmegaSelfModelV711

print("[Ω] booting v7.11 cognitive language renderer...", flush=True)

layer = get_execution_layer()

bus = OmegaBusV710()
kernel = OmegaKernelV710(layer, bus)

observer = OmegaObserverV711()
self_model = OmegaSelfModelV711()

bus.subscribe(lambda e: None)

tick = 0


if __name__ == "__main__":

    tick = 0

    while True:

        event = None
        try:
            packet = kernel.step(tick, {"drift": 40})
            event = packet

        except Exception as e:
            event = {
                "event_type": "route_error",
                "raw": str(e)
            }

        state_view = {
            "node": getattr(packet, "node", None) if 'packet' in locals() else None,
            "event_type": event.get("event_type") if isinstance(event, dict) else None,
            "tick": tick
        }

        should_emit, meta = continuity.should_emit(event, state_view)

        if should_emit:

            compressed = continuity.compress_state(state_view)
            narration = observer.narrate(event)

            print(f"\n[Ω v7.12 | TICK {tick}]", flush=True)
            print("STATE:", compressed, flush=True)
            print("MODE:", meta.get("mode"), flush=True)
            print(narration, flush=True)

        else:
            print(f"[Ω v7.12 | TICK {tick}] ⟲ suppressed", flush=True)

        tick += 1

