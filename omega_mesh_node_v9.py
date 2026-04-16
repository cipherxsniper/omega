import sys
import time
import random
from omega_neural_bus_v9 import BUS

node_id = sys.argv[1] if len(sys.argv) > 1 else "node_x"
role = sys.argv[2] if len(sys.argv) > 2 else "worker"

while True:
    BUS.publish("node.tick", {
        "node": node_id,
        "role": role,
        "load": random.random(),
        "signal": "heartbeat"
    })
    time.sleep(1)
