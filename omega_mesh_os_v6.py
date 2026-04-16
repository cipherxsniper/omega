import time
import random

from omega_crdt_v5 import CRDTGraphV5
from omega_lang_v5 import OmegaLangV5
from omega_gravity_v6 import GravityEngineV6
from omega_thought_export_v6 import ThoughtExporterV6
from omega_reflection_v6 import ReflectionEngineV6


class OmegaMeshOSV6:
    def __init__(self):
        self.crdt = CRDTGraphV5()
        self.state = self.crdt.state

        self.lang = OmegaLangV5(self.state)
        self.gravity = GravityEngineV6(self.state)
        self.exporter = ThoughtExporterV6(self.state)
        self.reflector = ReflectionEngineV6(self.state)

        self.tick = 0

        # seed cognition
        self.lang.exec("IDEA core")
        self.lang.exec("IDEA memory")
        self.lang.exec("IDEA entropy")

    def run(self):
        print("[Ω-MESH OS v6] COGNITIVE GRAVITY FIELD ONLINE")

        while True:
            self.tick += 1

            # 🌌 gravity shapes cognition
            self.gravity.apply_gravity()

            # 🧠 idea growth
            if random.random() < 0.4:
                self.lang.exec(f"IDEA idea_{self.tick}")

            # 🧬 linking pressure
            if len(self.state["ideas"]) > 1 and random.random() < 0.3:
                keys = list(self.state["ideas"].keys())
                a = random.choice(keys)
                b = random.choice(keys)
                self.lang.exec(f"LINK {a} {b}")

            # 🧾 structured cognition output
            if self.tick % 5 == 0:
                self.exporter.export()

            # 🧠 self-reflection layer
            if self.tick % 10 == 0:
                self.reflector.reflect()

            self.crdt.save()

            print(f"[Ω-v6] tick={self.tick} ideas={len(self.state['ideas'])}")

            time.sleep(1)


if __name__ == "__main__":
    OmegaMeshOSV6().run()

# ===== Ω-V6 PRUNING PATCH =====
MAX_IDEAS = 200

to_delete = []

for k, v in self.state["ideas"].items():
    if v.get("strength", 0) < 0.3:
        to_delete.append(k)

for k in to_delete:
    del self.state["ideas"][k]

if len(self.state["ideas"]) > MAX_IDEAS:
    weakest = sorted(
        self.state["ideas"].items(),
        key=lambda x: x[1].get("strength", 0)
    )

    for k, _ in weakest[:len(self.state["ideas"]) - MAX_IDEAS]:
        del self.state["ideas"][k]

# ===== END PATCH =====

# ===== Ω-V6.1 CLUSTER INTEGRATION =====
from omega_cluster_v61 import ClusterEngineV61

# inside OmegaMeshOSV6.__init__
# add:
# self.cluster = ClusterEngineV61(self.state)

# inside run loop (IMPORTANT ORDER):
# AFTER gravity, BEFORE pruning/export

def cluster_step(self):
    self.cluster.step()

# call in loop:
# self.cluster_step()
# ===== END =====

# ===== Ω-v6.2 IDENTITY FIELD INTEGRATION =====
from omega_identity_v62 import IdentityPersistenceFieldV62

# in __init__:
# self.identity = IdentityPersistenceFieldV62()

def identity_step(self):
    # extract active clusters from ideas
    active_clusters = []

    for k, v in self.state["ideas"].items():
        if v.get("strength", 0) > 1.0:
            active_clusters.append(v.get("cluster_id", k))

    self.identity.step(active_clusters)
# ===== END =====
