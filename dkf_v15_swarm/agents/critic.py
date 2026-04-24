class CriticAgent:
    def run(self, llm, response):
        return llm.generate(f"Critique this response for correctness and improve it:\n{response}")
