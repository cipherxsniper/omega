from runtime_v7.core.omega_memory_graph_v2 import get_memory

class OmegaAssistant:

    def __init__(self):
        self.memory = get_memory()
        print("[OMEGA ASSISTANT] ONLINE")

    def think(self, user_input):
        summary = self.memory.summary()

        if summary["event_types"] == 0:
            return "I am just waking up. No signals yet."

        if "feel" in user_input:
            return f"I sense {summary['event_types']} active signals forming structure."

        if "idea" in user_input:
            return "If signals repeat, they form behavior. Behavior becomes intelligence."

        if "what" in user_input:
            return f"I am tracking {summary['event_types']} signal types and evolving patterns."

        return "I am processing and learning from the swarm."

    def chat(self):
        print("\n[OMEGA CHAT READY]")
        print("Type 'exit' to quit\n")

        while True:
            user = input("You > ")

            if user.lower() == "exit":
                break

            response = self.think(user)
            print(f"Omega > {response}")


if __name__ == "__main__":
    OmegaAssistant().chat()
