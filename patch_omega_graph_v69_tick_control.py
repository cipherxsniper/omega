# ===== OmegaExecutionGraphV69 TICK CONTROL PATCH =====

# 1. MODIFY route signature (inside class)
def route(self, start_node, memory, payload, tick_id=None):
    # 2. Initialize last_tick if missing
    if not hasattr(self, "last_tick"):
        self.last_tick = None

    # 3. HARD STOP: duplicate tick protection
    if tick_id == self.last_tick:
        return {"error": "duplicate_tick_blocked"}

    self.last_tick = tick_id

    # ---- original execution continues below ----
    graph_results = []

    node = self.nodes[start_node]
    result = node(memory, payload)

    graph_results.append({
        "node": start_node,
        **result
    })

    # chain execution
    for next_node in self.edges.get(start_node, []):
        next_result = self.nodes[next_node](memory, payload)
        graph_results.append({
            "node": next_node,
            **next_result
        })

    # 4. FINAL CONTRACT OUTPUT ENFORCEMENT
    final_health = graph_results[-1].get("health", 0.0)

    return {
        "tick_id": tick_id,
        "graph_results": graph_results,
        "final_health": final_health
    }
# ===== END PATCH =====
