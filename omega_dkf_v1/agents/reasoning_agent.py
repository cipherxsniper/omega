from agents.base_agent import BaseAgent

class ReasoningAgent(BaseAgent):
    def run(self, query, context=None):
        return f"[Reasoning]\nQ: {query}\nContext: {len(context or [])} chunks"
