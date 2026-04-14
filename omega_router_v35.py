import json
import time
from omega_bus import read_bus, write_bus


# =========================
# 🧠 MESSAGE ROUTER
# =========================
class CognitiveRouter:
    def __init__(self):
        self.trust = {
            "attention": 1.0,
            "memory": 1.0,
            "goal": 1.0,
            "stability": 1.0
        }

    # -------------------------
    # SCORE SIGNAL IMPORTANCE
    # -------------------------
    def score(self, signal):
        base = signal.get("signal", 0.5)

        node = signal.get("node", "unknown")
        trust = self.trust.get(node, 1.0)

        return base * trust

    # -------------------------
    # ROUTE SIGNALS
    # -------------------------
    def route(self, signals):
        scored = []

        for s in signals:
            scored.append((self.score(s), s))

        scored.sort(reverse=True, key=lambda x: x[0])

        # keep top 30% signals only (selective cognition)
        cutoff = max(1, int(len(scored) * 0.3))

        return [s for _, s in scored[:cutoff]]


# =========================
# 🧠 REINFORCEMENT ENGINE
# =========================
class ReinforcementEngine:
    def __init__(self, router):
        self.router = router
        self.reward_memory = {}

    def update(self, routed_signals):

        for s in routed_signals:
            node = s.get("node")
            value = s.get("signal", 0.0)

            reward = abs(value)  # proxy reward signal

            if node not in self.reward_memory:
                self.reward_memory[node] = []

            self.reward_memory[node].append(reward)

            # keep bounded history
            self.reward_memory[node] = self.reward_memory[node][-50:]

            # compute reinforcement
            avg_reward = sum(self.reward_memory[node]) / len(self.reward_memory[node])

            # update trust (LEARNING STEP)
            self.router.trust[node] = (
                self.router.trust.get(node, 1.0) * 0.9
                + avg_reward * 0.1
            )


# =========================
# 🧠 V35 RUNTIME
# =========================
class OmegaV35:
    def __init__(self):
        self.router = CognitiveRouter()
        self.reinforce = ReinforcementEngine(self.router)

    def step(self):

        bus = read_bus()
        signals = bus.get("signals", [])

        # 🧠 ROUTE SIGNALS (SELECTIVE ATTENTION)
        routed = self.router.route(signals)

        # 🧠 LEARN FROM ROUTED SIGNALS
        self.reinforce.update(routed)

        # 🧠 WRITE BACK SYSTEM STATE
        bus["router_state"] = {
            "trust": self.router.trust,
            "routed_count": len(routed),
            "total_signals": len(signals)
        }

        write_bus(bus)

        print(
            f"[V35] routed={len(routed)} | "
            f"trust={ {k: round(v,2) for k,v in self.router.trust.items()} }"
        )

    def run(self):
        print("[V35] COGNITIVE ROUTER + REINFORCEMENT ONLINE")

        while True:
            self.step()
            time.sleep(1)


if __name__ == "__main__":
    OmegaV35().run()
