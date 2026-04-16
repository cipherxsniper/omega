from omega_neural_bus_v9 import BUS

print("[Ω NEXUS v9.3 KERNEL ONLINE]")

def broadcast_system(msg):
    BUS.publish("chat.message", msg)

BUS.publish("system.boot", {"status": "online", "version": "9.3"})

while True:
    BUS.publish("system.heartbeat", {"tick": 1})
