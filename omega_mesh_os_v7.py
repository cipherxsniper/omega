import random
import time
import uuid
from collections import defaultdict


class Idea:
    def __init__(self, intent, strength, origin):
        self.id = f"idea_{uuid.uuid4().hex[:8]}"
        self.intent = intent
        self.strength = strength
        self.origin = origin
        self.age = 0

    def mutate(self):
        self.strength += random.uniform(-0.1, 0.1)
        self.strength = max(0.01, min(self.strength, 2.0))
        self.intent = random.choice([
            "explore", "link", "mutate", "compress", "stabilize"
        ])


class Brain:
    def __init__(self, brain_id, role):
        self.id = brain_id
        self.role = role
        self.bias = "neutral"

    def think(self, state):
        entropy = state["entropy"]

        intent_map = {
            "explorer": ["explore", "create_idea"],
            "mutator": ["mutate", "link"],
            "compressor": ["compress", "stabilize"],
            "linker": ["link", "expand_graph"]
        }

        intent = random.choice(intent_map[self.role])

        noise = random.uniform(-1, 1) * entropy

        return {
            "type": "thought_ir",
            "source": self.id,
            "intent": intent,
            "payload": {
                "value": noise,
                "entropy": entropy
            },
            "confidence": random.uniform(0.4, 1.0)
        }


class MeshOSv7:
    def __init__(self):
        self.tick = 0
        self.entropy = 0.5
        self.bias = "neutral"

        self.brains = [
            Brain("brain_1", "explorer"),
            Brain("brain_2", "mutator"),
            Brain("brain_3", "compressor"),
            Brain("brain_4", "linker")
        ]

        self.ideas = {}
        self.memory = []
        self.rewards = defaultdict(float)

    # ⚡ FEEDBACK LOOP (event influences state)
    def apply_feedback(self, event):
        self.entropy += event["payload"]["value"] * 0.01
        self.entropy = max(0.01, min(self.entropy, 1.5))
        self.bias = event["intent"]

    # 🧠 MEMORY PRESSURE FIELD
    def memory_pressure(self, idea):
        decay = max(0.1, 1.0 - (idea.age * 0.01))
        return idea.strength * decay

    # ⚔️ IDEA COMPETITION ENGINE
    def evolve_ideas(self):
        to_remove = []

        for idea_id, idea in self.ideas.items():
            idea.age += 1

            pressure = self.memory_pressure(idea)

            # survival check
            if pressure < 0.15:
                to_remove.append(idea_id)
                continue

            # mutation chance
            if random.random() < 0.2:
                idea.mutate()

            # reinforcement
            self.rewards[idea.intent] += pressure * 0.01

        for i in to_remove:
            del self.ideas[i]

    # 🌐 SWARM EXECUTION
    def step_brains(self):
        for brain in self.brains:
            thought = brain.think({
                "entropy": self.entropy,
                "tick": self.tick
            })

            self.ingest(thought)

    # 🧠 IDEA CREATION / LINKING
    def ingest(self, thought):
        idea = Idea(
            intent=thought["intent"],
            strength=thought["confidence"],
            origin=thought["source"]
        )

        self.ideas[idea.id] = idea
        self.memory.append(thought)

    # 🔁 MAIN ROUTING LOOP
    def step(self):
        self.tick += 1

        self.step_brains()
        self.evolve_ideas()

        # global entropy drift
        self.entropy += random.uniform(-0.02, 0.02)

        # clamp
        self.entropy = max(0.01, min(self.entropy, 2.0))

        # LOG OUTPUT
        print(f"[Ω-v7] tick={self.tick} ideas={len(self.ideas)} entropy={round(self.entropy,3)} bias={self.bias}")

        # show dominant idea signal
        if self.ideas:
            dominant = max(self.ideas.values(), key=lambda x: x.strength)
            print(f"[Ω-v7] dominant={dominant.intent} strength={round(dominant.strength,3)} origin={dominant.origin}")


if __name__ == "__main__":
    osys = MeshOSv7()

    print("[Ω-MESH OS v7] COGNITIVE ROUTING KERNEL ONLINE")

    while True:
        osys.step()
        time.sleep(0.6)
