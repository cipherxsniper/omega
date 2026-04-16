from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79

from omega_event_contract_v715 import OmegaEventContractV715
from omega_observer_guard_v715 import ObserverGuardV715
from omega_self_model_v78 import OmegaSelfModelV78

print("[Ω] booting v7.15 strict event contract system...", flush=True)

layer = get_execution_layer()
kernel = OmegaKernelV79(layer)

observer = ObserverGuardV715(__import__("omega_observer_v75").OmegaObserverV75())
self_model = OmegaSelfModelV78()

tick = 0
prev = None

while True:

    raw = kernel.step(tick, {"drift": 40})

    # normalize kernel output into contract
    if isinstance(raw, dict) and raw.get("ok"):
        data = raw.get("data", {})
        event = OmegaEventContractV715.build(
            tick=tick,
            event_type="success",
            node=data.get("node", "unknown"),
            raw=raw,
            state={}
        )
    else:
        event = OmegaEventContractV715.build(
            tick=tick,
            event_type="route_error",
            node=None,
            raw=raw,
            state={}
        )

    # enforce contract BEFORE observer sees it
    event = OmegaEventContractV715.safe(event)

    field = {
        "memory": getattr(layer, "memory", {})
    }

    curr = self_model.snapshot(layer, event, tick)

    print(f"\n[Ω v7.15 | TICK {tick}]", flush=True)
    print("TYPE:", event["event_type"], flush=True)
    print("NODE:", event["node"], flush=True)

    print(observer.narrate(event, raw, field), flush=True)

    prev = curr
    tick += 1
