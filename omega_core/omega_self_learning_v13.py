# 🧠 Omega v13 Self-Adaptive Learning Core (RL-style system)

import random
import math


class SelfLearningSystem:

    def __init__(self):

        # policy weights per node (learned parameters)
        self.weights = {
            "attention": 0.5,
            "goal": 0.5,
            "memory": 0.5,
            "stability": 0.5
        }

        self.learning_rate = 0.05
        self.history = []

    # --------------------------------------
    # policy decision (forward pass)
    # --------------------------------------
    def forward(self, state):

        score = 0.0

        for k in self.weights:
            score += state.get(k, 0.0) * self.weights[k]

        noise = random.uniform(-0.02, 0.02)

        return max(0.0, min(1.0, score + noise))

    # --------------------------------------
    # reward function (core intelligence signal)
    # --------------------------------------
    def reward(self, state, action_score):

        stability = state.get("stability", 0.5)
        goal = state.get("goal", 0.5)

        # reward = success alignment - instability penalty
        return (goal * action_score) - (1 - stability) * 0.5

    # --------------------------------------
    # learning update (gradient-like update)
    # --------------------------------------
    def update(self, state, action_score):

        r = self.reward(state, action_score)

        self.history.append(r)

        # stabilize history
        self.history = self.history[-200:]

        for k in self.weights:

            gradient = state.get(k, 0.0) * r

            self.weights[k] += self.learning_rate * gradient

            self.weights[k] = max(0.01, min(1.0, self.weights[k]))

    # --------------------------------------
    # training step
    # --------------------------------------
    def step(self, state):

        action_score = self.forward(state)

        self.update(state, action_score)

        return {
            "score": action_score,
            "weights": self.weights,
            "reward": self.history[-1] if self.history else 0
        }
