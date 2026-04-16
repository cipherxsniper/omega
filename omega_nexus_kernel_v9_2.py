import time
from omega_neural_bus_v9 import BUS

print("[Ω NEXUS v9.2 KERNEL STARTING]")

def boot():
    BUS.publish("system.boot", {"status": "online"})
    print("[Ω KERNEL] BUS ONLINE")
    print("[Ω KERNEL] SYSTEM STABLE")

if __name__ == "__main__":
    boot()
    while True:
        time.sleep(5)
