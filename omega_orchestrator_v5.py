# ============================================================
# OMEGA ORCHESTRATOR v5 — PHASE 1 CORE
# Event-driven cognitive control system
# ============================================================

import time
import traceback
from collections import defaultdict


# ============================================================
# 🧠 EVENT BUS (CORE COMMUNICATION LAYER)
# ============================================================

class OmegaEventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)
        self.event_log = []

    def subscribe(self, event_type, handler):
        self.subscribers[event_type].append(handler)

    def publish(self, event_type, data=None):
        event = {
            "type": event_type,
            "data": data,
            "timestamp": time.time()
        }

        self.event_log.append(event)

        for handler in self.subscribers[event_type]:
            try:
                handler(event)
            except Exception as e:
                print(f"[EVENT ERROR] {event_type}: {e}")


# ============================================================
# 🧠 MEMORY CORE (PHASE 1 SIMPLE VERSION)
# ============================================================

class OmegaMemoryCore:
    def __init__(self):
        self.store = {}

    def set(self, key, value):
        self.store[key] = value

    def get(self, key, default=None):
        return self.store.get(key, default)

    def update(self, key, value):
        if key not in self.store:
            self.store[key] = []
        self.store[key].append(value)


# ============================================================
# 🧠 MODULE REGISTRY
# ============================================================

class OmegaModuleRegistry:
    def __init__(self):
        self.modules = {}

    def register(self, name, module):
        self.modules[name] = module

    def get(self, name):
        return self.modules.get(name)

    def all_modules(self):
        return self.modules


# ============================================================
# 🧠 OMEGA ORCHESTRATOR (CORE ENGINE)
# ============================================================

class OmegaOrchestrator:
    def __init__(self):
        self.bus = OmegaEventBus()
        self.memory = OmegaMemoryCore()
        self.registry = OmegaModuleRegistry()
        self.running = False

        self._bind_core_events()

    # --------------------------------------------------------
    # CORE EVENT HOOKS
    # --------------------------------------------------------

    def _bind_core_events(self):
        self.bus.subscribe("system_start", self.on_system_start)
        self.bus.subscribe("system_error", self.on_system_error)
        self.bus.subscribe("memory_update", self.on_memory_update)

    # --------------------------------------------------------
    # EVENT HANDLERS
    # --------------------------------------------------------

    def on_system_start(self, event):
        print("[OMEGA] System starting...")

    def on_system_error(self, event):
        print(f"[OMEGA ERROR] {event['data']}")

    def on_memory_update(self, event):
        data = event["data"]
        if data:
            self.memory.update(data["key"], data["value"])

    # --------------------------------------------------------
    # SYSTEM CONTROL
    # --------------------------------------------------------

    def start(self):
        self.running = True
        self.bus.publish("system_start")

        while self.running:
            try:
                # Placeholder for future brain cycle
                time.sleep(1)

            except Exception as e:
                self.bus.publish("system_error", str(e))
                traceback.print_exc()

    def stop(self):
        self.running = False

    # --------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------

    def run(self):
        self.start()
