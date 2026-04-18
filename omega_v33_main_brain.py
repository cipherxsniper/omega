from omega_v33_node_discovery import scan_nodes
from omega_v33_goal_engine import create_goal
from omega_v33_scheduler import Scheduler
from omega_v33_heartbeat import pulse

class OmegaBrain:
    def __init__(self):
        self.scheduler = Scheduler()
        self.nodes = []

    def boot(self):
        self.nodes = scan_nodes(["/data/data/com.termux/files/home/Omega",
                                 "/data/data/com.termux/files/home/Omega/omega-bot"])
        return f"🧠 Omega v33 booted with {len(self.nodes)} nodes"

    def process(self, message):
        goal = create_goal(message)

        self.scheduler.add_task(goal["priority"], {
            "message": message,
            "goal": goal
        })

        return f"🎯 Goal created: {goal}"

    def heartbeat_all(self):
        return [pulse(n["name"]) for n in self.nodes[:10]]

brain = OmegaBrain()
