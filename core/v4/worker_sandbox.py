from omega_event_bus_v4 import BUS

class Worker:

    def handle(self, event):
        if event["type"] != "validated_output":
            return

        BUS.emit("execution_result", {
            "status": "executed_safely",
            "data": event["payload"]
        })

WORKER = Worker()
BUS.subscribe(WORKER.handle)
