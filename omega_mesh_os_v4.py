import time
import random

from omega_bus_v4 import OmegaBusV4
from omega_crdt_memory_v4 import OmegaCRDTMemoryV4
from omega_lang_v4 import OmegaLangV4


class OmegaMeshOSV4:
    def __init__(self):
        self.bus = OmegaBusV4()
        self.memory = OmegaCRDTMemoryV4()
        self.lang = OmegaLangV4(self.memory.state)

        self.tick = 0
        self.entropy = 0.3

    def handle(self, msg):
        self.memory.merge({
            "nodes": {msg.get("id", "unknown"): msg},
            "ideas": {}
        })

    def run(self):
        print("[Ω-MESH OS v4] DISTRIBUTED COGNITIVE NETWORK ONLINE")

        self.bus.on_message(self.handle)
        self.bus.start()

        self.lang.exec("SPAWN_NODE core")

        while True:
            self.tick += 1

            self.entropy += random.uniform(-0.01, 0.02)
            self.entropy = max(0.1, min(0.9, self.entropy))

            if random.random() < 0.3:
                self.lang.exec(f"CREATE_IDEA idea_{self.tick}")

            if random.random() < 0.1:
                self.lang.exec("LINK idea_1 idea_2")

            self.memory.save()

            print(
                f"[Ω-v4] tick={self.tick} "
                f"nodes={len(self.memory.state['nodes'])} "
                f"ideas={len(self.memory.state['ideas'])} "
                f"entropy={self.entropy:.3f}"
            )

            time.sleep(1)


if __name__ == "__main__":
    OmegaMeshOSV4().run()
