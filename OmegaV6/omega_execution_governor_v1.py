import time

class ExecutionGovernorV1:
    def __init__(self):
        self.cooldowns = {}

    def allow(self, module):
        now = time.time()
        last = self.cooldowns.get(module, 0)

        if now - last < 3:
            return False

        self.cooldowns[module] = now
        return True
