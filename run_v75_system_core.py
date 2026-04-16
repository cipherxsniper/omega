from omega_bootstrap_v75 import get_execution_layer

OmegaExecutionLayerV73 = get_execution_layer()

# (rest of your existing runner code should already be here below this)

observer = __import__("omega_observer_v75").OmegaObserverV75()

tick = 0

    while True:
        trace = layer.route("temporal", {"drift": 40}, steps=4)

        field = {
            "global_memory": layer.memory
        }

        print(f"\n[Ω v7.5 | TICK {tick}]", flush=True)
        print("Final node:", trace["final_node"], flush=True)
        print(observer.narrate(tick, trace, field), flush=True)

        tick += 1

# FIXED OBSERVER IMPORT (v7.5)

# FIXED OBSERVER IMPORT (v7.5 correct class name)


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
        print(observer.narrate(tick, trace, field), flush=True)

        tick += 1
