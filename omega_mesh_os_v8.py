import random
import time
import uuid
from collections import defaultdict


# =========================
# 🧠 IDEA OBJECT (EVOLVING ENTITY)
# =========================
class Idea:
    def __init__(self, intent, strength, origin):
        self.id = f"idea_{uuid.uuid4().hex[:8]}"
        self.intent = intent
        self.strength = strength
        self.origin = origin

        self.age = 0
        self.fitness = 0.5
        self.reinforcement = 0.0

    def mutate(self):
        # stochastic drift
        self.strength += random.uniform(-0.08, 0.08)
        self.strength = max(0.01, min(self.strength, 2.0))

        # intent mutation pressure
        if random.random() < 0.3:
            self.intent = random.choice([
                "explore",
                "link",
                "mutate",
                "compress",
                "stabilize",
                "expand",
                "analyze"
            ])


# =========================
# 🧠 BRAIN NODE (SPECIALIZED AGENT)
# =========================
class Brain:
    def __init__(self, brain_id, role):
        self.id = brain_id
        self.role = role

        # adaptive bias learned over time
        self.intent_weights = defaultdict(lambda: 1.0)

    def select_intent(self, entropy):
        base_intents = {
            "explorer": ["explore", "expand", "create_idea"],
            "mutator": ["mutate", "link"],
            "compressor": ["compress", "stabilize"],
            "linker": ["link", "analyze"]
        }

        candidates = base_intents[self.role]

        # weighted learning influence
        weights = [self.intent_weights[i] for i in candidates]

        # entropy influences randomness
        if random.random() < entropy:
            return random.choice(candidates)

        return random.choices(candidates, weights=weights, k=1)[0]

    def think(self, state):
        intent = self.select_intent(state["entropy"])

        noise = random.uniform(-1, 1) * state["entropy"]

        return {
            "type": "thought_ir",
            "source": self.id,
            "intent": intent,
            "payload": {
                "value": noise,
                "entropy": state["entropy"]
            },
            "confidence": random.uniform(0.4, 1.0)
        }


# =========================
# 🧠 MESH OS v8 (LEARNING CORE)
# =========================
class MeshOSv8:
    def __init__(self):
        self.tick = 0
        self.entropy = 0.5

        self.brains = [
            Brain("brain_1", "explorer"),
            Brain("brain_2", "mutator"),
            Brain("brain_3", "compressor"),
            Brain("brain_4", "linker"),
        ]

        self.ideas = {}
        self.memory = []

        # ⚖️ reward system
        self.rewards = defaultdict(float)
        self.fitness_history = defaultdict(list)

    # =========================
    # ⚡ FEEDBACK LOOP (STATE LEARNING)
    # =========================
    def apply_feedback(self, event):
        self.entropy += event["payload"]["value"] * 0.01
        self.entropy = max(0.01, min(self.entropy, 1.5))

        intent = event["intent"]

        # reward signal
        reward = abs(event["payload"]["value"]) * event["confidence"]
        self.rewards[intent] += reward

    # =========================
    # 🧠 FITNESS FUNCTION
    # =========================
    def compute_fitness(self, idea):
        reward = self.rewards.get(idea.intent, 0.0)

        # entropy pressure = exploration incentive
        entropy_pressure = self.entropy * random.uniform(0.0, 0.2)

        fitness = (idea.strength * 0.6) + (reward * 0.4) - entropy_pressure

        idea.fitness = fitness

        self.fitness_history[idea.intent].append(fitness)

        return fitness

    # =========================
    # ⚔️ IDEA EVOLUTION ENGINE
    # =========================
    def evolve_ideas(self):
        to_delete = []

        for idea_id, idea in self.ideas.items():
            idea.age += 1

            fitness = self.compute_fitness(idea)

            # survival threshold
            if fitness < 0.2:
                to_delete.append(idea_id)
                continue

            # reinforcement learning update
            idea.reinforcement += fitness * 0.05

            # mutation pressure
            if random.random() < 0.25:
                idea.mutate()

        for i in to_delete:
            del self.ideas[i]

    # =========================
    # 🌐 BRAIN EXECUTION
    # =========================
    def step_brains(self):
        for brain in self.brains:
            thought = brain.think({
                "entropy": self.entropy,
                "tick": self.tick
            })

            self.ingest(thought)

    # =========================
    # 🧠 INGEST THOUGHT → IDEA
    # =========================
    def ingest(self, thought):
        idea = Idea(
            intent=thought["intent"],
            strength=thought["confidence"],
            origin=thought["source"]
        )

        self.ideas[idea.id] = idea
        self.memory.append(thought)

        # apply immediate feedback learning
        self.apply_feedback(thought)

    # =========================
    # 🔁 MAIN LOOP
    # =========================
    def step(self):
        self.tick += 1

        self.step_brains()
        self.evolve_ideas()

        # entropy drift
        self.entropy += random.uniform(-0.02, 0.02)
        self.entropy = max(0.01, min(self.entropy, 2.0))

        # LOGGING
        if self.ideas:
            best = max(self.ideas.values(), key=lambda x: x.fitness)
            print(
                f"[Ω-v8] tick={self.tick} ideas={len(self.ideas)} "
                f"entropy={round(self.entropy,3)} best={best.intent} "
                f"fitness={round(best.fitness,3)}"
            )
        else:
            print(
                f"[Ω-v8] tick={self.tick} ideas=0 entropy={round(self.entropy,3)}"
            )


# =========================
# 🚀 BOOT
# =========================
if __name__ == "__main__":
    osys = MeshOSv8()

    print("[Ω-MESH OS v8] LEARNING + REWARD EVOLUTION CORE ONLINE")

    while True:
        osys.step()
        time.sleep(0.6)
