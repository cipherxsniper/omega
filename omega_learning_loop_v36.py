class LearningLoop:

    def __init__(self, bus, memory):
        self.bus = bus
        self.memory = memory

    def learn(self, node, data):
        self.memory.append(data)
        self.bus.broadcast(node, f"learned:{data}")

    def reinforce(self):
        return "patterns reinforced across memory graph"
