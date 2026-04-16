import time

from omega_event_bus_v4 import BUS
import planner_agent
import reasoning_agent
import critique_agent
import worker_sandbox

class Supervisor:

    def start(self):
        print("[Ω SUPERVISOR v4] Autonomous Agent Network ONLINE")

        BUS.start()

        BUS.emit("goal", "optimize system intelligence safely")

        while True:
            time.sleep(1)

if __name__ == "__main__":
    Supervisor().start()
