from collections import deque
import json

class MemoryV4:
    def __init__(self):
        self.store = deque(maxlen=500)

    def write(self, item):
        self.store.append(item)

    def search(self, query):
        return [x for x in self.store if query in str(x)]

MEMORY = MemoryV4()
