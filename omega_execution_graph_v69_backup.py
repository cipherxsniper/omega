from collections import defaultdict


# =========================
# Ω CONTRACT ENFORCER
# =========================
def omega_contract(health, output, signals):
    return {
        "health": float(health),
        "output": output,
        "signals": signals or {}
    }


# =========================
# NODE WRAPPER
# =========================
class Node:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn
        self.history = []
        self.weight = 1.0

    def update(self, health):
        self.history.append(health)
        self.history = self.history[-20:]

        self.weight = sum(self.history) / len(self.history)


# =========================
# Ω EXECUTION GRAPH v6.9
# =========================
class OmegaExecutionGraphV69:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(dict)
        self.repair_node = None

    # ---------------------
    # NODE REGISTRATION
    # ---------------------
    def add_node(self, name, fn):
        self.nodes[name] = Node(name, fn)

    def set_repair_node(self, fn):
        self.repair_node = Node("repair", fn)

    def connect(self, a, b, weight=1.0):
        self.edges[a][b] = weight

    # ---------------------
    # ROUTING LOGIC
    # ---------------------
    def _next(self, current):
        options = self.edges.get(current, {})

        best = None
        best_score = -1

        for name, w in options.items():
            node = self.nodes.get(name)
            if not node:
                continue

            score = node.weight * w

            if score > best_score:
                best_score = score
                best = name

        return best

    # ---------------------
    # SELF-REWRITE ENGINE
    # ---------------------
    def _rewrite(self):
        for a, targets in self.edges.items():
            for b in targets:
                node = self.nodes.get(b)
                if not node:
                    continue

                if node.weight < 0.5:
                    self.edges[a][b] *= 0.90

                elif node.weight > 0.75:
                    self.edges[a][b] *= 1.05

                self.edges[a][b] = max(0.1, min(self.edges[a][b], 3.0))

    # ---------------------
    # EXECUTION ROUTE
    # ---------------------
    def route(self, start, memory, payload):
        current = start
        path = []

        for _ in range(6):

            node = self.nodes.get(current)
            if not node:
                break

            result = node.fn(memory, payload)

            # enforce contract always
            result = omega_contract(
                result.get("health", 0.0),
                result.get("output"),
                result.get("signals", {})
            )

            node.update(result["health"])

            path.append({
                "node": current,
                **result
            })

            # repair trigger
            if result["health"] < 0.4 and self.repair_node:
                r = self.repair_node.fn(memory, payload)
                path.append({
                    "node": "repair",
                    **omega_contract(
                        r.get("health", 0.5),
                        r.get("output"),
                        r.get("signals")
                    )
                })

            self._rewrite()

            nxt = self._next(current)
            if not nxt:
                break

            current = nxt

        return {
            "graph_results": path,
            "final_health": path[-1]["health"] if path else 0.0
        }
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
