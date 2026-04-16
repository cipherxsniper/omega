import time
import random

from omega_crdt_v5 import CRDTGraphV5
from omega_reinforcement_v5 import ReinforcementEngineV5
from omega_mutation_v5 import MutationEngineV5
from omega_bus_v5 import OmegaBusV5
from omega_lang_v5 import OmegaLangV5


class OmegaMeshOSV5:
    def __init__(self):
        self.crdt = CRDTGraphV5()
        self.state = self.crdt.state

        self.reinforce = ReinforcementEngineV5(self.state)
        self.mutate = MutationEngineV5(self.state)
        self.bus = OmegaBusV5()
        self.lang = OmegaLangV5(self.state)

        self.tick = 0

    def handle(self, msg):
        idea = msg.get("idea")
        if idea:
            self.reinforce.reward(idea, 0.2)

    def run(self):
        print("[Ω-MESH OS v5] TRUE COGNITIVE SWARM ONLINE")

        self.bus.on(self.handle)
        self.bus.start()

        self.lang.exec("IDEA seed")

        while True:
            self.tick += 1

            self.reinforce.decay_and_select()
            self.mutate.evolve()

            if random.random() < 0.4:
                self.lang.exec(f"IDEA idea_{self.tick}")

            if random.random() < 0.2:
                self.lang.exec("LINK seed idea_1")

            self.crdt.save()

            print(
                f"[Ω-v5] tick={self.tick} "
                f"ideas={len(self.state['ideas'])}"
            )

            time.sleep(1)


if __name__ == "__main__":
    OmegaMeshOSV5().run()
