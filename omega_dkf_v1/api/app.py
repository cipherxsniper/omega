from core.orchestrator import DKFOrchestrator

dkf = DKFOrchestrator()
dkf.boot()

def ask(q):
    return dkf.process(q)
