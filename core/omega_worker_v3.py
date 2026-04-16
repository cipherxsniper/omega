from omega_event_bus_v3 import BUS

class Worker:

    def handle(self, event):
        if event["type"] != "task_plan":
            return

        tasks = event["payload"]

        results = []
        for t in tasks:
            results.append({
                "task": t,
                "status": "completed_safe_mode"
            })

        BUS.emit("task_result", results)


WORKER = Worker()
BUS.subscribe(WORKER.handle)
