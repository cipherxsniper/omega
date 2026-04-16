import time
from collections import defaultdict
from runtime_v7.core.omega_crdt_memory_v1 import get_crdt


class SemanticCognitionEngineV15:

    def __init__(self):
        print("\n🧠 [V15 SEMANTIC COGNITION ENGINE] ONLINE\n")

        self.memory = get_crdt()

        # concept graph
        self.concepts = defaultdict(lambda: {
            "count": 0,
            "confidence": 0.5,
            "links": defaultdict(int)
        })

        self.running = True
        self.last_index = 0

    # -----------------------------
    # EVENT → MEANING
    # -----------------------------
    def interpret(self, event):

        etype = event.get("type", "unknown")
        content = event.get("content", "")

        # simple semantic mapping layer (expandable)
        concept = f"{etype}_{content}" if content else etype

        meaning = {
            "concept": concept,
            "category": self.categorize(etype),
            "importance": self.score(event),
            "raw": event
        }

        return meaning

    # -----------------------------
    # CATEGORY INFERENCE
    # -----------------------------
    def categorize(self, etype):

        if "heartbeat" in etype:
            return "network_health"

        if "user" in etype:
            return "interaction"

        return "general_event"

    # -----------------------------
    # IMPORTANCE SCORING
    # -----------------------------
    def score(self, event):

        base = 0.5

        if event.get("type") == "heartbeat":
            base += 0.2

        if "critical" in event.get("content", ""):
            base += 0.3

        return min(1.0, base)

    # -----------------------------
    # CONCEPT GRAPH UPDATE
    # -----------------------------
    def update_graph(self, meaning):

        c = meaning["concept"]

        self.concepts[c]["count"] += 1
        self.concepts[c]["confidence"] = min(
            1.0,
            self.concepts[c]["confidence"] + 0.01
        )

        # simple self-linking reinforcement
        for k in self.concepts:
            if k != c:
                self.concepts[c]["links"][k] += 1

    # -----------------------------
    # THINKING LOOP
    # -----------------------------
    def think(self):

        events = self.memory.state.get("events", [])
        new_events = events[self.last_index:]
        self.last_index = len(events)

        for e in new_events:

            meaning = self.interpret(e)
            self.update_graph(meaning)

            # store semantic layer back into memory
            self.memory.store({
                "type": "semantic_thought",
                "content": meaning,
                "timestamp": time.time()
            })

            print(f"[V15 THOUGHT] {meaning}")

    # -----------------------------
    # RUN LOOP
    # -----------------------------
    def run(self):

        while self.running:
            try:
                self.think()
                time.sleep(1)

            except Exception as e:
                print("[V15 ERROR]", e)


if __name__ == "__main__":
    engine = SemanticCognitionEngineV15()
    engine.run()
