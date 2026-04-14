import time
import traceback

from omega_state import OmegaState


# =========================
# 🧠 EVENT BUS (CENTRAL NERVE SYSTEM)
# =========================
class EventBus:
    def __init__(self):
        self.queue = []

    def emit(self, event):
        self.queue.append(event)

    def drain(self):
        events = self.queue
        self.queue = []
        return events


# =========================
# 🧩 SAFE MODULE WRAPPER
# =========================
class Module:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn

    def tick(self, state, event):
        try:
            return self.fn(state, event)
        except Exception as e:
            return {
                "module": self.name,
                "error": str(e)
            }


# =========================
# 🧠 OMEGA V27 KERNEL
# =========================
class OmegaKernelV27:
    def __init__(self):
        self.state = OmegaState()
        self.bus = EventBus()
        self.modules = []

        self.tick_rate = 1

        self._load_modules()

    # -------------------------
    # MODULE DEFINITIONS
    # -------------------------
    def _load_modules(self):

        def swarm(state, event):
            return {"swarm": "active", "tick": state.tick()}

        def memory(state, event):
            state.remember(event)
            return {"memory": "stored"}

        def ml(state, event):
            reward = 1.0 if event["type"] == "tick" else 0.5
            state.state["ml"]["reward"] = reward
            return {"ml_reward": reward}

        def temporal(state, event):
            return {"time": time.time(), "tick": state.get("tick")}

        def self_model(state, event):
            return {
                "identity": state.get("identity"),
                "stability": state.get("stability")
            }

        self.modules = [
            Module("swarm", swarm),
            Module("memory", memory),
            Module("ml", ml),
            Module("temporal", temporal),
            Module("self_model", self_model),
        ]

    # -------------------------
    # CORE COGNITION STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        event = {
            "type": "tick",
            "tick": tick,
            "timestamp": time.time()
        }

        self.bus.emit(event)

        results = []

        for e in self.bus.drain():
            self.state.push_event(e)

            for module in self.modules:
                result = module.tick(self.state, e)

                if result:
                    results.append(result)
                    self.state.push_event(result)

        # simple feedback loop (IMPORTANT)
        self.state.set("last_results", results)

        self.state.save()

        print(f"[V27] tick {tick} | modules={len(self.modules)} | events={len(results)}")

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V27] INTEGRATED COGNITION SYSTEM ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


# =========================
# BOOT
# =========================
if __name__ == "__main__":
    OmegaKernelV27().run()
