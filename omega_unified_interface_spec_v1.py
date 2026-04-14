# ============================================================
# OMEGA UNIFIED INTERFACE SPEC v1
# AMD-STABLE / RUNTIME ENFORCED ARCHITECTURE LAYER
# ============================================================

import time
from abc import ABC, abstractmethod


# ============================================================
# 🧠 VALIDATION CORE (PREVENTS EMPTY / CRASH STATES)
# ============================================================

class OmegaValidationError(Exception):
    pass


def validate_non_empty(data, name="data"):
    if data is None or (hasattr(data, "__len__") and len(data) == 0):
        raise OmegaValidationError(f"[OMEGA VALIDATION ERROR] {name} is empty")


def require_keys(obj, keys, name="object"):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise OmegaValidationError(
            f"[OMEGA VALIDATION ERROR] {name} missing keys: {missing}"
        )


# ============================================================
# 🧠 SWARM STATE CONTRACT
# ============================================================

class OmegaSwarmState:
    def __init__(self):
        self.state = {
            "agents": {},
            "strongest": None,
            "cycle": 0,
            "drift": 0.0
        }

    def update(self, agent_scores: dict):
        validate_non_empty(agent_scores, "agent_scores")

        self.state["agents"] = agent_scores
        self.state["strongest"] = max(agent_scores, key=agent_scores.get)
        self.state["cycle"] += 1

        avg = sum(agent_scores.values()) / len(agent_scores)
        self.state["drift"] = abs(max(agent_scores.values()) - avg)

        return self.state


# ============================================================
# 🧠 MEMORY INTERFACE (MANDATORY)
# ============================================================

class OmegaMemoryInterface(ABC):

    @abstractmethod
    def store(self, record: dict):
        validate_non_empty(record, "memory_record")

    @abstractmethod
    def recall(self, query: dict):
        validate_non_empty(query, "memory_query")

    @abstractmethod
    def consolidate(self):
        pass


# ============================================================
# 🧠 LEARNING INTERFACE (MANDATORY FIX FOR YOUR ERRORS)
# ============================================================

class OmegaLearningInterface(ABC):

    @abstractmethod
    def learn(self, data: dict):
        validate_non_empty(data, "learning_data")

    @abstractmethod
    def reinforce(self, reward: float):
        pass

    @abstractmethod
    def predict(self, context: dict):
        validate_non_empty(context, "context")


# ============================================================
# 🧠 BRAIN INPUT / OUTPUT CONTRACTS
# ============================================================

class OmegaBrainInterface:

    def __init__(self, brain_id: str):
        self.brain_id = brain_id

    def input_contract(self, payload: dict):
        require_keys(payload, ["memory", "swarm_state", "context", "tick"], "brain_input")
        return payload

    def output_contract(self, output: dict, score: float):
        return {
            "id": self.brain_id,
            "score": float(score),
            "output": output,
            "confidence": min(max(score / 10.0, 0.0), 1.0),
            "timestamp": time.time()
        }


# ============================================================
# 🧠 ORCHESTRATOR INTERFACE
# ============================================================

class OmegaOrchestratorInterface(ABC):

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def load_brains(self):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass


# ============================================================
# 🧠 COMMUNICATION BUS (FIXES SWARM ISOLATION)
# ============================================================

class OmegaBus:
    def __init__(self):
        self.subscribers = {}
        self.messages = []

    def subscribe(self, brain_id: str):
        if brain_id not in self.subscribers:
            self.subscribers[brain_id] = []

    def publish(self, sender: str, message: dict):
        validate_non_empty(message, "bus_message")

        self.messages.append({
            "sender": sender,
            "message": message,
            "timestamp": time.time()
        })

    def broadcast(self, message: dict):
        validate_non_empty(message, "broadcast_message")

        for brain_id in self.subscribers:
            self.subscribers[brain_id].append(message)


# ============================================================
# 🧠 REWARD SHAPING ENGINE (STABILIZES SWARM DRIFT)
# ============================================================

class OmegaRewardShaper:

    def compute(self, swarm_state: dict):
        validate_non_empty(swarm_state, "swarm_state")

        strongest = swarm_state.get("strongest")
        agents = swarm_state.get("agents", {})

        rewards = {}

        for agent, score in agents.items():
            if agent == strongest:
                rewards[agent] = score * 1.1
            else:
                rewards[agent] = score * 0.95

        return rewards


# ============================================================
# 🧠 RECURSIVE FEEDBACK CORE
# ============================================================

class OmegaRecursiveFeedback:

    def __init__(self):
        self.history = []

    def update(self, swarm_state: dict):
        validate_non_empty(swarm_state, "swarm_state")

        self.history.append(swarm_state)

        if len(self.history) > 50:
            self.history.pop(0)

        # drift correction
        avg_strength = sum(
            max(s["agents"].values()) for s in self.history
        ) / len(self.history)

        return {
            "history_length": len(self.history),
            "avg_strength": avg_strength
        }
