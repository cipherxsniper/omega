import time
import random
import math
from collections import defaultdict
from omega_state import OmegaState


# =========================
# 🧠 GOAL EMERGENCE ENGINE (V30 UPGRADED)
# =========================
class GoalEmergence:
    def __init__(self):
        self.reward_memory = []
        self.goal_weights = defaultdict(float)
        self.goal_entropy = 1.0
        self.emergent_goals = []

    # -------------------------
    # ENTROPY CALCULATION
    # -------------------------
    def _entropy(self):
        values = list(self.goal_weights.values())
        if not values:
            return 1.0

        total = sum(values)
        if total == 0:
            return 1.0

        probs = [v / total for v in values if v > 0]

        entropy = -sum(p * math.log(p + 1e-9) for p in probs)
        return entropy

    # -------------------------
    # OBSERVE MEMORY SIGNAL
    # -------------------------
    def observe(self, memory_entry):
        reward = memory_entry.get("ml_reward", 0.0)
        attention = memory_entry.get("attention", 1)
        stability = memory_entry.get("stability", 0.8)

        self.reward_memory.append(reward)
        if len(self.reward_memory) > 200:
            self.reward_memory = self.reward_memory[-200:]

        key = f"att_{attention}"

        # -------------------------
        # STABILITY-WEIGHTED REINFORCEMENT
        # -------------------------
        stability_factor = 0.5 + (stability * 0.5)
        reinforcement = reward * stability_factor

        self.goal_weights[key] += reinforcement * 0.08

        # -------------------------
        # NON-LINEAR DECAY (IMPORTANT)
        # -------------------------
        for k in list(self.goal_weights.keys()):
            self.goal_weights[k] *= 0.992  # slower decay = memory persistence

            # saturation clamp
            self.goal_weights[k] = min(self.goal_weights[k], 10.0)

        # prune noise floor
        self.goal_weights = {
            k: v for k, v in self.goal_weights.items() if v > 0.02
        }

        self.goal_entropy = self._entropy()

        self._compute_goals()

    # -------------------------
    # GOAL GENERATION
    # -------------------------
    def _compute_goals(self):
        sorted_goals = sorted(
            self.goal_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )

        self.emergent_goals = []

        for g, w in sorted_goals[:5]:
            confidence = math.tanh(w / 5.0)

            self.emergent_goals.append({
                "goal": g,
                "strength": round(w, 4),
                "confidence": round(confidence, 4)
            })

    # -------------------------
    # GOAL SELECTION (WITH ENTROPY BALANCE)
    # -------------------------
    def get_goal_vector(self):

        if not self.emergent_goals:
            return {
                "goal": "explore",
                "strength": 0.1,
                "confidence": 0.1
            }

        # entropy-driven exploration pressure
        top = self.emergent_goals[0]

        if self.goal_entropy < 0.8:
            # collapse detected → force exploration
            return {
                "goal": "explore",
                "strength": 0.5,
                "confidence": 0.3
            }

        return top


# =========================
# 🧠 V30 KERNEL (ENGINEERED)
# =========================
class OmegaKernelV30:
    def __init__(self):
        self.state = OmegaState()
        self.goal_engine = GoalEmergence()

        self.tick_rate = 1

    # -------------------------
    # MODULE SIMULATION
    # -------------------------
    def modules(self, tick):
        return {
            "ml_reward": random.uniform(0.3, 1.4),
            "attention": random.randint(1, 5),
            "memory_pressure": len(self.state.state["memory"]) / 200.0,
            "stability": random.uniform(0.6, 1.0),
        }

    # -------------------------
    # CORE STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        outputs = self.modules(tick)

        memory_entry = {
            "tick": tick,
            **outputs
        }

        # -------------------------
        # GOAL EMERGENCE
        # -------------------------
        self.goal_engine.observe(memory_entry)
        goal = self.goal_engine.get_goal_vector()

        # -------------------------
        # MEMORY WRITE
        # -------------------------
        self.state.remember({
            **memory_entry,
            "emergent_goal": goal,
            "entropy": self.goal_engine.goal_entropy
        })

        self.state.push_event({
            "type": "tick",
            "tick": tick,
            "goal": goal
        })

        self.state.save()

        # -------------------------
        # OUTPUT
        # -------------------------
        print(
            f"[V30] tick={tick} | "
            f"goal={goal['goal']} | "
            f"strength={goal['strength']} | "
            f"conf={goal.get('confidence', 0):.3f} | "
            f"entropy={self.goal_engine.goal_entropy:.3f} | "
            f"memory={len(self.state.state['memory'])}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V30] ENGINEERED GOAL EMERGENCE LAYER ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV30().run()
