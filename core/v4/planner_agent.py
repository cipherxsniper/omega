from omega_event_bus_v4 import BUS

class PlannerAgent:

    def handle(self, event):
        if event["type"] != "goal":
            return

        goal = event["payload"]

        plan = [
            f"analyze {goal}",
            f"design solution for {goal}",
            f"execute safe implementation for {goal}"
        ]

        BUS.emit("plan", plan)

AGENT = PlannerAgent()
BUS.subscribe(AGENT.handle)
