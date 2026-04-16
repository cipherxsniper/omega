from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79

from omega_event_contract_v715 import OmegaEventContractV715
from omega_event_bus_v716 import OmegaEventBusV716
from omega_cognition_graph_v716 import OmegaCognitionGraphV716

from omega_scheduler_v717 import OmegaSchedulerV717
from omega_memory_decay_v717 import OmegaMemoryDecayV717

from omega_attention_v718 import OmegaAttentionV718
from omega_predictor_v718 import OmegaPredictorV718

from omega_meta_observer_v719 import OmegaMetaObserverV719

print("[Ω] booting v7.19 meta-observer self-reflection layer...", flush=True)

layer = get_execution_layer()
kernel = OmegaKernelV79(layer)

bus = OmegaEventBusV716()
graph = OmegaCognitionGraphV716()
scheduler = OmegaSchedulerV717()
memory = OmegaMemoryDecayV717()

attention = OmegaAttentionV718()
predictor = OmegaPredictorV718()
meta = OmegaMetaObserverV719()

tick = 0


def handle(event):
    node = event.get("node")
    if node:
        graph.upsert_node(node, event)
        memory.write(node, event)
        attention.update_attention(event)


bus.subscribe("success", handle)
bus.subscribe("route_error", handle)
bus.subscribe("contract_violation", handle)


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

    # ATTENTION
    attn = attention.score_event(event, graph.snapshot())

    # PREDICTION
    risk = predictor.predict_failure(event, graph.snapshot())
    risk_level = predictor.classify(risk)

    # SCHEDULING
    scheduler.push({
        **event,
        "attention": attn,
        "risk": risk_level
    })

    active = scheduler.pop()

    bus.publish(active)

    memory.decay()
    attention.decay_attention()

    # 🧠 META LAYER (SELF-REFLECTION)
    stability = meta.score_stability(active, attn, risk_level)

    explanation = meta.explain_tick(
        tick,
        active,
        attn,
        risk_level,
        stability
    )

    print(f"\n[Ω v7.19 | TICK {tick}]", flush=True)
    print("EVENT:", active["event_type"], flush=True)
    print("ATTENTION:", attn, flush=True)
    print("RISK:", risk_level, flush=True)
    print("STABILITY:", stability, flush=True)

    print("REFLECTION:", explanation["summary"], flush=True)

    tick += 1
