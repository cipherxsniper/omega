# system/omega_orchestrator_v4_2.py

from core.memorycore_v2 import MemoryCore
from core.context_engine_v2 import ContextEngine
from core.goal_engine_v2 import GoalEngine
from core.reinforcement_core_v2 import ReinforcementCore
from core.memory_graph_v2 import MemoryGraph
from core.reasoning_engine_v2 import ReasoningEngine
from core.self_modifier_v2 import SelfModifier

from engines.internet_engine_v2 import InternetEngine
from engines.prediction_engine_v2 import PredictionEngine
from engines.action_engine_v2 import ActionEngine


class Omega:
    def __init__(self):
        self.state = {
            "memory": [],
            "goals": [],
            "predictions": [],
            "actions": [],
            "score": 0,
            "knowledge_graph": {}
        }

        self.memory = MemoryCore(self.state)
        self.context = ContextEngine(self.state)
        self.goals = GoalEngine(self.state)
        self.reinforce = ReinforcementCore(self.state)
        self.graph = MemoryGraph(self.state)
        self.reason = ReasoningEngine(self.state)
        self.modifier = SelfModifier()

        self.internet = InternetEngine()
        self.predict = PredictionEngine(self.state)
        self.action = ActionEngine(self.state)

    def run(self):
        print("\n🧠 OMEGA V4.2 CYCLE\n")

        data = self.internet.ingest()
        goal = self.goals.get_active_goal()
        prediction = self.predict.predict()
        context = self.context.build_context()

        decision = self.reason.reason(goal["goal"], prediction, context)
        action = self.action.execute(decision)

        self.memory.store(data, "input")
        self.memory.store(decision, "decision")

        score = self.reinforce.evaluate(decision, data)

        self.graph.build()

        print("[Goal]", goal)
        print("[Prediction]", prediction)
        print("[Decision]", decision)
        print("[Action]", action)
        print("[Score]", score)
        print("[Graph]", self.graph.stats())

        if score < -10:
            print("[Evolution]", self.modifier.evolve())

        self.goals.generate_goal()
