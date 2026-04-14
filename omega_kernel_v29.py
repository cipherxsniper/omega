import time
import random
from omega_state import OmegaState


# =========================
# 🧠 SELF MODEL ENGINE
# =========================
class SelfModel:
    def __init__(self):
        self.history = []
        self.attention_bias = 1.0
        self.goal_drift = 0.0

    def update(self, metrics):
        """
        Build internal representation of system behavior
        """

        memory = metrics["memory"]
        attention = metrics["attention"]
        tick = metrics["tick"]

        # --- memory pressure ---
        memory_pressure = min(1.0, memory / 200.0)

        # --- stability signal ---
        stability = 1.0 - abs(0.5 - (attention / 5.0))

        # --- drift signal ---
        drift = abs(self.goal_drift - stability)

        self.goal_drift = (self.goal_drift * 0.9) + (drift * 0.1)

        # --- adaptive attention bias ---
        if memory_pressure > 0.7:
            self.attention_bias *= 0.98
        else:
            self.attention_bias *= 1.01

        self.attention_bias = max(0.5, min(1.5, self.attention_bias))

        state = {
            "tick": tick,
            "memory_pressure": memory_pressure,
            "stability": stability,
            "goal_drift": self.goal_drift,
            "attention_bias": self.attention_bias
        }

        self.history.append(state)

        if len(self.history) > 200:
            self.history = self.history[-200:]

        return state


# =========================
# 🧠 V29 KERNEL (V28 + SELF MODEL)
# =========================
class OmegaKernelV29:
    def __init__(self):
        self.state = OmegaState()
        self.model = SelfModel()

        self.tick_rate = 1

    # -------------------------
    # MODULE SIMULATION (V28 BASELINE)
    # -------------------------
    def modules(self, event):
        return {
            "swarm": random.random(),
            "memory": len(self.state.state["memory"]),
            "ml_reward": random.uniform(0.5, 1.2),
            "temporal": time.time(),
            "attention": random.randint(1, 5)
        }

    # -------------------------
    # CORE STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        raw = self.modules({"tick": tick})

        # -------------------------
        # SELF MODEL UPDATE
        # -------------------------
        self_metrics = self.model.update({
            "tick": tick,
            "memory": raw["memory"],
            "attention": raw["attention"]
        })

        # -------------------------
        # ADAPTIVE ATTENTION LAYER
        # -------------------------
        adjusted_attention = int(
            raw["attention"] * self.model.attention_bias
        )

        # clamp attention
        adjusted_attention = max(1, min(5, adjusted_attention))

        # -------------------------
        # MEMORY WRITE
        # -------------------------
        self.state.remember({
            "tick": tick,
            "ml_reward": raw["ml_reward"],
            "attention": adjusted_attention,
            "self_model": self_metrics
        })

        # -------------------------
        # STATE EVOLUTION SIGNALS
        # -------------------------
        self.state.state["ml"]["bias"] = self.model.attention_bias
        self.state.state["ml"]["drift"] = self.model.goal_drift

        self.state.push_event({
            "type": "tick",
            "tick": tick,
            "attention": adjusted_attention,
            "memory": raw["memory"],
            "self_model": self_metrics
        })

        self.state.save()

        # -------------------------
        # OBSERVABILITY OUTPUT
        # -------------------------
        print(
            f"[V29] tick={tick} | "
            f"mem={raw['memory']} | "
            f"att={adjusted_attention} | "
            f"bias={self.model.attention_bias:.3f} | "
            f"drift={self.model.goal_drift:.4f}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V29] SELF-MODEL COGNITION LAYER ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


# =========================
# BOOT
# =========================
if __name__ == "__main__":
    OmegaKernelV29().run()
