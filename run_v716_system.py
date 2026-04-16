from omega_event_bus_v716 import OmegaEventBusV716
from omega_cognition_graph_v716 import OmegaCognitionGraphV716

from omega_event_contract_v715 import OmegaEventContractV715
from omega_kernel_v79 import OmegaKernelV79
from omega_bootstrap_v75 import get_execution_layer

print("[Ω] booting v7.16 event bus + cognition graph...", flush=True)

bus = OmegaEventBusV716()
graph = OmegaCognitionGraphV716()

layer = get_execution_layer()
kernel = OmegaKernelV79(layer)

tick = 0


def handle_success(event):
    node = event.get("node")
    if node:
        graph.upsert_node(node, event)

def handle_route_error(event):
    node = event.get("node")
    if node:
        graph.upsert_node(node, event)


bus.subscribe("success", handle_success)
bus.subscribe("route_error", handle_route_error)


while True:

    raw = kernel.step(tick, {"drift": 40})

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

    event = OmegaEventContractV715.safe(event)

    # PUBLISH INTO GLOBAL SYSTEM
    bus.publish(event)

    snapshot = graph.snapshot()

    print(f"\n[Ω v7.16 | TICK {tick}]", flush=True)
    print("EVENT:", event["event_type"], flush=True)
    print("GRAPH NODES:", len(snapshot["nodes"]), flush=True)

    tick += 1
