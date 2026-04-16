import time
import uuid

class TaskV83:
    def __init__(self, payload, priority=1):
        self.task_id = str(uuid.uuid4())
        self.payload = payload
        self.priority = priority
        self.created = time.time()
        self.status = "queued"
        self.result = None

    def complete(self, result):
        self.result = result
        self.status = "done"
        self.completed = time.time()
