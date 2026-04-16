class OmegaKnowledgeFieldV75:
    def __init__(self):
        self.global_memory = {
            "nodes": {},
            "events": [],
            "relationships": {},
            "summary": ""
        }

    def update_node(self, node, data):
        if node not in self.global_memory["nodes"]:
            self.global_memory["nodes"][node] = {
                "history": [],
                "avg_health": 0.0,
                "runs": 0
            }

        n = self.global_memory["nodes"][node]
        n["history"].append(data)
        n["runs"] += 1

        health = data.get("health", 0.0)
        n["avg_health"] = (
            (n["avg_health"] * (n["runs"] - 1)) + health
        ) / n["runs"]

    def log_event(self, event):
        self.global_memory["events"].append(event)

    def get_context(self):
        return self.global_memory
