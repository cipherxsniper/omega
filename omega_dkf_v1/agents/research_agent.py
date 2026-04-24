from agents.base_agent import BaseAgent

class ResearchAgent(BaseAgent):
    def run(self, query, context=None):
        return f"[Research] analyzing: {query}"
