# system/omega_orchestrator_v2.py

from core.memorycore_v1 import MemoryCore
from core.context_engine_v11 import ContextEngine
from core.reinforcement_core import ReinforcementCore

from engines.learning_engine_v17 import LearningEngine
from engines.aware_engine_v1 import AwareEngine
from engines.prediction_engine import PredictionEngine

from brains.brain_1 import Brain1
from brains.brain_2 import Brain2
from brains.brain_3 import Brain3

from system.health_monitor import HealthMonitor


class OmegaOrchestrator:
    def __init__(self):
        self.memory = MemoryCore()
        self.context = ContextEngine()
        self.reinforcement = ReinforcementCore()

        self.learning = LearningEngine()
        self.aware = AwareEngine()
        self.predictor = PredictionEngine()

        self.brains = [Brain1(), Brain2(), Brain3()]
        self.health = HealthMonitor()

    def run_cycle(self):
        print("\n🧠 OMEGA CYCLE\n")

        # Awareness
        obs = self.aware.observe("world", self.context.snapshot())

        # Brain processing
        for brain in self.brains:
            thought = brain.think(obs)
            print(thought)
            self.memory.store(thought)

        # Learning
        self.learning.learn(str(obs))

        # Prediction
        pred = self.predictor.simulate()
        print(f"[Prediction] {pred}")

        # Reinforcement
        self.reinforcement.evaluate("prediction", "good" if pred == "UP" else "bad")

        print(f"[Score] {self.reinforcement.get_score()}")

        # Health
        print(self.health.check())
