from agents.base_agent import BaseAgent

class ExecutorAgent(BaseAgent):
    def run(self, query, context=None):
        return f"[Executor] executing: {query}"
