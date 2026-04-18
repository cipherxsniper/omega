class TaskQueue:
    def __init__(self):
        self.tasks = []

    def load(self, plan):
        self.tasks.extend(plan)

    def size(self):
        return len(self.tasks)

    def next(self):
        return self.tasks.pop(0) if self.tasks else None
