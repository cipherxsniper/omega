class OmegaExecutionGraphV70:
    def __init__(self):
        self.nodes = {}
        self.edges = {}              # {a: {b: weight}}
        self.repair_node = None
        self.last_tick = None

        # 🧠 NEW: node health memory
        self.node_memory = {}

    # ---------------------------
    # CORE REGISTRATION
    # ---------------------------
    def add_node(self, name, fn):
        self.nodes[name] = fn
        self.edges.setdefault(name, {})
        self.node_memory.setdefault(name, {
            "avg_health": 1.0,
            "failures": 0
        })

    def set_repair_node(self, fn):
        self.repair_node = fn

    # ---------------------------
    # WEIGHTED CONNECTIONS
    # ---------------------------
    def connect(self, a, b, weight=1.0):
        self.edges.setdefault(a, {})
        self.edges[a][b] = weight

    # ---------------------------
    # ADAPTIVE ROUTING UPDATE
    # ---------------------------
    def _update_weight(self, a, b, health):
        if health < 0.5:
            self.edges[a][b] = max(0.3, self.edges[a][b] - 0.1)
        else:
            self.edges[a][b] = min(1.0, self.edges[a][b] + 0.05)

    # ---------------------------
    # NODE MEMORY UPDATE
    # ---------------------------
    def _update_memory(self, node, health):
        mem = self.node_memory[node]

        mem["avg_health"] = (mem["avg_health"] * 0.9) + (health * 0.1)

        if health < 0.5:
            mem["failures"] += 1

    # ---------------------------
    # ROUTER
    # ---------------------------
    def route(self, start_node, memory, payload, tick_id=None):

        if tick_id == self.last_tick:
            return {"error": "duplicate_tick_blocked"}

        self.last_tick = tick_id

        graph_results = []

        current = start_node
        visited = set()

        while current and current not in visited:
            visited.add(current)

            node_fn = self.nodes[current]
            result = node_fn(memory, payload)

            health = result.get("health", 0.0)

            # update memory
            self._update_memory(current, health)

            graph_results.append({
                "node": current,
                **result
            })

            # drift-based reroute decision
            drift = payload.get("drift", 0)

            if drift > 30 and self.repair_node:
                repair_result = self.repair_node(memory, payload)
                graph_results.append({"node": "repair", **repair_result})
                break

            # weighted routing selection
            next_nodes = self.edges.get(current, {})

            if not next_nodes:
                break

            # choose highest weight edge
            current = max(next_nodes.items(), key=lambda x: x[1])[0]

            # adapt weights based on health
            for b in next_nodes:
                self._update_weight(current, b, health)

        final_health = graph_results[-1].get("health", 0.0)

        return {
            "tick_id": tick_id,
            "graph_results": graph_results,
            "node_memory": self.node_memory,
            "final_health": final_health
        }
