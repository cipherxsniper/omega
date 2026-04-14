import time
import random
import importlib
from collections import defaultdict, deque
from omega_state import OmegaState


# =========================
# 🧠 MODULE REGISTRY BUS
# =========================
class ModuleBus:
    """
    Treats all omega_*.py files as a cognitive swarm registry.
    """
    def __init__(self):
        self.modules = {
            "ml": 1.0,
            "swarm": 1.0,
            "memory": 1.0,
            "temporal": 1.0,
            "identity": 1.0
        }

        self.performance = defaultdict(float)

    def score_module(self, name, reward, stability):
        score = reward * stability
        self.performance[name] += score * 0.1

        # decay weak modules
        for k in self.performance:
            self.performance[k] *= 0.995

    def get_weights(self):
        total = sum(self.performance.values()) + 1e-6

        return {
            k: (v / total)
            for k, v in self.performance.items()
        }


# =========================
# 🧠 ATTENTION GOVERNOR
# =========================
class AttentionGovernor:
    def __init__(self):
        self.history = deque(maxlen=100)

    def allocate(self, signals):
        scored = []

        for s in signals:
            score = (
                s.get("ml_reward", 0.5)
                * s.get("stability", 1.0)
                * random.uniform(0.9, 1.1)
            )

            scored.append((score, s))

        scored.sort(reverse=True, key=lambda x: x[0])
        top = scored[:3]

        self.history.extend(top)

        return top


# =========================
# 🧠 STABILITY GOVERNOR
# =========================
class StabilityGovernor:
    def __init__(self):
        self.instability = 0.0

    def evaluate(self, memory_pressure, reward_variance):
        self.instability = (
            memory_pressure * 0.5 +
            reward_variance * 0.5
        )

        return self.instability

    def clamp(self, value):
        if self.instability > 0.7:
            return value * 0.85  # throttle system
        return value


# =========================
# 🧠 V33 KERNEL
# =========================
class OmegaKernelV33:
    def __init__(self):
        self.state = OmegaState()

        self.bus = ModuleBus()
        self.attention = AttentionGovernor()
        self.stability = StabilityGovernor()

        self.recent_rewards = deque(maxlen=20)

        self.tick_rate = 1

    # -------------------------
    # SIMULATED ENVIRONMENT
    # -------------------------
    def collect_signals(self):
        return [
            {
                "module": "ml",
                "ml_reward": random.uniform(0.3, 1.6),
                "stability": random.uniform(0.6, 1.0)
            },
            {
                "module": "swarm",
                "ml_reward": random.uniform(0.5, 1.3),
                "stability": random.uniform(0.7, 1.0)
            },
            {
                "module": "memory",
                "ml_reward": random.uniform(0.2, 1.2),
                "stability": random.uniform(0.8, 1.0)
            },
            {
                "module": "temporal",
                "ml_reward": random.uniform(0.4, 1.5),
                "stability": random.uniform(0.6, 1.0)
            }
        ]

    # -------------------------
    # CORE STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        signals = self.collect_signals()

        # 🧠 ATTENTION SELECTION
        top = self.attention.allocate(signals)

        # reward stats
        rewards = [s[1]["ml_reward"] for s in top]
        self.recent_rewards.extend(rewards)

        reward_var = max(rewards) - min(rewards) if rewards else 0.0

        memory_pressure = len(self.state.state["memory"]) / 500.0

        # ⚖️ STABILITY CONTROL
        instability = self.stability.evaluate(memory_pressure, reward_var)

        # 🧠 MODULE COMPETITION UPDATE
        for score, signal in top:
            self.bus.score_module(
                signal["module"],
                signal["ml_reward"],
                signal["stability"]
            )

        # 🧠 ADAPTIVE GLOBAL SCALE
        global_mod = self.stability.clamp(1.0 + sum(rewards) * 0.05)

        # -------------------------
        # MEMORY WRITE
        # -------------------------
        self.state.remember({
            "tick": tick,
            "top_signals": top,
            "instability": instability,
            "global_mod": global_mod,
            "module_weights": self.bus.get_weights()
        })

        self.state.push_event({
            "type": "tick",
            "tick": tick,
            "instability": instability
        })

        self.state.save()

        print(
            f"[V33] tick={tick} | "
            f"top={len(top)} | "
            f"instability={instability:.3f} | "
            f"memory={len(self.state.state['memory'])}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V33] ATTENTION + STABILITY + COMPETITION LAYER ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV33().run()
