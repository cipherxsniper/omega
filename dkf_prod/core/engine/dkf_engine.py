class DKFEngine:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.memory = []

    def process(self, user_input):
        context = "\n".join(self.memory[-5:])

        prompt = f"""
You are DKF CORE SYSTEM.

Context:
{context}

User:
{user_input}

Respond with:
1. Answer
2. Reasoning
3. One follow-up question
"""

        response = self.llm.generate(prompt)
        self.memory.append(user_input)
        self.memory.append(response)

        return response
