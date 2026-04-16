import time
import random


class OmegaCivilizationV5:

    def __init__(self):
        self.frame = {
            "entities": {},
            "economy": {
                "currency": "OMEGA",
                "transactions": [],
                "price_table": {},
                "inflation_rate": 0.01,
                "compute_market": {}
            },
            "governance": {
                "council": [],
                "votes": [],
                "rules": {},
                "consensus_threshold": 0.66,
                "conflict_log": []
            },
            "memory": {
                "events": [],
                "index": {}
            },
            "events": [],
            "timestamp": time.time()
        }

    # ------------------------
    # ENTITY UPDATE LOOP
    # ------------------------
    def step_entities(self):
        for e in self.frame["entities"].values():

            e["compute_power"] += random.uniform(-0.2, 0.2)
            e["trust"] += random.uniform(-0.01, 0.01)
            e["wealth"] += random.uniform(-1, 1)

            if e["trust"] < 0.1:
                e["status"] = "failed"

    # ------------------------
    # ECONOMY STEP
    # ------------------------
    def step_economy(self):
        econ = self.frame["economy"]

        econ["inflation_rate"] += random.uniform(-0.001, 0.001)

        econ["transactions"].append({
            "t": time.time(),
            "volume": random.uniform(1, 10)
        })

    # ------------------------
    # GOVERNANCE STEP
    # ------------------------
    def step_governance(self):
        gov = self.frame["governance"]

        vote = random.choice([0, 1])

        gov["votes"].append({
            "t": time.time(),
            "vote": vote
        })

        if len(gov["votes"]) > 10:
            gov["votes"].pop(0)

    # ------------------------
    # MEMORY STEP
    # ------------------------
    def step_memory(self):
        mem = self.frame["memory"]

        mem["events"].append({
            "id": str(time.time()),
            "type": "cycle",
            "data": {},
            "weight": random.uniform(0, 1),
            "timestamp": time.time()
        })

    # ------------------------
    # FULL CIVILIZATION STEP
    # ------------------------
    def step(self):
        self.step_entities()
        self.step_economy()
        self.step_governance()
        self.step_memory()

        self.frame["timestamp"] = time.time()

        return self.frame
