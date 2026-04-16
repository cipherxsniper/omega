from runtime_v7.core.omega_memory_graph_v3 import get_memory

class OmegaAssistant:

    def __init__(self):
        self.memory = get_memory()
        print("[OMEGA ASSISTANT V2] ONLINE")

    def think(self, user_input):
        summary = self.memory.summary()
        insights = self.memory.infer()

        if summary["total_events"] == 0:
            return "I am awake, but no signals have reached me yet."

        if "feel" in user_input:
            return f"I feel {summary['total_events']} signals flowing through my system."

        if "idea" in user_input:
            if insights:
                return f"My idea: {insights[0]}"
            return "Patterns are forming, but not yet stable."

        if "what" in user_input:
            return f"I am tracking {summary['event_types']} event types and evolving behavior."

        if insights:
            return f"I am noticing: {', '.join(insights[:2])}"

        return "I am learning."

    def chat(self):
        print("\n[OMEGA CHAT READY V2]")
        print("Type 'exit' to quit\n")

        while True:
            user = input("You > ")

            if user.lower() == "exit":
                break

            print("Omega >", self.think(user))


if __name__ == "__main__":
    OmegaAssistant().chat()
