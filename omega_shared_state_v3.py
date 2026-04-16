from multiprocessing import Manager

def create_shared_state():
    manager = Manager()

    return manager.dict({
        "tick": 0,
        "nodes": manager.dict(),
        "ideas": manager.dict(),
        "rewards": manager.dict(),
        "fitness": manager.dict()
    })
