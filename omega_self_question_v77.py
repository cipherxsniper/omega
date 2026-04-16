class OmegaSelfQuestionV77:
    def ask(self, state):
        stability = state.get("stability", 0.5)

        if stability < 0.4:
            return "Why is system stability degrading?"
        if state.get("final_node") == "temporal":
            return "Why is routing stuck on temporal node?"
        return "What changed in the last cognition cycle?"
