import time
from collections import defaultdict


class SwarmReasoningEngineV11:
    """
    V11 Swarm Reasoning Engine

    Builds reasoning layer on top of:
    - V10 Memory Graph

    Capabilities:
    - pattern detection
    - causal inference (simple heuristic model)
    - node behavior scoring
    """

    def __init__(self, memory_graph):
        self.memory = memory_graph

        # inferred behavior scores per node_id
        self.node_scores = defaultdict(lambda: {
            "activity": 0,
            "heartbeat": 0,
            "routing": 0,
            "anomalies": 0
        })

        print("[V11 REASONING] ONLINE")

    # -----------------------------
    # MAIN REASONING LOOP
    # -----------------------------
    def analyze(self):
        """
        Runs full reasoning pass over memory graph
        """
        for node_id, node in self.memory.nodes.items():
            event = node["event"]
            self._score_event(event)

        insights = self._generate_insights()
        return insights

    # -----------------------------
    # EVENT SCORING MODEL
    # -----------------------------
    def _score_event(self, event):
        node_id = event.get("node_id")
        event_type = event.get("type")

        if not node_id:
            return

        score = self.node_scores[node_id]

        # activity boost
        score["activity"] += 1

        # type-based reasoning signals
        if event_type == "heartbeat":
            score["heartbeat"] += 1

        elif event_type == "routing_tick":
            score["routing"] += 1

        else:
            score["anomalies"] += 1

    # -----------------------------
    # INSIGHT GENERATION
    # -----------------------------
    def _generate_insights(self):
        insights = {
            "high_activity_nodes": [],
            "low_signal_nodes": [],
            "anomalous_nodes": [],
            "system_state": "UNKNOWN"
        }

        for node_id, score in self.node_scores.items():

            total = score["activity"]

            # high activity nodes
            if total > 5:
                insights["high_activity_nodes"].append(node_id)

            # anomaly detection heuristic
            if score["anomalies"] > score["heartbeat"] + score["routing"]:
                insights["anomalous_nodes"].append(node_id)

            # low signal nodes
            if total < 2:
                insights["low_signal_nodes"].append(node_id)

        # global system state inference
        if len(insights["anomalous_nodes"]) > 3:
            insights["system_state"] = "UNSTABLE"

        elif len(insights["high_activity_nodes"]) > 0:
            insights["system_state"] = "ACTIVE"

        else:
            insights["system_state"] = "DORMANT"

        print(f"[V11 INSIGHT] state={insights['system_state']}")
        return insights


# -----------------------------
# FACTORY FUNCTION
# -----------------------------
def create_reasoning_engine(memory_graph):
    return SwarmReasoningEngineV11(memory_graph)

def start():
    print("[V11] STARTED PERSISTENT LOOP")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    import time
    start()

