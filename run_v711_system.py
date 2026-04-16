from omega_bootstrap_v75 import get_execution_layer

print("[Ω] booting v7.11 safe runtime...", flush=True)

def safe_imports():
    from omega_observer_v75 import OmegaObserverV75
    from omega_continuity_v712 import OmegaContinuityV712
    from omega_self_model_v78 import OmegaSelfModelV78
    return OmegaObserverV75, OmegaContinuityV712, OmegaSelfModelV78


def main():
    # --- ALWAYS initialize inside runtime boundary ---
    OmegaObserverV75, OmegaContinuityV712, OmegaSelfModelV78 = safe_imports()

    layer = get_execution_layer()

    observer = OmegaObserverV75()
    continuity = OmegaContinuityV712()
    self_model = OmegaSelfModelV78()

    prev = None
    tick = 0

    while True:
        try:
            packet = layer.route("temporal", {"drift": 40}, steps=4)

            event = {
                "event_type": "state_update",
                "node": packet.get("final_node"),
                "trace": packet.get("trace", []),
                "raw": packet,
            }

            state_view = {
                "node": event["node"],
                "event_type": event["event_type"],
                "tick": tick
            }

            should_emit, meta = continuity.should_emit(event, state_view)

            if should_emit:
                compressed = continuity.compress_state(state_view)

                curr = self_model.snapshot(layer, packet, tick)

                print(f"\n[Ω v7.11 | TICK {tick}]", flush=True)
                print("STATE:", compressed, flush=True)
                print("MODE:", meta.get("mode", "default"), flush=True)

                print(observer.narrate(event, prev, curr), flush=True)

                prev = curr
            else:
                print(f"[Ω v7.11 | TICK {tick}] ⟲ suppressed", flush=True)

            tick += 1

        except Exception as e:
            # CRASH PREVENTION LAYER
            error_event = {
                "event_type": "route_error",
                "raw": str(e),
                "node": None
            }

            print("\n⚠️ Omega runtime exception captured:", flush=True)
            print(observer.narrate(error_event, prev, None), flush=True)


# === v7.12 RUNTIME SAFETY GUARANTEE ===
def _bootstrap_runtime():
    global continuity, observer, self_model, kernel

    from omega_continuity_v712 import OmegaContinuityV712
    from omega_self_model_v78 import OmegaSelfModelV78

    continuity = OmegaContinuityV712()
    self_model = OmegaSelfModelV78()

    # SAFE observer import (defensive)
    mod = __import__("omega_observer_v75")
    observer = getattr(mod, "OmegaObserverV75", None) or getattr(mod, "OmegaOmegaObserverV75", None)

    if observer is None:
        raise Exception("[BOOT FAILURE] No valid observer found")

    observer = observer()

    return True


def _safe_event(event):
    if event is None:
        return {"event_type": "null_event", "raw": None}

    if not isinstance(event, dict):
        return {"event_type": "type_error", "raw": str(event)}

    if "event_type" not in event:
        event["event_type"] = "unknown"

    return event


# === v7.12 SAFE MAIN LOOP WRAPPER ===
if __name__ == "__main__":
    print("[Ω] booting v7.12 safe runtime...", flush=True)

    _bootstrap_runtime()

    tick = 0

    while True:
        try:
            packet = kernel.step(tick, {"drift": 40})

            event = _safe_event(packet)

            state_view = {
                "node": packet.get("node") if isinstance(packet, dict) else "unknown",
                "event_type": event.get("event_type"),
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

        except Exception as e:
            print(f"[Ω ERROR SAFE-CATCH] {e}", flush=True)

