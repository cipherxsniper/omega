import time
from collections import defaultdict, deque

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class WorldModelEngineV17:

    def __init__(self):
        print("\n🌍🧠 [V17 WORLD MODEL ENGINE] ONLINE\n")

        self.memory = get_crdt()

        # -------------------------
        # WORLD STATE MODEL
        # -------------------------
        self.world_state = {
            "nodes": defaultdict(lambda: {
                "activity": 0,
                "trust": 1.0,
                "last_seen": time.time()
            }),
            "global_health": 1.0
        }

        # -------------------------
        # CAUSAL MEMORY (from V16 style)
        # -------------------------
        self.transitions = defaultdict(lambda: defaultdict(int))

        self.last_index = 0
        self.running = True

    # =====================================================
    # UPDATE WORLD STATE
    # =====================================================
    def update_world(self, event):

        node = event.get("node_id", "unknown")

        state = self.world_state["nodes"][node]

        state["activity"] += 1
        state["last_seen"] = time.time()

        if event.get("type") == "heartbeat":
            state["trust"] = min(1.0, state["trust"] + 0.01)
        else:
            state["trust"] -= 0.001

        # clamp
        state["trust"] = max(0.0, min(1.0, state["trust"]))

    # =====================================================
    # LEARN TRANSITIONS
    # =====================================================
    def learn_transition(self, prev_event, next_event):

        if not prev_event or not next_event:
            return

        key = prev_event.get("type", "unknown")
        nxt = next_event.get("type", "unknown")

        self.transitions[key][nxt] += 1

    # =====================================================
    # PREDICTION ENGINE
    # =====================================================
    def predict_next(self, event_type):

        options = self.transitions.get(event_type, {})

        if not options:
            return {"prediction": "unknown_future", "confidence": 0.1}

        best = max(options.items(), key=lambda x: x[1])

        return {
            "prediction": best[0],
            "confidence": min(1.0, best[1] / 10)
        }

    # =====================================================
    # WORLD HEALTH MODEL
    # =====================================================
    def compute_global_health(self):

        nodes = self.world_state["nodes"]

        if not nodes:
            return 1.0

        trust_sum = sum(n["trust"] for n in nodes.values())
        return trust_sum / len(nodes)

    # =====================================================
    # THINK LOOP
    # =====================================================
    def think(self):

        events = self.memory.state.get("events", [])
        new_events = events[self.last_index:]
        self.last_index = len(events)

        prev = None

        for e in new_events:

            self.update_world(e)
            self.learn_transition(prev, e)

            prediction = self.predict_next(e.get("type"))

            self.world_state["global_health"] = self.compute_global_health()

            print(f"[V17 WORLD STATE] node={e.get('node_id')} trust={self.world_state['nodes'][e.get('node_id','unknown')]['trust']:.2f}")
            print(f"[V17 PREDICTION] {prediction}")

            prev = e

    # =====================================================
    # RUN LOOP
    # =====================================================
    def run(self):

        while self.running:
            try:
                self.think()
                time.sleep(1)

            except Exception as e:
                print("[V17 ERROR]", e)


if __name__ == "__main__":
    engine = WorldModelEngineV17()
    engine.run()
