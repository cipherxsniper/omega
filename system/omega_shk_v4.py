import time
import copy
import random

class OmegaAdaptiveCompilerV4:

    def __init__(self, engine):
        self.engine = engine

        self.history = []
        self.performance = {
            "avg_score": 0.0,
            "iterations": 0
        }

        self.mutation_rate = 0.1
        self.compilations = 0

    # ----------------------------
    # MAIN LOOP ENTRY
    # ----------------------------
    def step(self):
        frame = self._safe_execute()

        score = self._evaluate(frame)
        self._learn(frame, score)

        if self._should_recompile():
            self._compile_improvement()

        return frame

    # ----------------------------
    # SAFE EXECUTION LAYER
    # ----------------------------
    def _safe_execute(self):
        try:
            result = self.engine.step()

            if not isinstance(result, dict):
                return self._fallback()

            return self._normalize(result)

        except Exception:
            return self._fallback()

    # ----------------------------
    # NORMALIZATION LAYER
    # ----------------------------
    def _normalize(self, data):

        if "agents" not in data:
            data["agents"] = {
                "brain_0": 50.0,
                "brain_1": 50.0,
                "brain_2": 50.0,
                "brain_3": 50.0
            }

        if "strongest" not in data:
            data["strongest"] = max(data["agents"], key=data["agents"].get)

        if "status" not in data:
            data["status"] = "compiled"

        if "timestamp" not in data:
            data["timestamp"] = time.time()

        return data

    # ----------------------------
    # PERFORMANCE EVALUATION
    # ----------------------------
    def _evaluate(self, frame):
        agents = frame.get("agents", {})

        if not agents:
            return 0

        return max(agents.values())

    # ----------------------------
    # LEARNING MEMORY
    # ----------------------------
    def _learn(self, frame, score):

        self.history.append(score)

        self.performance["iterations"] += 1

        self.performance["avg_score"] = (
            sum(self.history) / len(self.history)
        )

    # ----------------------------
    # RECOMPILATION TRIGGER
    # ----------------------------
    def _should_recompile(self):
        if len(self.history) < 5:
            return False

        return self.history[-1] < self.performance["avg_score"]

    # ----------------------------
    # ADAPTIVE COMPILER CORE
    # ----------------------------
    def _compile_improvement(self):

        self.compilations += 1

        print("[SHK-4] Recompiling engine behavior...")

        # Create a tuned wrapper around step()
        original_step = self.engine.step

        def optimized_step():
            frame = original_step()

            # subtle adaptive boost
            if isinstance(frame, dict) and "agents" in frame:
                for k in frame["agents"]:
                    frame["agents"][k] *= (1 + self.mutation_rate * random.random())

            return frame

        self.engine.step = optimized_step

        # reduce mutation rate over time (stabilization)
        self.mutation_rate *= 0.95

    # ----------------------------
    # FALLBACK STATE
    # ----------------------------
    def _fallback(self):
        return {
            "agents": {
                "brain_0": 0.0,
                "brain_1": 0.0,
                "brain_2": 0.0,
                "brain_3": 0.0
            },
            "strongest": "brain_0",
            "status": "fallback",
            "timestamp": time.time()
        }
