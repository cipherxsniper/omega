import random
import copy

class OmegaKernelV6_5:

    def __init__(self):

        # --- base node memory ---
        self.nodes = {
            "brain": {"success": 1.0, "failure": 1.0},
            "system": {"success": 1.0, "failure": 1.0},
            "executor": {"success": 1.0, "failure": 1.0},
            "observer": {"success": 1.0, "failure": 1.0},
        }

        # --- policy (THIS WILL EVOLVE) ---
        self.policy = {
            "exploration_bias": 0.5,
            "stability_bias": 0.5,
            "entropy_limit": 0.7,
            "learning_rate": 0.05
        }

        self.history = []
        self.policy_history = []

    # -------------------------
    # 🧠 NODE WEIGHT
    # -------------------------
    def weight(self, node):
        n = self.nodes[node]
        total = n["success"] + n["failure"]
        return n["success"] / total

    # -------------------------
    # 🌐 ATTENTION
    # -------------------------
    def attention(self):
        scores = {}

        for node in self.nodes:
            stability = self.weight(node)
            exploration = random.uniform(0, self.policy["entropy_limit"])

            score = (
                stability * self.policy["stability_bias"] +
                exploration * self.policy["exploration_bias"]
            )

            scores[node] = score

        total = sum(scores.values())
        return {k: v / total for k, v in scores.items()}

    # -------------------------
    # 🔮 EXECUTION
    # -------------------------
    def tick(self):

        attn = self.attention()
        chosen = max(attn, key=attn.get)

        # simulate outcome
        success = random.random() < self.weight(chosen)

        if success:
            self.nodes[chosen]["success"] += 1
        else:
            self.nodes[chosen]["failure"] += 1

        self.history.append({
            "node": chosen,
            "success": success
        })

        # 🔁 evolve policy
        self.evolve_policy()

        return {
            "chosen": chosen,
            "success": success,
            "attention": attn,
            "policy": self.policy
        }

    # -------------------------
    # 🔁 SELF-REWRITING POLICY
    # -------------------------
    def evolve_policy(self):

        if len(self.history) < 5:
            return

        recent = self.history[-5:]
        success_rate = sum(1 for r in recent if r["success"]) / len(recent)

        old_policy = copy.deepcopy(self.policy)

        # --- mutation strength ---
        drift = (0.5 - success_rate) * self.policy["learning_rate"]

        # adjust exploration vs stability
        self.policy["exploration_bias"] += drift
        self.policy["stability_bias"] -= drift

        # adjust entropy
        self.policy["entropy_limit"] += drift * 0.5

        # clamp values (VERY IMPORTANT)
        self.policy["exploration_bias"] = min(max(self.policy["exploration_bias"], 0.1), 0.9)
        self.policy["stability_bias"] = min(max(self.policy["stability_bias"], 0.1), 0.9)
        self.policy["entropy_limit"] = min(max(self.policy["entropy_limit"], 0.2), 1.0)

        self.policy_history.append({
            "old": old_policy,
            "new": copy.deepcopy(self.policy),
            "success_rate": success_rate
        })
