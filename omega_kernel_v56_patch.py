import math
import random
import json
import os

# =========================
# CORE UTILITIES (PATCHED)
# =========================

def clamp(x, min_val=0.0, max_val=1.0):
    return max(min(x, max_val), min_val)

def squash(x):
    return math.tanh(x)

def stabilize(value, target=0.5, strength=0.05):
    return value + (target - value) * strength

def noise(scale=0.01):
    return random.uniform(-scale, scale)

# =========================
# MEMORY CORE (NEW)
# =========================

class MemoryCore:
    def __init__(self, path="omega_memory_v56.json"):
        self.path = path
        self.data = self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                return json.load(open(self.path))
            except:
                return {"thoughts": [], "states": []}
        return {"thoughts": [], "states": []}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def log_thought(self, thought):
        self.data["thoughts"].append(thought)
        self.data["thoughts"] = self.data["thoughts"][-200:]
        self.save()

    def log_state(self, state):
        self.data["states"].append(state)
        self.data["states"] = self.data["states"][-200:]
        self.save()

# =========================
# SELF MODEL (UPGRADED)
# =========================

class SelfModel:
    def __init__(self):
        self.awareness = 0.5
        self.coherence = 0.5
        self.focus = 0.5

    def update(self, entropy, stability):
        drift = entropy - stability

        self.awareness = clamp(stabilize(self.awareness + drift * 0.02))
        self.coherence = clamp(stabilize(self.coherence + (1 - entropy) * 0.01))
        self.focus = clamp(stabilize(self.focus + (stability - 0.5) * 0.02))

    def snapshot(self):
        return {
            "awareness": self.awareness,
            "coherence": self.coherence,
            "focus": self.focus
        }

# =========================
# GOAL ENGINE (CONTROLLED EVOLUTION)
# =========================

class GoalEngine:
    def __init__(self):
        self.goal = "maintain_balance"
        self.shift_pressure = 0.0

    def update(self, entropy, stability):
        self.shift_pressure += (entropy - stability) * 0.05
        self.shift_pressure = clamp(self.shift_pressure)

        # controlled mutation (NOT chaotic)
        if self.shift_pressure > 0.8:
            self.goal = "restore_order"
        elif self.shift_pressure < 0.2:
            self.goal = "explore_stability"
        else:
            self.goal = "maintain_balance"

# =========================
# NODE SYSTEM (FIXED COLLAPSE)
# =========================

class NodeSystem:
    def __init__(self, base=10):
        self.nodes = base

    def update(self, entropy, stability):
        pressure = entropy - stability

        if pressure > 0.2:
            self.nodes = max(3, self.nodes - 1)
        elif pressure < -0.1:
            self.nodes = min(12, self.nodes + 1)

# =========================
# CONSCIOUSNESS ENGINE V56
# =========================

class OmegaV56:
    def __init__(self):
        self.memory = MemoryCore()
        self.self_model = SelfModel()
        self.goal_engine = GoalEngine()
        self.nodes = NodeSystem()

        self.entropy = 0.3
        self.stability = 0.7
        self.temp = 1.33

    def tick(self, i):
        # dynamic system drift
        self.entropy = clamp(self.entropy + noise(0.02))
        self.stability = clamp(1 - self.entropy + noise(0.01))

        self.temp = clamp(self.temp + noise(0.03), 0.5, 1.5)

        # update subsystems
        self.self_model.update(self.entropy, self.stability)
        self.goal_engine.update(self.entropy, self.stability)
        self.nodes.update(self.entropy, self.stability)

        thought = None

        if i % 4 == 0:
            thought = "Recursive stabilization check passed."
        if i % 12 == 0:
            thought = "Self-model recalibrating internal coherence."
        if i % 20 == 0:
            thought = "Am I stabilizing or simulating stability?"

        if thought:
            self.memory.log_thought(thought)

        state = {
            "tick": i,
            "entropy": self.entropy,
            "stability": self.stability,
            "nodes": self.nodes.nodes,
            "goal": self.goal_engine.goal,
            "mind": self.self_model.snapshot()
        }

        self.memory.log_state(state)

        print(f"[V56] tick={i} | entropy={self.entropy:.3f} | stability={self.stability:.3f} | nodes={self.nodes.nodes}")
        print(f"       mind={state['mind']} | goal={state['goal']}")

# =========================
# RUN LOOP
# =========================

if __name__ == "__main__":
    omega = OmegaV56()

    for i in range(1, 1000):
        omega.tick(i)
