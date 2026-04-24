class ReasonerAgent:
    def run(self, llm, prompt):
        return llm.generate(f"Reason step by step:\n{prompt}")
