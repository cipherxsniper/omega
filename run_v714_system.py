from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79
from omega_observer_v75 import OmegaObserverV75
from omega_contract_v714 import OmegaContractV714
from omega_execution_gate_v714 import OmegaExecutionGateV714

print("[Ω] booting v7.14 unified execution contract layer...", flush=True)

# --- SINGLE SOURCE OF TRUTH ---
layer = get_execution_layer()
kernel = OmegaExecutionGateV714(OmegaKernelV79(layer))
observer = OmegaObserverV75()

tick = 0

while True:

    # 1. RAW EXECUTION
    raw = kernel.step(tick, {"drift": 40})

    if not raw["ok"]:
        event = {
            "event_type": "route_error",
            "node": None,
            "tick": tick,
            "raw": raw["error"]
        }
    else:
        node = raw["data"].get("node", "unknown")

        event = OmegaContractV714.normalize(
            tick,
            node,
            raw["data"]
        )

    # 2. VALIDATION
    valid, err = OmegaContractV714.validate(event)

    if not valid:
        event = {
            "event_type": "contract_violation",
            "node": None,
            "tick": tick,
            "raw": err
        }

    # 3. OUTPUT
    print(f"\n[Ω v7.14 | TICK {tick}]", flush=True)
    print("EVENT:", event["event_type"], flush=True)
    print("NODE:", event.get("node"), flush=True)

    print(observer.narrate(event, raw), flush=True)

    tick += 1
