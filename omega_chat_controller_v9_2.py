from omega_neural_bus_v9 import BUS
import time

class ChatController:
    def __init__(self):
        self.memory = []
        self.state = {"mode": "swarm-aware"}

    def handle(self, msg):
        self.memory.append(msg)

        response = {
            "input": msg,
            "analysis": "Nexus v9.2 distributed cognition active",
            "memory_size": len(self.memory),
            "backend": "event-driven swarm OS"
        }

        print("[Ω CHAT]", response)

controller = ChatController()

BUS.subscribe("chat.message", controller.handle)

print("[Ω CHAT] controller online (event-driven mode)")

while True:
    time.sleep(1)
