# ============================================================
# OMEGA ECONOMY ENGINE v5
# AUTONOMOUS GOAL + REWARD + RESOURCE ALLOCATION SYSTEM
# ============================================================

import time
import uuid


# ============================================================
# 🎯 GOAL SYSTEM
# ============================================================

class OmegaGoalEngine:
    def __init__(self, mesh, state):
        self.mesh = mesh
        self.state = state
        self.goals = {}

    def create_goal(self, description, priority=0.5):
        goal_id = str(uuid.uuid4())

        self.goals[goal_id] = {
            "description": description,
            "priority": priority,
            "reward": 0,
            "progress": 0,
            "created": time.time()
        }

        self.state.add_knowledge({
            "type": "goal_created",
            "goal": self.goals[goal_id]
        })

        return goal_id

    def update_progress(self, goal_id, value):
        if goal_id in self.goals:
            self.goals[goal_id]["progress"] += value

    def complete_goal(self, goal_id):
        if goal_id in self.goals:
            self.goals[goal_id]["reward"] += 1.0
            self.state.add_knowledge({
                "type": "goal_completed",
                "goal": self.goals[goal_id]
            })

            self.mesh.publish(
                "goal_completed",
                data=self.goals[goal_id],
                source="goal_engine"
            )


# ============================================================
# 💰 REWARD SYSTEM
# ============================================================

class OmegaRewardSystem:
    def __init__(self, state):
        self.state = state
        self.score = 0

    def reward(self, amount, reason=""):
        self.score += amount

        self.state.add_knowledge({
            "type": "reward",
            "amount": amount,
            "reason": reason
        })

    def penalize(self, amount, reason=""):
        self.score -= amount

        self.state.add_knowledge({
            "type": "penalty",
            "amount": amount,
            "reason": reason
        })


# ============================================================
# ⚙️ RESOURCE ALLOCATION ENGINE
# ============================================================

class OmegaResourceAllocator:
    def __init__(self, decision_engine):
        self.decision_engine = decision_engine

    def adjust_brain_focus(self, context="default"):
        weights = self.decision_engine.weights

        # simple adaptive focus logic
        for brain in weights:
            if context == "risk":
                weights[brain] *= 0.9
            elif context == "prediction":
                weights[brain] *= 1.05
            elif context == "noise":
                weights[brain] *= 0.95

        # normalize
        total = sum(weights.values())
        for k in weights:
            weights[k] /= total

        return weights


# ============================================================
# 🔁 STRATEGY ENGINE
# ============================================================

class OmegaStrategyEngine:
    def __init__(self):
        self.active_strategy = "balanced"

    def select_strategy(self, context_score):
        if context_score > 0.8:
            self.active_strategy = "aggressive"
        elif context_score > 0.5:
            self.active_strategy = "balanced"
        else:
            self.active_strategy = "defensive"

        return self.active_strategy
