# OMEGA SUPERVISOR v1
# Process manager + watchdog + kill switch

import time
import threading
import os
from omega_event_router import ROUTER
from omega_worker_pool import POOL

KILL_SWITCH = False


class Watchdog:
    def __init__(self):
        self.heartbeat = time.time()

    def beat(self):
        self.heartbeat = time.time()

    def monitor(self):
        global KILL_SWITCH

        while not KILL_SWITCH:
            if time.time() - self.heartbeat > 10:
                print("[Ω SUPERVISOR] SYSTEM STALL DETECTED → RESTART SIGNAL")
                ROUTER.emit("restart_signal")
            time.sleep(2)


class Supervisor:
    def __init__(self):
        self.watchdog = Watchdog()

    def start(self):
        print("[Ω SUPERVISOR] booting core stack...")

        t = threading.Thread(target=self.watchdog.monitor, daemon=True)
        t.start()

        ROUTER.emit("system_boot")

        while not KILL_SWITCH:
            self.watchdog.beat()
            time.sleep(1)

    def stop(self):
        global KILL_SWITCH
        KILL_SWITCH = True
        ROUTER.emit("shutdown")


SUPERVISOR = Supervisor()


if __name__ == "__main__":
    SUPERVISOR.start()
