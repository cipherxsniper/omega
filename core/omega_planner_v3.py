# OMEGA PLANNER v3
# Converts goals into structured tasks

from omega_event_bus_v3 import BUS

class Planner:

    def handle(self, event):
        if event["type"] != "goal":
            return

        goal = event["payload"]

        tasks = self.decompose(goal)

        BUS.emit("task_plan", tasks)

    def decompose(self, goal):
        return [
            {"step": 1, "task": f"analyze {goal}"},
            {"step": 2, "task": f"design solution for {goal}"},
            {"step": 3, "task": f"execute safe implementation of {goal}"}
        ]


PLANNER = Planner()
BUS.subscribe(PLANNER.handle)
