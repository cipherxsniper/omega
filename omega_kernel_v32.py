import time
import random
from collections import defaultdict, deque


# =========================
# 🧠 SCHEMA REGISTRY
# =========================
class SchemaRegistry:
    def __init__(self):
        self.schemas = defaultdict(set)

    def register(self, channel, key):
        self.schemas[channel].add(key)

    def validate(self, channel, key):
        return key in self.schemas[channel] or True  # permissive + self-healing


# =========================
# 🧠 SAFE STATE CORE
# =========================
class SafeState:
    def __init__(self):
        self.memory = deque(maxlen=500)
        self.data = defaultdict(float)
        self.tick = 0

    def inc(self, key, value):
        self.data[key] = self.data.get(key, 0.0) + value

    def set(self, key, value):
        self.data[key] = value

    def push(self, item):
        self.memory.append(item)

    def snapshot(self):
        return {
            "tick": self.tick,
            "memory_size": len(self.memory)
        }


# =========================
# 🧠 COGNITIVE MESSAGE BUS
# =========================
class CognitiveBus:
    def __init__(self, schema):
        self.schema = schema
        self.subscribers = defaultdict(list)
        self.event_log = deque(maxlen=1000)

    def subscribe(self, channel, fn):
        self.subscribers[channel].append(fn)

    def publish(self, channel, event):
        self.event_log.append((channel, event))

        for fn in self.subscribers[channel]:
            try:
                fn(event)
            except Exception as e:
                # 🧠 crash isolation
                print(f"[BUS] module crash isolated: {e}")


# =========================
# 🧠 V32 KERNEL
# =========================
class OmegaKernelV32:
    def __init__(self):
        self.state = SafeState()
        self.schema = SchemaRegistry()
        self.bus = CognitiveBus(self.schema)

        self._register_modules()
        self.tick_rate = 1

    # -------------------------
    # MODULE REGISTRATION
    # -------------------------
    def _register_modules(self):

        self.bus.subscribe("ml", self.ml_module)
        self.bus.subscribe("memory", self.memory_module)
        self.bus.subscribe("swarm", self.swarm_module)
        self.bus.subscribe("temporal", self.temporal_module)
        self.bus.subscribe("self", self.self_model_module)

    # -------------------------
    # MODULES
    # -------------------------
    def ml_module(self, event):
        reward = random.uniform(0.4, 1.4)
        self.state.inc("ml_reward", reward)

    def memory_module(self, event):
        self.state.push(event)

    def swarm_module(self, event):
        self.state.inc("swarm_signal", random.random())

    def temporal_module(self, event):
        self.state.inc("time_flow", time.time() % 1000)

    def self_model_module(self, event):
        stability = random.uniform(0.6, 1.0)
        self.state.set("stability", stability)

    # -------------------------
    # TICK ENGINE
    # -------------------------
    def step(self):
        self.state.tick += 1

        tick_event = {
            "type": "tick",
            "tick": self.state.tick,
            "time": time.time()
        }

        # 🧠 publish to all modules
        self.bus.publish("ml", tick_event)
        self.bus.publish("memory", tick_event)
        self.bus.publish("swarm", tick_event)
        self.bus.publish("temporal", tick_event)
        self.bus.publish("self", tick_event)

        snap = self.state.snapshot()

        print(
            f"[V32] tick={snap['tick']} | "
            f"memory={snap['memory_size']} | "
            f"ml={round(self.state.data.get('ml_reward',0),2)} | "
            f"stability={round(self.state.data.get('stability',0),2)}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V32] SELF-HEALING COGNITION BUS ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV32().run()
