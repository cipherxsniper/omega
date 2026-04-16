import time
import random
from collections import deque, defaultdict
from omega_state import OmegaState


# =========================
# 🧠 SAFE GOAL EMERGENCE ENGINE (V30 FIXED)
# =========================
class GoalEmergence:
    def __init__(self):
        self.reward_memory = deque(maxlen=200)

        # 🔥 FIX: no KeyErrors ever again
        self.goal_weights = defaultdict(float)

        self.emergent_goals = []
        self.goal_entropy = 0.0

    # -------------------------
    # SAFE UPDATE CORE
    # -------------------------
    def _safe_inc(self, key, value):
        self.goal_weights[key] += value

    # -------------------------
    # OBSERVE MEMORY
    # -------------------------
    def observe(self, memory_entry):

        reward = memory_entry.get("ml_reward", 0.0)
        attention = memory_entry.get("attention", 1)

        # 🔥 CLAMP + SANITIZE ATTENTION (CRITICAL FIX)
        attention = max(1, min(int(attention), 5))

        self.reward_memory.append(reward)

        key = f"att_{attention}"

        # SAFE UPDATE (NO KEYERROR EVER)
        self._safe_inc(key, reward * 0.1)

        # decay system
        for k in list(self.goal_weights.keys()):
            self.goal_weights[k] *= 0.995

        # prune noise
        self.goal_weights = defaultdict(
            float,
            {k: v for k, v in self.goal_weights.items() if v > 0.01}
        )

        self._compute_emergent_goals()
        self._compute_entropy()

    # -------------------------
    # EMERGENT GOALS
    # -------------------------
    def _compute_emergent_goals(self):
        sorted_goals = sorted(
            self.goal_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )

        self.emergent_goals = [
            {"goal": g, "strength": round(w, 4)}
            for g, w in sorted_goals[:5]
        ]

    # -------------------------
    # ENTROPY (V31 FIX)
    # -------------------------
    def _compute_entropy(self):
        if not self.goal_weights:
            self.goal_entropy = 0.0
            return

        values = list(self.goal_weights.values())
        avg = sum(values) / len(values)
        var = sum((x - avg) ** 2 for x in values) / len(values)

        self.goal_entropy = float(var)

    # -------------------------
    # OUTPUT
    # -------------------------
    def get_goal_vector(self):
        if not self.emergent_goals:
            return {"goal": "explore", "strength": 0.1}

        return self.emergent_goals[0]


# =========================
# 🧠 V31 SELF-REFLECTION KERNEL (STABLE)
# =========================
class OmegaKernelV31:
    def __init__(self):
        self.state = OmegaState()
        self.goal_engine = GoalEmergence()

        self.tick_rate = 1

    # -------------------------
    def modules(self):
        return {
            "ml_reward": random.uniform(0.3, 1.4),
            "attention": random.randint(1, 5),
            "stability": random.uniform(0.6, 1.0),
            "memory_pressure": len(self.state.state["memory"]) / 200.0,
        }

    # -------------------------
    def step(self):
        tick = self.state.tick()

        outputs = self.modules()

        memory_entry = {
            "tick": tick,
            **outputs
        }

        # GOAL SYSTEM
        self.goal_engine.observe(memory_entry)
        goal = self.goal_engine.get_goal_vector()

        # MEMORY WRITE
        self.state.remember({
            **memory_entry,
            "goal": goal
        })

        self.state.push_event({
            "type": "tick",
            "tick": tick,
            "goal": goal
        })

        self.state.save()

        print(
            f"[V31] tick={tick} | "
            f"goal={goal['goal']} | "
            f"entropy={self.goal_engine.goal_entropy:.3f} | "
            f"memory={len(self.state.state['memory'])}"
        )

    # -------------------------
    def run(self):
        print("[V31] SELF-HEALING GOAL SYSTEM ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV31().run()
