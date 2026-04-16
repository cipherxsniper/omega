from omega_execution_layer_v72 import OmegaExecutionLayerV72
from omega_adaptive_router_v72 import OmegaAdaptiveRouterV72

layer = OmegaExecutionLayerV72()
router = OmegaAdaptiveRouterV72(layer)

# simple demo nodes
layer.register_node("temporal", lambda m,p: {"health": 0.6, "type": "temporal"})
layer.register_node("diagnostic", lambda m,p: {"health": 0.8, "type": "diagnostic"})
layer.register_node("repair", lambda m,p: {"health": 0.9, "type": "repair"})

layer.connect("temporal", "diagnostic", 0.7)
layer.connect("diagnostic", "repair", 0.8)

result = layer.route("temporal", {"drift": 40}, steps=5)

print("[Ω v7.2 EXECUTION RESULT]")
print(result)
