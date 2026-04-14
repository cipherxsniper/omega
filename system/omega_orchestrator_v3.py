# system/omega_orchestrator_v3.py

from core.memorycore_v1 import MemoryCore
from core.context_engine_v11 import ContextEngine
from core.reinforcement_core_v2  import ReinforcementCore
from core.goal_engine_v1 import GoalEngine
from core.self_modifier_v1 import SelfModifier

from engines.learning_engine_v17 import LearningEngine
from engines.aware_engine_v1 import AwareEngine
from engines.prediction_engine import PredictionEngine
from engines.internet_engine_v1 import InternetEngine

from brains.brain_autonomous import AutonomousBrain

from system.health_monitor import HealthMonitor


class OmegaOrchestratorV3:
    def __init__(self):
        # 🧠 Core Systems
        self.memory = MemoryCore()
        self.context = ContextEngine()
        self.reinforcement = ReinforcementCore()
        self.goals = GoalEngine()
        self.modifier = SelfModifier()

        # ⚙️ Engines
        self.learning = LearningEngine()
        self.aware = AwareEngine()
        self.predictor = PredictionEngine()
        self.internet = InternetEngine()

        # 🤖 Brain
        self.brain = AutonomousBrain()

        # ❤️ Health
        self.health = HealthMonitor()

    def run_cycle(self):
        print("\n🚀 OMEGA V3 CYCLE\n")

        # 🌐 1. INTERNET DATA INGESTION
        data = self.internet.ingest()
        print("[Internet]", data)

        # 🧠 2. CONTEXT UPDATE
        self.context.update("last_data", data)

        # 👁 3. AWARENESS
        awareness = self.aware.observe("environment", self.context.snapshot())
        print("[Awareness]", awareness)

        # 🎯 4. GOAL SELECTION
        goal = self.goals.get_active_goal()
        print("[Goal]", goal)

        # 🔮 5. PREDICTION
        prediction = self.predictor.simulate()
        print("[Prediction]", prediction)

        # 🤖 6. DECISION MAKING
        decision = self.brain.decide(goal["goal"], prediction, data)
        print("[Decision]", decision)

        # 🧠 7. MEMORY STORAGE
        self.memory.store(decision, tag="decision")

        # 🧠 8. MEMORY USAGE (NEW 🔥)
        recent_memory = self.memory.retrieve()
        if recent_memory:
            print("[Memory Insight]", recent_memory[-1])

        # ⚡ 9. LEARNING
        learned = self.learning.learn(str(data))
        print(learned)

        # 🔁 10. REINFORCEMENT FEEDBACK
        if "Adjust" in decision or "Optimize" in decision:
            outcome = "good"
        elif "Idle" in decision:
            outcome = "bad"
        else:
            outcome = "neutral"

        self.reinforcement.evaluate(prediction)

        print("[Score]", self.reinforcement.get_score())
        print("[Trend]", self.reinforcement.intelligence_trend())

        # 🧬 11. CONTROLLED SELF-EVOLUTION (FIXED 🔥)
        if self.reinforcement.get_score() < -5:
            print("[Evolution Triggered]")
            print(self.modifier.evolve_brain())

        # 🎯 12. GOAL PROGRESSION
        self.goals.complete_goal(goal)
        new_goal = self.goals.generate_new_goal()
        print("[New Goal Generated]", new_goal)

        # ❤️ 13. SYSTEM HEALTH
        print("[Health]", self.health.check())

        print("\n🧠 END CYCLE\n")
