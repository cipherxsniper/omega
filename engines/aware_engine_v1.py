# engines/aware_engine_v1.py

class AwareEngine:
    def __init__(self):
        self.observations = []

    def observe(self, environment, system_state):
        obs = {
            "environment": environment,
            "system": system_state
        }
        self.observations.append(obs)
        return obs

    def self_reflect(self):
        return {
            "total_observations": len(self.observations),
            "last_state": self.observations[-1] if self.observations else None
        }
