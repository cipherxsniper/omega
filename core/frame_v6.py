import time


def create_frame():
    return {
        "entities": {},
        "economy": {
            "inflation": 0.02,
            "transactions": []
        },
        "governance": {
            "votes": [],
            "consensus_threshold": 0.72
        },
        "laws": {},
        "memory": {
            "events": []
        },
        "events": [],
        "timestamp": time.time()
    }
