# ============================================================
# OMEGA IDENTITY ENGINE v5
# SELF MODEL + EPISODIC MEMORY + REFLECTION SYSTEM
# ============================================================

import time
import uuid


# ============================================================
# 🧠 IDENTITY CORE
# ============================================================

class OmegaIdentityCore:
    def __init__(self, state):
        self.state = state

        self.identity = {
            "name": "OMEGA",
            "version": "5.0",
            "stability": 1.0,
            "decision_style": "balanced",
            "confidence_bias": 0.5,
            "evolution_stage": 1
        }

    def update_trait(self, key, value):
        self.identity[key] = value

        self.state.add_knowledge({
            "type": "identity_update",
            "key": key,
            "value": value
        })

    def get_identity(self):
        return self.identity


# ============================================================
# 📖 EPISODIC MEMORY SYSTEM
# ============================================================

class OmegaEpisodicMemory:
    def __init__(self, state):
        self.state = state
        self.episodes = []

    def record_episode(self, event, outcome, context=None):
        episode = {
            "id": str(uuid.uuid4()),
            "event": event,
            "outcome": outcome,
            "context": context,
            "timestamp": time.time()
        }

        self.episodes.append(episode)

        self.state.add_knowledge({
            "type": "episode",
            "data": episode
        })

    def get_recent(self, limit=10):
        return self.episodes[-limit:]


# ============================================================
# 🧠 SELF-REFLECTION ENGINE
# ============================================================

class OmegaSelfReflection:
    def __init__(self, identity, memory, learning_engine):
        self.identity = identity
        self.memory = memory
        self.learning = learning_engine

    def evaluate_performance(self):
        episodes = self.memory.get_recent(20)

        if not episodes:
            return {"status": "no_data"}

        success = sum(1 for e in episodes if e["outcome"] == "success")
        failure = sum(1 for e in episodes if e["outcome"] == "failure")

        score = success / (failure + 1)

        return {
            "success": success,
            "failure": failure,
            "performance_score": score
        }

    def reflect(self):
        report = self.evaluate_performance()

        if report.get("performance_score", 1) < 0.5:
            self.identity.update_trait("decision_style", "defensive")
        elif report.get("performance_score", 1) > 1.5:
            self.identity.update_trait("decision_style", "aggressive")
        else:
            self.identity.update_trait("decision_style", "balanced")

        self.identity.update_trait(
            "stability",
            min(max(report.get("performance_score", 1), 0.1), 2.0)
        )

        self.learning.record_success(
            "self_reflection",
            report.get("performance_score", 1)
        )

        return report
