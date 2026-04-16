import time
from collections import defaultdict, deque

from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class CausalReasoningEngineV16:

    def __init__(self):
        print("\n🧠 [V16 CAUSAL REASONING ENGINE] ONLINE\n")

        self.memory = get_crdt()

        # -------------------------
        # CAUSAL GRAPH
        # -------------------------
        self.causal_graph = defaultdict(lambda: {
            "causes": defaultdict(int),
            "effects": defaultdict(int),
            "confidence": 0.5
        })

        self.last_index = 0
        self.running = True

    # =====================================================
    # EVENT → CAUSE DETECTION
    # =====================================================
    def detect_cause(self, event):

        etype = event.get("type", "")
        content = event.get("content", "")

        # simple causal heuristics (expandable later)
        if etype == "heartbeat":
            return "node_active_signal"

        if "drop" in content:
            return "network_instability"

        if "error" in content:
            return "system_fault"

        return "unknown_cause"

    # =====================================================
    # EFFECT GENERATION
    # =====================================================
    def infer_effect(self, cause):

        mapping = {
            "node_active_signal": "system_stability",
            "network_instability": "trust_decrease",
            "system_fault": "repair_needed",
            "unknown_cause": "uncertain_state"
        }

        return mapping.get(cause, "unknown_state")

    # =====================================================
    # UPDATE CAUSAL GRAPH
    # =====================================================
    def update_graph(self, cause, effect):

        node = self.causal_graph[cause]

        node["effects"][effect] += 1
        node["confidence"] = min(
            1.0,
            node["confidence"] + 0.01
        )

    # =====================================================
    # REASONING ENGINE (THE "WHY" LAYER)
    # =====================================================
    def reason(self, event):

        cause = self.detect_cause(event)
        effect = self.infer_effect(cause)

        self.update_graph(cause, effect)

        explanation = {
            "event": event,
            "cause": cause,
            "effect": effect,
            "explanation": f"{cause} leads to {effect}",
            "confidence": self.causal_graph[cause]["confidence"]
        }

        return explanation

    # =====================================================
    # THINK LOOP
    # =====================================================
    def think(self):

        events = self.memory.state.get("events", [])
        new_events = events[self.last_index:]
        self.last_index = len(events)

        for e in new_events:

            result = self.reason(e)

            # store back into CRDT memory
            self.memory.store({
                "type": "causal_thought",
                "content": result,
                "timestamp": time.time()
            })

            print(f"[V16 REASON] {result}")

    # =====================================================
    # RUN LOOP
    # =====================================================
    def run(self):

        while self.running:
            try:
                self.think()
                time.sleep(1)

            except Exception as e:
                print("[V16 ERROR]", e)


if __name__ == "__main__":
    engine = CausalReasoningEngineV16()
    engine.run()
