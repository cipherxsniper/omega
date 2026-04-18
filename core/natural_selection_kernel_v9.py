import time
import random
from datetime import datetime

from omega.core.global_memory import GLOBAL_MEMORY

class NaturalSelectionKernelV9:

    def __init__(self):
        self.population = GLOBAL_MEMORY.get("nodes", {})
        self.fitness_history = {}

    # -----------------------------
    # FITNESS EVALUATION
    # -----------------------------
    def evaluate_fitness(self, node_name, node_state):
        score = 0.5

        # reward stability
        score += node_state.get("stability", 0) * 0.3

        # reward usefulness
        score += node_state.get("utility", 0) * 0.3

        # penalize chaos
        score -= node_state.get("error_rate", 0) * 0.4

        return max(0.0, min(1.0, score))

    # -----------------------------
    # SELECTION PRESSURE
    # -----------------------------
    def selection_step(self):
        survivors = {}

        for node_name, state in self.population.items():
            fitness = self.evaluate_fitness(node_name, state)

            self.fitness_history[node_name] = fitness

            # survival threshold
            if fitness >= 0.55:
                survivors[node_name] = state
            else:
                state["status"] = "dormant"

        GLOBAL_MEMORY["nodes"] = survivors

        return {
            "survivors": len(survivors),
            "total": len(self.population)
        }

    # -----------------------------
    # MUTATION FIELD
    # -----------------------------
    def mutation_pressure(self):
        for node_name, state in self.population.items():

            drift = random.uniform(-0.05, 0.05)

            state["stability"] = max(0, min(1,
                state.get("stability", 0.5) + drift
            ))

    # -----------------------------
    # FULL EVOLUTION CYCLE
    # -----------------------------
    def run_cycle(self):
        self.mutation_pressure()
        result = self.selection_step()

        GLOBAL_MEMORY["last_evolution"] = {
            "time": datetime.utcnow().isoformat(),
            "result": result
        }

        return result
