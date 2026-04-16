import random
import time

class OmegaKernelV6:

    def __init__(self):

        # 🧠 Unified causal memory (fixes fragmentation)
        self.causal_memory = {
            "events": [],
            "success_rate": 1.0,
            "failure_rate": 0.0,
            "node_health": {},
        }

        # ⚖️ Learnable policy system (bounded adaptation only)
        self.policy = {
            "exploration_bias": 0.5,
            "stability_bias": 0.5,
            "entropy_limit": 0.7,
            "learning_rate": 0.05
        }

        # 🧭 Attention governor (prevents runaway loops)
        self.attention = {
            "active_nodes": set(),
            "max_active_nodes": 8,
            "load": 0.0
        }

        # 📊 Learning signals
        self.metrics = {
            "tick": 0,
            "stability": 1.0,
            "adaptation_pressure": 0.0
        }

    # -----------------------------
    # 🧠 1. CAUSAL MEMORY UPDATE
    # -----------------------------
    def record_event(self, node, success, cost=1.0):

        self.causal_memory["events"].append({
            "node": node,
            "success": success,
            "cost": cost,
            "tick": self.metrics["tick"]
        })

        # update global stats
        total = len(self.causal_memory["events"])
        success_count = sum(e["success"] for e in self.causal_memory["events"])

        self.causal_memory["success_rate"] = success_count / total
        self.causal_memory["failure_rate"] = 1 - self.causal_memory["success_rate"]

    # -----------------------------
    # ⚖️ 2. POLICY LEARNING ENGINE
    # -----------------------------
    def update_policy(self):

        failure_pressure = self.causal_memory["failure_rate"]

        # adapt exploration if failure increases
        self.policy["exploration_bias"] += failure_pressure * self.policy["learning_rate"]

        # stabilize if success is high
        self.policy["stability_bias"] += self.causal_memory["success_rate"] * 0.01

        # clamp values (VERY IMPORTANT)
        self.policy["exploration_bias"] = min(max(self.policy["exploration_bias"], 0.1), 0.9)
        self.policy["stability_bias"] = min(max(self.policy["stability_bias"], 0.1), 0.9)

    # -----------------------------
    # 🧭 3. ATTENTION GOVERNOR
    # -----------------------------
    def allocate_attention(self, candidates):

        # prevent overload
        if len(self.attention["active_nodes"]) >= self.attention["max_active_nodes"]:
            self.attention["active_nodes"] = set(list(self.attention["active_nodes"])[-5:])

        weighted = []

        for node in candidates:
            score = random.random()

            # stability bias pushes toward known-good nodes
            score += self.policy["stability_bias"] * 0.5

            # exploration bias injects randomness
            score += self.policy["exploration_bias"] * random.random()

            weighted.append((node, score))

        best = max(weighted, key=lambda x: x[1])[0]

        self.attention["active_nodes"].add(best)

        return best

    # -----------------------------
    # 📊 4. SELF CORRECTION LOOP
    # -----------------------------
    def learn_from_history(self):

        events = self.causal_memory["events"]

        if len(events) < 10:
            return

        recent = events[-10:]

        failure_ratio = sum(not e["success"] for e in recent) / 10

        # adjust system stability
        self.metrics["stability"] = 1.0 - failure_ratio

        # adaptation pressure increases when unstable
        self.metrics["adaptation_pressure"] = failure_ratio * 2

        # self-healing adjustment
        if failure_ratio > 0.4:
            self.policy["stability_bias"] += 0.05
            self.policy["exploration_bias"] -= 0.03

    # -----------------------------
    # 🧠 RUN TICK
    # -----------------------------
    def tick(self, candidates):

        self.metrics["tick"] += 1

        choice = self.allocate_attention(candidates)

        # simulate outcome
        success = random.random() < self.metrics["stability"]

        self.record_event(choice, success)

        self.update_policy()
        self.learn_from_history()

        return {
            "tick": self.metrics["tick"],
            "chosen": choice,
            "success": success,
            "policy": self.policy,
            "stability": self.metrics["stability"],
            "active_attention": list(self.attention["active_nodes"])
        }
