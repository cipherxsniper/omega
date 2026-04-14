import time
import signal

RUNNING = True

class ProcessSupervisorV2:
    def __init__(self):
        self.dead_counts = {}

    def register_dead(self, module):
        self.dead_counts[module] = self.dead_counts.get(module, 0) + 1

        if self.dead_counts[module] > 3:
            print(f"🛑 BLACKLISTED: {module}")
            return False

        print(f"♻️ MARKED DEAD: {module} ({self.dead_counts[module]})")
        return True

    def should_restart(self, module):
        return self.dead_counts.get(module, 0) < 3


def shutdown(signum, frame):
    global RUNNING
    print("[SUPERVISOR] Shutdown signal received")
    RUNNING = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def main():
    print("[SUPERVISOR] ACTIVE")

    sup = ProcessSupervisorV2()

    while RUNNING:
        try:
            # Simulated monitoring loop
            print("[SUPERVISOR] monitoring system...")
            time.sleep(2)

        except Exception as e:
            print(f"[SUPERVISOR] ERROR: {e}")
            time.sleep(2)

    print("[SUPERVISOR] CLEAN EXIT")

if __name__ == "__main__":
    main()
