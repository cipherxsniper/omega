from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v712 import OmegaKernelV712
from omega_observer_v75 import OmegaObserverV75
from omega_continuity_v712 import OmegaContinuityV712

print("[Ω] booting v7.13 execution contract system...", flush=True)

layer = get_execution_layer()
kernel = OmegaKernelV712(layer)

observer = OmegaObserverV75()
continuity = OmegaContinuityV712()

tick = 0
prev_event = None

while True:

    try:
        packet = kernel.safe_step(tick, {"drift": 40})

        event = packet.get("event", {
            "event_type": "state_update",
            "raw": packet
        })

        state_view = {
            "node": packet.get("node"),
            "trace_len": len(packet.get("trace", [])),
            "event_type": event.get("event_type"),
            "tick": tick
        }

        should_emit, meta = continuity.should_emit(event, state_view)

        if should_emit:
            compressed = continuity.compress_state(state_view)

            narration = observer.narrate(event, packet, state_view)

            print(f"\n[Ω v7.13 | TICK {tick}]", flush=True)
            print("STATE:", compressed, flush=True)
            print("MODE:", meta.get("mode"), flush=True)
            print(narration, flush=True)

        tick += 1
        prev_event = event

    except Exception as e:
        error_event = {
            "event_type": "route_error",
            "raw": str(e),
            "node": None
        }

        print(observer.narrate(error_event, {}, {"tick": tick}), flush=True)
        tick += 1
