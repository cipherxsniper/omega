import random
import math

class OmegaKernelV6_8:
    def __init__(self):
        self.tick_count = 0

        self.nodes = ["brain", "system", "executor", "observer"]

        self.entropy = 0.7

        self.policy = {
            "exploration_bias": 0.5,
            "stability_bias": 0.5,
            "learning_rate": 0.05
        }

        # 🧠 Long-term memory
        self.memory = {
            node: {
                "success": 1.0,
                "failure": 1.0,
                "streak": 0,
                "long_term_score": 0.5
            } for node in self.nodes
        }

        # 🔒 Node lock system
        self.locked_node = None

    # --- Softmax attention ---
    def softmax(self, scores):
        exp = [math.exp(s) for s in scores]
        total = sum(exp)
        return [e / total for e in exp]

    # --- Entropy regulator ---
    def regulate_entropy(self):
        if self.entropy > 0.85:
            self.policy["exploration_bias"] *= 0.9
            self.policy["stability_bias"] *= 1.1

        self.entropy = min(self.entropy, 0.9)

    # --- Long-term scoring ---
    def update_long_term(self, node, success):
        m = self.memory[node]

        if success:
            m["success"] += 1
            m["streak"] += 1
        else:
            m["failure"] += 1
            m["streak"] = 0

        total = m["success"] + m["failure"]
        stability = m["success"] / total

        # weighted stability + streak
        m["long_term_score"] = (stability * 0.7) + (min(m["streak"], 10) / 10 * 0.3)

    # --- Node locking ---
    def update_lock(self):
        best_node = max(self.nodes, key=lambda n: self.memory[n]["long_term_score"])

        if self.memory[best_node]["long_term_score"] > 0.75:
            self.locked_node = best_node

    # --- Confidence-weighted learning ---
    def adapt_learning(self, success):
        if success:
            self.policy["learning_rate"] *= 0.98
        else:
            self.policy["learning_rate"] *= 1.02

        self.policy["learning_rate"] = min(max(self.policy["learning_rate"], 0.01), 0.2)

    # --- Tick ---
    def tick(self):
        self.tick_count += 1

        # attention scores
        scores = []
        for n in self.nodes:
            base = self.memory[n]["long_term_score"]

            if self.locked_node == n:
                base *= 1.3  # boost locked node

            noise = random.uniform(-self.entropy, self.entropy)
            scores.append(base + noise)

        attention = self.softmax(scores)

        chosen_index = attention.index(max(attention))
        chosen = self.nodes[chosen_index]

        # simulate success
        success = random.random() < self.memory[chosen]["long_term_score"]

        # update systems
        self.update_long_term(chosen, success)
        self.update_lock()
        self.adapt_learning(success)
        self.regulate_entropy()

        # entropy drift
        self.entropy += random.uniform(0.005, 0.02)

        return {
            "tick": self.tick_count,
            "chosen": chosen,
            "success": success,
            "locked_node": self.locked_node,
            "entropy": self.entropy,
            "learning_rate": self.policy["learning_rate"],
            "top_nodes": sorted(
                [(n, self.memory[n]["long_term_score"]) for n in self.nodes],
                key=lambda x: x[1],
                reverse=True
            )
        }
