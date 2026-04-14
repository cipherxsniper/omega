import time
import threading

from core.intelligence import OmegaMind
from core.swarm import SwarmNetwork
from core.ingestion import DataStreamBus
from core.memory import MemoryBus
from core.evolver import Evolver


class Orchestrator:
    def __init__(self):
        self.running = True

        # 🧠 CORE SYSTEMS
        self.memory = 5050
        self.mind = OmegaMind(self.memory)
        self.swarm = SwarmNetwork(self.memory)
        self.data = DataStreamBus()
        self.evolver = Evolver()

    def boot(self):
        print("[KERNEL] OMEGA UNIFIED SYSTEM ONLINE")

        threading.Thread(target=self.swarm.listen, daemon=True).start()
        threading.Thread(target=self.data.run, daemon=True).start()
        threading.Thread(target=self.learning_loop, daemon=True).start()

        while self.running:
            time.sleep(1)

    def learning_loop(self):
        while self.running:
            try:
                features = self.data.get_features()

                decision = self.mind.step(features)

                self.memory.store("system", {
                    "features": features,
                    "decision": decision
                })

                self.swarm.broadcast({
                    "decision": decision
                })

                if self.mind.should_evolve():
                    self.evolver.suggest_patch()

            except Exception as e:
                print("[KERNEL ERROR]", e)

            time.sleep(2)
