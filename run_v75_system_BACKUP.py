import time

from omega_execution_layer_v73 import OmegaExecutionLayerV73
from omega_knowledge_field_v75 import OmegaKnowledgeFieldV75
from omega_observer_v75 import OmegaObserverV75
from omega_fusion_v75 import OmegaFusionV75

layer = OmegaExecutionLayerV73()
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
    print(observer.narrate(tick, trace, field))

    tick += 1
    time.sleep(1)
