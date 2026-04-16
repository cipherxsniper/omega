import random
from omega_bus import OmegaBus

class GoalNode:
    def __init__(self):
        self.bus = OmegaBus()

    def step(self, tick):
        data = self.bus.read()[-30:]

        goal_strength = random.uniform(0, 1)

        goal = "explore" if goal_strength > 0.5 else "stabilize"

        packet = {
            "type": "goal",
            "tick": tick,
            "goal": goal,
            "strength": goal_strength
        }

        self.bus.write(packet)
        print("[GOAL] tick", tick, goal)

if __name__ == "__main__":
    import time
    node = GoalNode()
    t = 0
    while True:
        node.step(t)
        t += 1
        time.sleep(1)
