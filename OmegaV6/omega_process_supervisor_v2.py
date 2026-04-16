import time

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


# ---------------------------
# 🔥 CRITICAL FIX: DAEMON LOOP
# ---------------------------

if __name__ == "__main__":
    sup = ProcessSupervisorV2()

    print("[SUPERVISOR] ONLINE")

    while True:
        # keep process alive so systemd doesn't kill it
        time.sleep(5)
