import time
import random
import math
import uuid
import copy


# =========================
# 🧩 IDEA OBJECT
# =========================
class Idea:

    def __init__(self, x, y):

        self.id = str(uuid.uuid4())[:8]
        self.x = x
        self.y = y

        self.strength = random.uniform(0.3, 1.0)

    def reinforce(self, value):
        self.strength += value
        self.strength = min(self.strength, 5.0)


# =========================
# 🧠 BRAIN
# =========================
class Brain:

    def __init__(self, brain_id):

        self.id = brain_id
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)

        self.vx = 0
        self.vy = 0

    def move(self):

        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.9
        self.vy *= 0.9


# =========================
# 🧠 SELF-AWARE SYSTEM
# =========================
class OmegaSelfAware:

    def __init__(self):

        self.brains = [Brain(f"brain_{i}") for i in range(5)]
        self.ideas = []

        self.tick = 0

        # memory of past states
        self.history = []

        # adaptive parameters
        self.idea_spawn_rate = 0.3
        self.stability_bias = 0.0

    # -------------------------
    # DISTANCE
    # -------------------------
    def dist(self, a, b):
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2) + 0.01

    # -------------------------
    # IDEA CREATION
    # -------------------------
    def spawn_idea(self):

        if random.random() < self.idea_spawn_rate:

            b = random.choice(self.brains)
            self.ideas.append(Idea(b.x, b.y))

    # -------------------------
    # IDEA REINFORCEMENT
    # -------------------------
    def reinforce(self):

        for idea in self.ideas:

            for b in self.brains:

                if self.dist(idea, b) < 0.5:
                    idea.reinforce(0.05 + self.stability_bias)

    # -------------------------
    # BELIEF SYSTEM
    # -------------------------
    def belief_strength(self):

        if not self.ideas:
            return 0

        return sum(i.strength for i in self.ideas) / len(self.ideas)

    # -------------------------
    # SELF OBSERVATION
    # -------------------------
    def observe(self):

        state = {
            "tick": self.tick,
            "ideas": len(self.ideas),
            "belief_strength": self.belief_strength()
        }

        self.history.append(copy.deepcopy(state))

        return state

    # -------------------------
    # SELF COMPARISON
    # -------------------------
    def compare(self):

        if len(self.history) < 2:
            return None

        prev = self.history[-2]
        curr = self.history[-1]

        delta = {
            "idea_growth": curr["ideas"] - prev["ideas"],
            "belief_change": curr["belief_strength"] - prev["belief_strength"]
        }

        return delta

    # -------------------------
    # DECISION ENGINE
    # -------------------------
    def decide(self, delta):

        if not delta:
            return "observe"

        if delta["idea_growth"] < 1:
            self.idea_spawn_rate += 0.05
            return "increase_creation"

        if delta["belief_change"] < 0:
            self.stability_bias += 0.02
            return "stabilize"

        return "maintain"

    # -------------------------
    # META THOUGHT
    # -------------------------
    def meta_thought(self, state, delta, decision):

        return {
            "type": "meta_thought",
            "tick": self.tick,
            "observation": state,
            "delta": delta,
            "decision": decision
        }

    # -------------------------
    # STEP
    # -------------------------
    def step(self):

        self.tick += 1

        self.spawn_idea()
        self.reinforce()

        for b in self.brains:
            b.move()

        state = self.observe()
        delta = self.compare()
        decision = self.decide(delta)

        meta = self.meta_thought(state, delta, decision)

        return meta


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":

    system = OmegaSelfAware()

    print("[Ω-v19] SELF-AWARE COGNITIVE LOOP ONLINE")

    while True:

        meta = system.step()

        if system.tick % 3 == 0:
            print("[Ω-v19 META]", meta)

        time.sleep(0.5)
