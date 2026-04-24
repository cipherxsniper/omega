from agents.base_agent import BaseAgent

class CriticAgent(BaseAgent):
    def run(self, query, context=None):
        return f"[Critic] evaluating: {query}"
