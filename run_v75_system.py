import time

from omega_execution_layer_v73 import OmegaExecutionLayerV73
from omega_knowledge_field_v75 import OmegaKnowledgeFieldV75
from omega_observer_v75 import OmegaObserverV75
from omega_fusion_v75 import OmegaFusionV75

layer = OmegaExecutionLayerV73()

# === v7.5 NODE SAFETY BOOT PATCH ===
from omega_node_safety_v75 import OmegaNodeSafetyV75

safety = OmegaNodeSafetyV75()
safety.ensure_nodes(layer)

field = OmegaKnowledgeFieldV75()
observer = OmegaObserverV75()
fusion = OmegaFusionV75()

tick = 0

while True:
    trace = layer.route(
        "temporal",
        {"drift": 40},
        steps=4
    )["trace"]

    # update global field
    for step in trace:
        node = step["node"]
        result = step["result"]

        field.update_node(node, result)

    field.log_event({
        "tick": tick,
        "trace": trace
    })

    fusion.fuse(field)

    print("\n" + "="*40)
    print(observer.narrate(tick, trace, field), flush=True)

    tick += 1
    time.sleep(1)

# === v7.5 FORCE BASE CONNECTIVITY ===
if not hasattr(layer, "weights") or not layer.weights:
    layer.weights = {}

    base_nodes = ["temporal", "diagnostic", "repair"]

    for a in base_nodes:
        for b in base_nodes:
            if a != b:
                layer.weights[(a, b)] = 0.5

