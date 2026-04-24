class ExecutorAgent:
    def run(self, llm, refined):
        return llm.generate(f"Finalize and format clean response:\n{refined}")
