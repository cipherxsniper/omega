from omega_execution_layer_v73 import OmegaExecutionLayerV73
from omega_cross_learning_v73 import OmegaCrossLearningV73

layer = OmegaExecutionLayerV73()
learner = OmegaCrossLearningV73(layer)

# demo nodes
layer.register_node("temporal", lambda m,p: {"health": 0.6})
layer.register_node("diagnostic", lambda m,p: {"health": 0.8})
layer.register_node("repair", lambda m,p: {"health": 0.9})

layer.connect("temporal", "diagnostic", 0.7)
layer.connect("diagnostic", "repair", 0.8)
layer.connect("repair", "temporal", 0.4)

for tick in range(5):
    result = layer.route("temporal", {"drift": 40}, steps=4)
    learner.propagate_learning()

    print(f"\n[TICK {tick}]")
    print(result)
