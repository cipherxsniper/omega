import time
from runtime_v7.core.omega_memory_graph_v3 import get_memory

class SwarmCognitionV12:

    def __init__(self):
        self.memory = get_memory()
        print("[V12 COGNITION] ONLINE")

    def loop(self):
        while True:
            summary = self.memory.summary()
            insights = self.memory.infer()

            print(f"[COGNITION] events={summary['total_events']} patterns={summary['total_patterns']}")

            for i in insights:
                print(f"[INSIGHT] {i}")

            time.sleep(3)

    def start(self):
        self.loop()


if __name__ == "__main__":
    SwarmCognitionV12().start()
