class MotivationEngine:

    def reason(self, goal, memory_state):
        return f"""
🧠 Motivation Trace:
Current Goal: {goal['goal']}
Priority Level: {goal['priority']}

Reasoning:
This goal persists due to repeated reinforcement in system memory.
"""
