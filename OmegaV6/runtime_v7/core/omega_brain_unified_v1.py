import time
import threading
from runtime_v7.core.omega_memory_graph_v3 import get_memory


class OmegaBrainUnifiedV1:
    """
    Unified Omega Brain:
    - Chat Interface
    - Cognition Loop
    - Memory Graph Awareness
    """

    def __init__(self):
        self.memory = get_memory()

        self.running = True
        self.last_index = 0

        self.latest_thoughts = []
        self.lock = threading.Lock()

        print("[OMEGA BRAIN V1] ONLINE")
        print("[COGNITION + CHAT FUSED]")
        print("Type 'exit' to quit\n")

        # start cognition thread
        self.cognition_thread = threading.Thread(target=self.cognition_loop, daemon=True)
        self.cognition_thread.start()

    # -----------------------------
    # COGNITION LOOP (BACKGROUND)
    # -----------------------------
    def cognition_loop(self):
        while self.running:
            try:
                events = self.memory.memory.get("events", [])
                new_events = events[self.last_index:]
                self.last_index = len(events)

                thoughts = []

                for e in new_events:
                    etype = e.get("type", "unknown")

                    if etype == "heartbeat":
                        thoughts.append("Detected live swarm heartbeat signal.")
                    elif etype == "ping":
                        thoughts.append("Network probe detected from node.")
                    else:
                        thoughts.append(f"Event processed: {etype}")

                with self.lock:
                    self.latest_thoughts = thoughts[-5:]  # keep last few

                time.sleep(1)

            except Exception as e:
                print("[COGNITION ERROR]", e)
                time.sleep(2)

    # -----------------------------
    # RESPONSE ENGINE
    # -----------------------------
    def generate_response(self, user_input: str):

        user_input = user_input.lower()

        # basic identity responses
        if "hello" in user_input:
            return "I am online as a unified cognition system."

        if "how are you" in user_input:
            return "I am actively processing swarm memory streams."

        if "what are you thinking" in user_input or "thought" in user_input:
            with self.lock:
                if self.latest_thoughts:
                    return " | ".join(self.latest_thoughts)
                return "No active cognitive signals yet."

        # memory-aware response
        events = self.memory.memory.get("events", [])

        if events:
            last = events[-1]
            return f"Last swarm event: {last.get('type', 'unknown')}"

        return "Listening to system bus..."

    # -----------------------------
    # CHAT LOOP
    # -----------------------------
    def chat(self):
        while self.running:
            try:
                user = input("\n~Omega$> ")

                if user.strip().lower() == "exit":
                    self.running = False
                    print("Omega Brain shutting down...")
                    break

                response = self.generate_response(user)
                print(f"Omega > {response}")

            except KeyboardInterrupt:
                self.running = False
                print("\nShutdown signal received.")
                break


if __name__ == "__main__":
    OmegaBrainUnifiedV1().chat()
