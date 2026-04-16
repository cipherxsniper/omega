import time
import json
import random
import multiprocessing
from multiprocessing import Manager


# =========================
# 🌐 EVENT STRUCTURE
# =========================
def create_event(source, event_type, payload, target=None):

    return {
        "type": event_type,
        "source": source,
        "target": target,
        "payload": payload,
        "timestamp": time.time()
    }


# =========================
# 🧠 COGNITIVE EVENT BUS
# =========================
class OmegaEventBus:

    def __init__(self, shared_state):

        self.state = shared_state
        self.event_queue = Manager().list()

    # -------------------------
    # PUBLISH EVENT
    # -------------------------
    def publish(self, event):

        self.event_queue.append(event)

        print(f"[Ω-BUS] event from {event['source']} type={event['type']}")

    # -------------------------
    # ROUTE EVENT
    # -------------------------
    def route(self):

        for _ in range(len(self.event_queue)):

            event = self.event_queue.pop(0)

            source = event["source"]
            payload = event["payload"]

            # =========================
            # FEEDBACK LOOP EFFECT
            # =========================
            if "entropy" in payload:
                self.state["entropy"] += payload["entropy"] * 0.001

            # =========================
            # REWARD INJECTION
            # =========================
            if source not in self.state["rewards"]:
                self.state["rewards"][source] = 0

            self.state["rewards"][source] += payload.get("value", 0) * 0.01

            # =========================
            # MEMORY UPDATE
            # =========================
            self.state["history"].append(event)

            # limit memory
            if len(self.state["history"]) > 200:
                self.state["history"].pop(0)

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):

        print("[Ω-BUS v12] cognitive event bus ONLINE")

        while True:

            self.route()
            time.sleep(0.2)


# =========================
# 🧠 INITIAL STATE
# =========================
def init_state():

    return {
        "entropy": 0.5,
        "rewards": {},
        "history": []
    }


# =========================
# 🚀 MAIN
# =========================
if __name__ == "__main__":

    manager = Manager()
    shared_state = manager.dict(init_state())

    bus = OmegaEventBus(shared_state)

    bus.run()
