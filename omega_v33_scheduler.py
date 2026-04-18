import heapq

class Scheduler:
    def __init__(self):
        self.queue = []

    def add_task(self, priority, task):
        heapq.heappush(self.queue, (-priority, task))

    def next_task(self):
        if not self.queue:
            return None
        return heapq.heappop(self.queue)[1]
