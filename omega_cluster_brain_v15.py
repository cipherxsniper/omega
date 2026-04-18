import random
import math
import copy

# 🧠 Omega v15 Cluster Brain (Neuroevolution Core)

class ClusterBrain:

    def __init__(self, name):
        self.name = name

        # core traits
        self.weight = random.uniform(0.3, 0.7)
        self.specialization = random.uniform(0.2, 0.8)
        self.energy = 0.5

        # graph connections (weighted synapses)
        self.connections = {}

        # evolutionary memory
        self.fitness_history = []
        self.age = 0

    # -------------------------
    # CONNECTIVITY EVOLUTION
    # -------------------------
    def connect(self, other):
        if other.name not in self.connections:
            self.connections[other.name] = random.uniform(0.1, 0.5)

    def mutate_connections(self):
        # add/remove/adjust synapses
        for k in list(self.connections.keys()):
            self.connections[k] += random.uniform(-0.05, 0.05)
            self.connections[k] = max(0.01, min(1.0, self.connections[k]))

            # prune weak connections
            if self.connections[k] < 0.08:
                del self.connections[k]

    # -------------------------
    # INFERENCE (THINKING)
    # -------------------------
    def influence(self, global_signal, network_signal=0.0):

        connection_sum = sum(self.connections.values())

        return (
            self.weight * 0.4 +
            self.specialization * 0.25 +
            connection_sum * 0.2 +
            global_signal * 0.1 +
            network_signal * 0.05
        )

    # -------------------------
    # LEARNING UPDATE
    # -------------------------
    def update(self, feedback):

        self.age += 1

        # energy drift
        self.energy += feedback * 0.08

        # adaptive mutation pressure
        mutation_rate = 0.02 + (1 - self.energy) * 0.05

        self.weight += random.uniform(-mutation_rate, mutation_rate) * feedback
        self.specialization += random.uniform(-mutation_rate, mutation_rate) * feedback

        # clamp stability
        self.weight = max(0.01, min(1.0, self.weight))
        self.specialization = max(0.01, min(1.0, self.specialization))

        # connection evolution
        self.mutate_connections()

        # record fitness
        self.fitness_history.append(feedback)

        if len(self.fitness_history) > 50:
            self.fitness_history.pop(0)

    # -------------------------
    # FITNESS SCORE
    # -------------------------
    def fitness(self):
        if not self.fitness_history:
            return 0.5
        return sum(self.fitness_history) / len(self.fitness_history)


# =========================
# 🧠 CLUSTER EVOLUTION ENGINE
# =========================

class ClusterEvolutionSystem:

    def __init__(self):
        self.brains = []
        self.generation = 0

    def add_brain(self, brain):
        self.brains.append(brain)

    def global_signal(self):
        if not self.brains:
            return 0.5
        return sum(b.energy for b in self.brains) / len(self.brains)

    # -------------------------
    # SELECTION PRESSURE
    # -------------------------
    def select_survivors(self):
        self.brains.sort(key=lambda b: b.fitness(), reverse=True)

        # top 50% survive
        cutoff = max(1, len(self.brains) // 2)
        self.brains = self.brains[:cutoff]

    # -------------------------
    # REPRODUCTION (NEUROEVOLUTION)
    # -------------------------
    def reproduce(self):
        offspring = []

        for brain in self.brains:
            child = copy.deepcopy(brain)
            child.name = brain.name + "_mut"

            # mutation burst
            child.weight += random.uniform(-0.1, 0.1)
            child.specialization += random.uniform(-0.1, 0.1)

            # mutate connections harder in offspring
            for k in child.connections:
                child.connections[k] += random.uniform(-0.1, 0.1)

            offspring.append(child)

        self.brains.extend(offspring)

    # -------------------------
    # FULL EVOLUTION STEP
    # -------------------------
    def step(self, external_signal=0.5):

        self.generation += 1
        global_sig = self.global_signal()

        results = {}

        for brain in self.brains:
            signal = brain.influence(external_signal, global_sig)
            brain.update(signal - 0.5)

            results[brain.name] = {
                "fitness": brain.fitness(),
                "energy": brain.energy,
                "connections": len(brain.connections)
            }

        # evolution cycle
        self.select_survivors()
        self.reproduce()

        return results


# =========================
# 🧪 SIMPLE BOOTSTRAP
# =========================

if __name__ == "__main__":

    system = ClusterEvolutionSystem()

    # initial population
    for i in range(6):
        system.add_brain(ClusterBrain(f"brain_{i}"))

    for step in range(10):
        print("\nGENERATION:", system.generation)
        output = system.step(external_signal=random.uniform(0.3, 0.8))
        print(output)
