import time
from omega_execution_layer_v73 import OmegaExecutionLayerV73

layer = OmegaExecutionLayerV73()

tick = 0

while True:
    try:
        result = layer.route(
            "temporal",
            {"drift": 40},
            steps=4
        )

        print(f"\n[TICK {tick}]")
        print(result)

        tick += 1
        time.sleep(1)

    except Exception as e:
        print("[ERROR]", e)
        time.sleep(2)
