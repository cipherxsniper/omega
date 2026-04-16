import heapq
import time

class OmegaSchedulerV717:

    def __init__(self):
        self.queue = []

    def score_event(self, event):
        base = {
            "success": 1.0,
            "state_update": 0.8,
            "route_error": 1.5,
            "contract_violation": 2.0
        }.get(event.get("event_type"), 1.0)

        severity = float(event.get("severity", 0.5))
        return base + severity

    def push(self, event):
        score = self.score_event(event)

        heapq.heappush(
            self.queue,
            (-score, time.time(), event)
        )

    def pop(self):
        if not self.queue:
            return None
        return heapq.heappop(self.queue)[2]

    def size(self):
        return len(self.queue)
