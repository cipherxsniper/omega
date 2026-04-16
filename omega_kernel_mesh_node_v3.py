import time
import json
import os
import random
import uuid
from datetime import datetime

BUS_FILE = "omega_mesh_bus_v3.json"

NODE_ID = str(uuid.uuid4())[:8]


def load_bus():
    with open(BUS_FILE, "r") as f:
        return json.load(f)


def save_bus(bus):
    with open(BUS_FILE, "w") as f:
        json.dump(bus, f, indent=2)


def emit(bus, event_type, data):
    bus["events"].append({
        "node": NODE_ID,
        "type": event_type,
        "data": data,
        "time": str(datetime.now())
    })


def update_node(bus):
    bus["nodes"][NODE_ID] = {
        "last_seen": str(datetime.now()),
        "load": random.random(),
        "status": "active"
    }


def physics(bus):
    bus["global_state"]["entropy"] += random.uniform(0.0, 0.02)
    bus["global_state"]["stability"] = max(
        0.1,
        1.0 - bus["global_state"]["entropy"] * 0.4
    )


def process_events(bus):
    events = bus["events"][-10:]
    for e in events:
        if e["type"] == "ping":
            emit(bus, "pong", {"from": NODE_ID})


def loop():
    while True:
        bus = load_bus()

        bus["tick"] += 1

        update_node(bus)
        physics(bus)
        process_events(bus)

        emit(bus, "heartbeat", {"node": NODE_ID})

        save_bus(bus)

        print(f"[NODE {NODE_ID}] tick={bus['tick']} entropy={bus['global_state']['entropy']:.3f}")

        time.sleep(1)


if __name__ == "__main__":
    print(f"🧠 Omega Mesh Node ONLINE: {NODE_ID}")
    loop()
