import json
import time
import random
from quantum_brain import QuantumBrain

class OmegaBrainBridge:
    """
    Connects QuantumBrain IR output → Omega Mesh / Kernel systems
    """

    def __init__(self):
        self.brain = QuantumBrain("mesh_bridge_brain")
        self.history = []

        self.state = {
            "tick": 0,
            "entropy": 0.5,
            "memory_pressure": 0.1
        }

    def process_thought(self, thought):
        """
        Routes IR thoughts into mesh-compatible events
        """

        event = {
            "event_type": "mesh_signal",
            "timestamp": time.time(),
            "source": thought["source"],
            "intent": thought["intent"],
            "confidence": thought["confidence"],

            "payload": thought["payload"],

            # 🧠 translation layer (IR → mesh meaning)
            "mesh_weight": (
                thought["confidence"]
                * (1 + thought["payload"]["entropy"])
            )
        }

        return event

    def run(self):
        print("[Ω-BRIDGE] QuantumBrain → Mesh bridge ONLINE")

        while True:
            self.state["tick"] += 1

            # evolve entropy slightly
            self.state["entropy"] += random.uniform(-0.01, 0.01)
            self.state["entropy"] = max(0.05, min(1.0, self.state["entropy"]))

            # generate thought
            thought = self.brain.step(self.state)

            # convert to mesh event
            event = self.process_thought(thought)

            # store memory
            self.history.append(event)
            if len(self.history) > 50:
                self.history.pop(0)

            # OUTPUT (THIS IS NOW MESH-READY DATA)
            print("[Ω-MESH EVENT]", json.dumps(event, indent=2))

            time.sleep(0.8)


if __name__ == "__main__":
    OmegaBrainBridge().run()
