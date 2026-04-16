from omega_bootstrap_v75 import get_execution_layer

OmegaExecutionLayerV73 = get_execution_layer()


if __name__ == "__main__":
    print("[Ω] booting v7.5 runner...", flush=True)

    layer = OmegaExecutionLayerV73()

    from omega_node_safety_v75 import OmegaNodeSafetyV75
    safety = OmegaNodeSafetyV75()
    safety.ensure_nodes(layer)

    observer = __import__("omega_observer_v75").OmegaObserverV75()

    tick = 0

    while True:
        trace = layer.route("temporal", {"drift": 40}, steps=4)

        field = {"global_memory": layer.memory}

        print(f"\n[Ω v7.5 | TICK {tick}]", flush=True)
        print("Final node:", trace["final_node"], flush=True)
        print(observer.narrate(tick, __import__("patch_observer_v75").normalize_trace(trace), field), flush=True)

        tick += 1

from omega_schema_v76 import OmegaFieldV76, normalize_trace

if __name__ == "__main__":

    print("[Ω] booting v7.6 schema layer...", flush=True)

    layer = OmegaExecutionLayerV73()

    from omega_node_safety_v75 import OmegaNodeSafetyV75
    safety = OmegaNodeSafetyV75()
    safety.ensure_nodes(layer)

    observer = __import__("omega_observer_v75").OmegaObserverV75()

    tick = 0

    while True:
        raw_trace = layer.route("temporal", {"drift": 40}, steps=4)
        trace = normalize_trace(raw_trace)

        field = OmegaFieldV76(layer.memory)

        print(f"\n[Ω v7.6 | TICK {tick}]", flush=True)
        print("Final node:", trace.final_node, flush=True)
        print(observer.narrate(tick, trace, field), flush=True)

        tick += 1

# === v7.8 SELF-MODEL INIT PATCH ===
from omega_self_model_v78 import OmegaSelfModelV78
self_model = OmegaSelfModelV78()
prev = None

