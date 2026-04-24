from core.runtime import Runtime
from governance.permissions import PermissionEngine
from rag.retriever import Retriever
from agents.reasoning_agent import ReasoningAgent

class DKFOrchestrator:
    def __init__(self):
        self.runtime = Runtime()
        self.permissions = PermissionEngine()
        self.retriever = Retriever()
        self.reasoning = ReasoningAgent()

    def boot(self):
        self.runtime.initialize()
        print("🧠 DKF Orchestrator Online")

    def process(self, query):
        if not self.permissions.allow(query):
            return "⛔ Blocked by governance"

        context = self.retriever.search(query)
        return self.reasoning.run(query, context)
