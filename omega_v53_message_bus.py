import time
from collections import defaultdict

BUS = defaultdict(list)

def send(sender, channel, message):
    BUS[channel].append((sender, message))

def read(channel):
    return BUS[channel]

if __name__ == "__main__":
    send("brain_01", "memory", "hello swarm")
    send("brain_02", "memory", "processing data")

    print("🧠 BUS STATE:", dict(BUS))
