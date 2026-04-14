import multiprocessing as mp
import random
import time
import os


# =========================================================
# Ω-LANG COMPILER (MINIMAL EXEC ENGINE)
# =========================================================
class OmegaLangCompiler:
    def execute(self, instruction, state, node_id):
        cmd = instruction.split()

        if not cmd:
            return

        if cmd[0] == "SPAWN_IDEA":
            idea = cmd[1]
            state["ideas"].append({
                "name": idea,
                "energy": random.uniform(0.5, 1.2),
                "owner": node_id
            })

        elif cmd[0] == "BOOST":
            for idea in state["ideas"]:
                if idea["name"] == cmd[1]:
                    idea["energy"] += 0.1

        elif cmd[0] == "DECAY":
            for idea in state["ideas"]:
                idea["energy"] *= 0.99


# =========================================================
# FITNESS FUNCTION (REINFORCEMENT SIGNAL)
# =========================================================
def compute_fitness(idea):
    return idea["energy"] / (1 + random.random() * 0.01)


# =========================================================
# NODE PROCESS (TRUE PARALLEL AGENT)
# =========================================================
def node_process(node_id, state, lock):
    compiler = OmegaLangCompiler()

    while True:
        time.sleep(random.uniform(0.1, 0.3))

        with lock:
            # -----------------------------
            # 1. OBSERVE GLOBAL STATE
            # -----------------------------
            ideas = state["ideas"]

            # -----------------------------
            # 2. THINK (select idea)
            # -----------------------------
            if ideas:
                idea = random.choice(ideas)

                fitness = compute_fitness(idea)

                # reinforcement learning update
                if fitness > 0.8:
                    instruction = f"BOOST {idea['name']}"
                else:
                    instruction = f"DECAY {idea['name']}"

                compiler.execute(instruction, state, node_id)

            # -----------------------------
            # 3. GENERATE NEW IDEAS
            # -----------------------------
            if random.random() < 0.2:
                new_idea = f"idea_{random.randint(0,999)}"
                compiler.execute(f"SPAWN_IDEA {new_idea}", state, node_id)

            # -----------------------------
            # 4. GLOBAL ENTROPY DRIFT
            # -----------------------------
            state["entropy"] += random.uniform(-0.01, 0.02)
            state["tick"] += 1

            # -----------------------------
            # 5. LOG LIGHTLY
            # -----------------------------
            if state["tick"] % 20 == 0:
                print(
                    f"[Ω-v3] tick={state['tick']} "
                    f"ideas={len(state['ideas'])} "
                    f"entropy={state['entropy']:.3f} "
                    f"node={node_id}"
                )


# =========================================================
# KERNEL BOOTSTRAP
# =========================================================
class OmegaOSv3:
    def __init__(self):
        self.manager = mp.Manager()

        self.state = self.manager.dict()
        self.state["ideas"] = self.manager.list()
        self.state["entropy"] = 0.3
        self.state["tick"] = 0

        self.lock = mp.Lock()
        self.processes = []

    def spawn_nodes(self, n=4):
        for i in range(n):
            p = mp.Process(
                target=node_process,
                args=(f"node_{i}", self.state, self.lock)
            )
            self.processes.append(p)

    def run(self):
        print("[Ω-OS v3] Multiprocess Cognitive Kernel ONLINE")

        self.spawn_nodes(6)

        for p in self.processes:
            p.start()

        # kernel watchdog
        while True:
            time.sleep(2)

            with self.lock:
                ideas = self.state["ideas"]

                # global fitness sorting
                ranked = sorted(
                    ideas,
                    key=lambda x: x["energy"],
                    reverse=True
                )

                self.state["ideas"][:] = ranked[:50]

                if self.state["tick"] % 50 == 0:
                    print(
                        f"[KERNEL] tick={self.state['tick']} "
                        f"ideas={len(self.state['ideas'])} "
                        f"entropy={self.state['entropy']:.3f}"
                    )


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    OmegaOSv3().run()
