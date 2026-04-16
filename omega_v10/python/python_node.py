
import json, time, os

NODE_ID = "py_node_" + str(os.getpid())

while True:
    try:
        with open("../core/node_registry.json", "r") as f:
            registry = json.load(f)
    except:
        registry = {"nodes": {}}

    registry["nodes"][NODE_ID] = {
        "type": "python",
        "last_seen": time.time(),
        "load": 0.5
    }

    with open("../core/node_registry.json", "w") as f:
        json.dump(registry, f, indent=2)

    time.sleep(2)
