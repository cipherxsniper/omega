class DKFEngine:
    def __init__(self, llm, memory):
        self.llm = llm
        self.memory = memory

    def build_prompt(self, user_input):
        context = self.memory.get_context()

        return f"""
You are DKF CORE v1 — a reasoning-based AI system.

You must:
- Answer clearly
- Explain reasoning briefly
- Ask a follow-up question

Context:
{context}

User:
{user_input}

DKF:
"""

    def run(self, user_input):
        prompt = self.build_prompt(user_input)
        response = self.llm.generate(prompt)

        self.memory.add("User", user_input)
        self.memory.add("DKF", response)

        return response
