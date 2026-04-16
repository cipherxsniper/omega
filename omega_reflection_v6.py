import random

class ReflectionEngineV6:
    def __init__(self, state):
        self.state = state

    def reflect(self):
        ideas = self.state["ideas"]

        suggestions = []

        if len(ideas) < 5:
            suggestions.append("Increase idea mutation rate for diversity.")

        strengths = [v.get("strength", 1) for v in ideas.values()]
        avg = sum(strengths) / len(strengths) if strengths else 0

        if avg < 1.0:
            suggestions.append("Increase reinforcement reward scaling.")

        if len(ideas) > 20:
            suggestions.append("Introduce pruning system for unstable ideas.")

        print("\n🧠 OMEGA SELF-REFLECTION")
        print("=" * 40)

        if suggestions:
            for s in suggestions:
                print("•", s)
        else:
            print("System is stable. No upgrades required.")

        print("=" * 40 + "\n")
