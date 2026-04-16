from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79

from omega_event_contract_v715 import OmegaEventContractV715
from omega_event_bus_v716 import OmegaEventBusV716
from omega_cognition_graph_v716 import OmegaCognitionGraphV716

from omega_scheduler_v717 import OmegaSchedulerV717
from omega_memory_decay_v717 import OmegaMemoryDecayV717

print("[Ω] booting v7.17 scheduler + memory decay layer...", flush=True)

layer = get_execution_layer()
kernel = OmegaKernelV79(layer)

bus = OmegaEventBusV716()
graph = OmegaCognitionGraphV716()
scheduler = OmegaSchedulerV717()
memory = OmegaMemoryDecayV717()

tick = 0


def handle_event(event):
    node = event.get("node")
    if node:
        graph.upsert_node(node, event)
        memory.write(node, event)


bus.subscribe("success", handle_event)
bus.subscribe("route_error", handle_event)
bus.subscribe("contract_violation", handle_event)


while True:

    raw = kernel.step(tick, {"drift": 40})

    if isinstance(raw, dict) and raw.get("ok"):
        data = raw.get("data", {})

        event = OmegaEventContractV715.build(
            tick=tick,
            event_type="success",
            node=data.get("node", "unknown"),
            raw=raw,
            state={},
            severity=0.5
        )
    else:
        event = OmegaEventContractV715.build(
            tick=tick,
            event_type="route_error",
            node=None,
            raw=raw,
            state={},
            severity=1.0
        )

    event = OmegaEventContractV715.safe(event)

    # 1. schedule event
    scheduler.push(event)

    # 2. process only highest priority event
    active = scheduler.pop()

    # 3. publish system-wide
    bus.publish(active)

    # 4. decay memory each tick
    memory.decay()

    snapshot = graph.snapshot()

    print(f"\n[Ω v7.17 | TICK {tick}]", flush=True)
    print("QUEUE SIZE:", scheduler.size(), flush=True)
    print("MEMORY NODES:", len(snapshot["nodes"]), flush=True)

    tick += 1
