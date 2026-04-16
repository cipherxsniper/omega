import time
from omega_execution_layer_v73 import OmegaExecutionLayerV73
from omega_message_bus_v74 import OmegaMessageBusV74
from omega_scheduler_v74 import OmegaSchedulerV74

layer = OmegaExecutionLayerV73()
bus = OmegaMessageBusV74()
sched = OmegaSchedulerV74()

tick = 0

def node_wrapper(node_name):
    def run(event):
        result = layer.route(
            node_name,
            event["payload"],
            steps=3
        )

        bus.publish({
            "type": "node_result",
            "node": node_name,
            "result": result,
            "tick": event["tick"]
        })

        return result
    return run

# subscribe all nodes dynamically
for node in layer.nodes:
    bus.subscribe("tick", node_wrapper(node))

while True:
    event = {
        "type": "tick",
        "tick": tick,
        "payload": {"drift": 40}
    }

    bus.publish(event)

    results = bus.dispatch()

    print(f"\n[TICK {tick}]")
    print(results)

    tick += 1
    time.sleep(1)
