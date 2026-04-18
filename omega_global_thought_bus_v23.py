from collections import deque

GLOBAL_MEMORY = {
    "sentences": deque(maxlen=200),
    "states": deque(maxlen=200),
    "signals": deque(maxlen=200),
    "sources": deque(maxlen=200)
}

NODE_REGISTRY = {}

def register_node(name):
    if name not in NODE_REGISTRY:
        NODE_REGISTRY[name] = {
            "last_output": None,
            "local_bias": 1.0
        }

def broadcast(node, message, state, signal):
    GLOBAL_MEMORY["sentences"].append(message)
    GLOBAL_MEMORY["states"].append(state)
    GLOBAL_MEMORY["signals"].append(signal)
    GLOBAL_MEMORY["sources"].append(node)

def get_recent(n=10):
    return list(GLOBAL_MEMORY["sentences"])[-n:]

def get_global_state():
    if not GLOBAL_MEMORY["signals"]:
        return 0.5
    return sum(GLOBAL_MEMORY["signals"]) / len(GLOBAL_MEMORY["signals"])
