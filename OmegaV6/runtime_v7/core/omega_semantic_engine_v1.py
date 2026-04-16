import time
from collections import defaultdict, deque


class SemanticEngineV1:
    """
    🧠 V15 SEMANTIC LAYER
    Converts raw swarm events into meaning, intent, and compressed cognition
    """

    def __init__(self):
        print("\n🧠 [SEMANTIC ENGINE V1] ONLINE — MEANING LAYER ACTIVE\n")

        # ----------------------------
        # MEMORY BUFFERS
        # ----------------------------
        self.recent_events = deque(maxlen=500)
        self.concepts = defaultdict(int)
        self.intent_map = defaultdict(int)
        self.compressed_memory = []

        # ----------------------------
        # SEMANTIC RULES (simple but expandable)
        # ----------------------------
        self.rules = {
            "heartbeat": "node_presence_signal",
            "user_input": "external_intent_signal",
            "error": "system_instability_event",
            "connect": "node_join_event",
            "disconnect": "node_exit_event"
        }

    # =====================================================
    # EVENT → MEANING
    # =====================================================
    def interpret(self, event: dict):
        etype = event.get("type", "unknown")

        concept = self.rules.get(etype, "unknown_event")

        content = event.get("content", "")
        node_id = event.get("node_id", "unknown")

        meaning = {
            "concept": concept,
            "node": node_id,
            "intent": self._infer_intent(etype, content),
            "weight": self._weight(event),
            "timestamp": time.time()
        }

        self.recent_events.append(meaning)

        # update concept stats
        self.concepts[concept] += 1
        self.intent_map[meaning["intent"]] += 1

        return meaning

    # =====================================================
    # INTENT DETECTION (LIGHTWEIGHT BUT EXTENSIBLE)
    # =====================================================
    def _infer_intent(self, etype, content):
        if etype == "heartbeat":
            return "maintenance_signal"

        if etype == "user_input":
            if "?" in content:
                return "query_intent"
            return "command_intent"

        if etype == "error":
            return "instability_signal"

        return "neutral_observation"

    # =====================================================
    # EVENT WEIGHTING
    # =====================================================
    def _weight(self, event):
        base = 1.0

        if event.get("type") == "heartbeat":
            return base * 0.5

        if event.get("type") == "error":
            return base * 2.0

        return base

    # =====================================================
    # COMPRESSION ENGINE (CRITICAL FOR SCALING)
    # =====================================================
    def compress_memory(self):
        """
        Turns raw event stream into semantic summaries
        """
        summary = {
            "total_events": len(self.recent_events),
            "concepts": dict(self.concepts),
            "top_intents": dict(self.intent_map),
            "dominant_concept": self._dominant(self.concepts),
            "dominant_intent": self._dominant(self.intent_map),
            "timestamp": time.time()
        }

        self.compressed_memory.append(summary)

        # prevent memory explosion
        if len(self.compressed_memory) > 200:
            self.compressed_memory = self.compressed_memory[-100:]

        return summary

    # =====================================================
    # DOMINANCE HELPER
    # =====================================================
    def _dominant(self, table):
        if not table:
            return None
        return max(table.items(), key=lambda x: x[1])[0]

    # =====================================================
    # "THOUGHT" GENERATION (FIRST REAL COGNITION STEP)
    # =====================================================
    def generate_thought(self):
        if not self.recent_events:
            return {
                "thought": "silence_detected",
                "confidence": 0.0
            }

        last = self.recent_events[-1]

        thought = {
            "thought": f"system observing {last['concept']}",
            "dominant_state": self._dominant(self.concepts),
            "intent_focus": self._dominant(self.intent_map),
            "confidence": min(1.0, len(self.recent_events) / 100),
            "timestamp": time.time()
        }

        return thought
