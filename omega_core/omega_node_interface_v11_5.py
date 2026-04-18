# 🧠 Node Interface (Event-Aware Cognitive Unit)

class OmegaNode:

    def __init__(self, name, bus):

        self.name = name
        self.bus = bus

        self.state = {
            "pressure": 0.5,
            "memory": [],
            "influence": 0.5
        }

        # every node listens to ecosystem events
        self.bus.subscribe("memory_update", name)
        self.bus.subscribe("goal_update", name)
        self.bus.subscribe("attention_signal", name)

    def emit(self, event_type, data):

        return self.bus.publish(
            event_type,
            self.name,
            data
        )

    def step(self):

        # simulate internal decision
        self.state["pressure"] += 0.01

        if self.state["pressure"] > 0.7:
            self.emit("attention_signal", {
                "pressure": self.state["pressure"]
            })

        return self.state
