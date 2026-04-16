import time
import threading

from runtime_v7.core.v9_9_swarm_bus_v14 import SwarmBusV14
from runtime_v7.core.omega_semantic_engine_v1 import SemanticEngineV1


class OmegaV15:

    def __init__(self):
        print("\n🧠🌍 [OMEGA V15] SEMANTIC COGNITION SYSTEM BOOTING...\n")

        # ----------------------------
        # CORE LAYERS
        # ----------------------------
        self.bus = SwarmBusV14()
        self.semantic = SemanticEngineV1()

        self.running = True

        # attach hook into bus memory stream
        threading.Thread(target=self.semantic_loop, daemon=True).start()
        threading.Thread(target=self.thought_loop, daemon=True).start()

        print("\n🟢 [OMEGA V15] ONLINE — SEMANTIC INTELLIGENCE ACTIVE\n")

    # =====================================================
    # SEMANTIC PIPELINE
    # =====================================================
    def semantic_loop(self):
        last_index = 0

        while self.running:
            try:
                events = self.bus.memory.state.get("events", [])
                new_events = events[last_index:]
                last_index = len(events)

                for e in new_events:
                    self.semantic.interpret(e)

                time.sleep(0.1)

            except Exception as e:
                print("[SEMANTIC LOOP ERROR]", e)

    # =====================================================
    # THOUGHT GENERATION LOOP
    # =====================================================
    def thought_loop(self):
        while self.running:
            try:
                thought = self.semantic.generate_thought()
                print(f"[V15 THOUGHT] {thought}")

                time.sleep(2)

            except Exception as e:
                print("[THOUGHT LOOP ERROR]", e)

    # =====================================================
    # RUN
    # =====================================================
    def run(self):
        print("\n~OmegaV15$> system online (type exit)\n")

        while True:
            cmd = input("~OmegaV15$> ")

            if cmd == "exit":
                break

            self.bus.memory.apply({
                "type": "user_input",
                "content": cmd
            })

            print("[OMEGA]", cmd)


if __name__ == "__main__":
    OmegaV15().run()
