import time

class OmegaHealthMonitorV2:
    def __init__(self):
        self.failures = {}

    def report_failure(self, name):
        self.failures[name] = self.failures.get(name, 0) + 1

        if self.failures[name] >= 3:
            return "BLACKLIST"
        if self.failures[name] == 2:
            return "COOLDOWN"
        return "RETRY"

    def heartbeat_ok(self, last_seen, threshold=5):
        return (time.time() - last_seen) < threshold
