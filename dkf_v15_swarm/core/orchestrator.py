from core.llm_client import LLMClient
from agents.reasoner import ReasonerAgent
from agents.critic import CriticAgent
from agents.executor import ExecutorAgent

class SwarmOrchestrator:
    def __init__(self):
        self.llm = LLMClient()
        self.reasoner = ReasonerAgent()
        self.critic = CriticAgent()
        self.executor = ExecutorAgent()

    def process(self, prompt):
        step1 = self.reasoner.run(self.llm, prompt)
        step2 = self.critic.run(self.llm, step1)
        final = self.executor.run(self.llm, step2)
        return final
