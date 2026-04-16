import time
from runtime_v7.core.omega_memory_graph_v3 import get_memory


class OmegaAssistantV3:
    def __init__(self):
        self.memory = get_memory()
        self.running = True
        self.last_index = 0

        print("[OMEGA ASSISTANT V3] ONLINE")
        print("[OMEGA CHAT READY V3]")
        print("Type 'exit' to quit\n")

    # -----------------------------
    # THINKING ENGINE (REAL SIGNALS)
    # -----------------------------
    def think(self, user_input: str):
        events = self.memory.memory.get("events", [])

        # detect new swarm signals
        new_events = events[self.last_index:]
        self.last_index = len(events)

        # base response logic
        if user_input.lower() in ["hello", "hi"]:
            return "I am online. Swarm memory is active."

        if "how are you" in user_input.lower():
            return "I am processing distributed swarm signals."

        if "thought" in user_input.lower():
            return "I am forming emergent patterns from memory graph."

        # if swarm events exist
        if new_events:
            last = new_events[-1]
            return f"Swarm signal detected: {last.get('type', 'unknown')}"

        # fallback ONLY when no signals exist
        return "Listening for swarm activity..."

    # -----------------------------
    # CHAT LOOP
    # -----------------------------
    def chat(self):
        while self.running:
            try:
                user = input("\n~Omega$> ")

                if user.lower() == "exit":
                    print("Shutting down Omega Assistant...")
                    break

                response = self.think(user)
                print(f"Omega > {response}")

            except KeyboardInterrupt:
                print("\nShutting down...")
                break


if __name__ == "__main__":
    OmegaAssistantV3().chat()
