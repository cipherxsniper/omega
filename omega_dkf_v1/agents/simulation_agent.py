from agents.base_agent import BaseAgent

class SimulationAgent(BaseAgent):
    def run(self, query, context=None):
        return f"[Simulation] running scenario for: {query}"
