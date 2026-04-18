# 🧠 Omega Node Adapter v11 (Safe Interaction Layer)

import time

class NodeAdapter:

    def __init__(self, name, memory_graph):
        self.name = name
        self.mem = memory_graph

    def perceive(self, signal=0.0):
        return self.mem.read_global_context(self.name)

    def act(self, decision, value=0.0):
        self.mem.write_memory(self.name, decision, value)

    def learn(self, feedback):
        self.mem.update_influence(self.name, feedback)
