import time
from collections import defaultdict

# ================================
# NODE MODEL
# ================================
class Node:
    def __init__(self, id, type="TASK"):
        self.id = id
        self.type = type
        self.runtime_health = 0.5
        self.semantic_health = 0.5
        self.causal_health = 0.5
        self.trust = 1.0
        self.last_seen = time.time()

    def score(self):
        return (
            self.runtime_health * 0.4 +
            self.semantic_health * 0.3 +
            self.causal_health * 0.3
        ) * self.trust


# ================================
# CONSENSUS FIELD
# ================================
class ConsensusField:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(list)
        self.belief_state = {}
        self.conflicts = {}

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def link(self, a, b):
        self.edges[a].append(b)

    def propagate_trust(self):
        for parent, children in self.edges.items():
            for c in children:
                if parent in self.nodes and c in self.nodes:
                    self.nodes[c].trust += self.nodes[parent].trust * 0.05

    def compute_consensus(self):
        results = {}

        for nid, node in self.nodes.items():
            base = node.score()

            neighbors = self.edges.get(nid, [])
            if neighbors:
                neighbor_avg = sum(
                    self.nodes[n].runtime_health for n in neighbors if n in self.nodes
                ) / max(len(neighbors), 1)
            else:
                neighbor_avg = base

            final = (base * 0.7) + (neighbor_avg * 0.3)
            results[nid] = final

        return results


# ================================
# SYSTEM STATE CLASSIFIER
# ================================
def classify(state):
    avg = sum(state.values()) / max(len(state), 1)

    if avg > 0.75:
        return "STABLE_CONSENSUS"
    elif avg > 0.5:
        return "DEGRADED_CONSENSUS"
    elif avg > 0.25:
        return "FRAGMENTED_TRUTH"
    else:
        return "CONSENSUS_COLLAPSE"
