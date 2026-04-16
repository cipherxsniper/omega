from omega_bootstrap_v75 import get_execution_layer
from omega_kernel_v79 import OmegaKernelV79

from omega_kernel_adapter_v723 import OmegaKernelAdapterV723
from omega_causal_memory_v723 import OmegaCausalMemoryV723
from omega_causal_infer_v723 import OmegaCausalInferV723

print("[Ω] booting v7.23 causal memory engine...", flush=True)

layer = get_execution_layer()

# 🧠 FIX: unified kernel interface
kernel = OmegaKernelAdapterV723(OmegaKernelV79(layer))

memory = OmegaCausalMemoryV723()
infer = OmegaCausalInferV723()

tick = 0
prev_event_id = None
prev_event = None

while True:

    # 🧠 unified execution call (NO version drift possible now)
    raw = kernel.step(tick, {"drift": 40})

    event = {
        "tick": tick,
        "event_type": "success" if isinstance(raw, dict) else "route_error",
        "node": "unknown",
        "severity": 0.5
    }

    event_id = memory.add_event(event)

    if prev_event_id:
        confidence = infer.score_relation(prev_event, event)
        memory.link(prev_event_id, event_id, confidence)

    chain = memory.trace_back(event_id)
    explanation = infer.explain_chain(chain, memory)

    print(f"\n[Ω v7.23 | TICK {tick}]", flush=True)
    print("EVENT:", event["event_type"], flush=True)
    print("CAUSAL CHAIN:", " → ".join(chain), flush=True)
    print("EXPLANATION:", explanation, flush=True)

    prev_event_id = event_id
    prev_event = event
    tick += 1
