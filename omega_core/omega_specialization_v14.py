# 🧠 Omega v14 Emergent Specialization Engine

import random
import copy


class SpecializationEngine:

    def __init__(self):

        # initial population of "thinking agents"
        self.agents = {
            "agent_A": {"skill": 0.5, "role": "generalist"},
            "agent_B": {"skill": 0.5, "role": "generalist"},
            "agent_C": {"skill": 0.5, "role": "generalist"}
        }

        self.generation = 0

    # --------------------------------------
    # simulate environment challenge
    # --------------------------------------
    def environment(self):

        return {
            "attention": random.random(),
            "goal": random.random(),
            "memory": random.random(),
            "stability": random.random()
        }

    # --------------------------------------
    # evaluate agent performance
    # --------------------------------------
    def evaluate(self, agent, state):

        skill = self.agents[agent]["skill"]

        score = (
            state["goal"] * skill +
            state["attention"] * (1 - skill) +
            random.uniform(-0.02, 0.02)
        )

        return max(0.0, min(1.0, score))

    # --------------------------------------
    # specialization mutation
    # --------------------------------------
    def specialize(self, agent):

        role = self.agents[agent]["role"]

        # create specialized copy
        child = f"{agent}_spec_{self.generation}"

        self.agents[child] = copy.deepcopy(self.agents[agent])

        # drift specialization
        if role == "generalist":

            self.agents[child]["role"] = random.choice([
                "attention_specialist",
                "goal_specialist",
                "memory_specialist"
            ])

        else:

            # refine specialization further
            self.agents[child]["skill"] += random.uniform(-0.05, 0.1)

        self.agents[child]["skill"] = max(0.01, min(1.0, self.agents[child]["skill"]))

    # --------------------------------------
    # pruning weak agents
    # --------------------------------------
    def prune(self):

        to_remove = []

        for k, v in self.agents.items():

            if v["skill"] < 0.25 and "spec" in k:
                to_remove.append(k)

        for k in to_remove:
            del self.agents[k]

    # --------------------------------------
    # evolution cycle
    # --------------------------------------
    def step(self):

        state = self.environment()

        scores = {}

        for agent in list(self.agents.keys()):

            score = self.evaluate(agent, state)

            scores[agent] = score

            # reinforcement learning update
            self.agents[agent]["skill"] += (score - 0.5) * 0.05

            self.agents[agent]["skill"] = max(0.01, min(1.0, self.agents[agent]["skill"]))

        # find best performer
        best = max(scores, key=scores.get)

        # SPECIALIZATION RULE:
        # best agent replicates (emergent branching)
        if scores[best] > 0.7:
            self.specialize(best)

        # prune weak agents
        self.prune()

        self.generation += 1

        return state, scores, best, self.agents
