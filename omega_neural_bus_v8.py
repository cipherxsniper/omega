# omega_neural_bus_v8.py

import queue
import uuid
from datetime import datetime

BUS = queue.Queue()

def emit(node, msg_type, data):
    BUS.put({
        "id": str(uuid.uuid4()),
        "time": datetime.utcnow().isoformat(),
        "node": node,
        "type": msg_type,
        "data": data
    })

def listen():
    return BUS.get()
