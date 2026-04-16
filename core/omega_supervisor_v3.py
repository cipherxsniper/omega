import time
from omega_event_bus_v3 import BUS
import omega_reasoning_node_v3
import omega_planner_v3
import omega_worker_v3
import omega_memory_v3

class Supervisor:

    def __init__(self):
        self.alive = True

    def start(self):
        print("[Ω SUPERVISOR v3] Cognitive stack online")

        BUS.start()

        # boot test cycle
        BUS.emit("goal", "optimize system stability")

        while self.alive:
            time.sleep(1)


if __name__ == "__main__":
    Supervisor().start()
