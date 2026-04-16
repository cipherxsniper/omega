import time

class OmegaEngineV6:
    def __init__(self, civilization_engine, governance_engine, economy_engine):
        self.civilization = civilization_engine
        self.governance = governance_engine
        self.economy = economy_engine

        self.frame = {
            "entities": {},
            "economy": {},
            "governance": {},
            "memory": {"events": []},
            "laws": {},
            "timestamp": time.time()
        }

    def step(self):
        # ALWAYS pass frame correctly
        self.frame = self.civilization.step(self.frame)
        self.frame = self.governance.step(self.frame)
        self.frame = self.economy.step(self.frame)
        return self.frame
