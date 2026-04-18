# 🧠 OMEGA v29 GLOBAL BUS

import time
from collections import defaultdict, deque

BUS = {
    "state": {},
    "memory": defaultdict(float),
    "signals": deque(maxlen=100),
    "links": defaultdict(set),
    "tick": 0
}

def emit(source, data):
    BUS["signals"].append((source, data))
    BUS["tick"] += 1

def write(key, value):
    BUS["state"][key] = value

def read(key):
    return BUS["state"].get(key, None)
