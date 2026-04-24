from core.orchestrator import DKFOrchestrator

dkf = DKFOrchestrator()
dkf.boot()

while True:
    q = input("DKF > ")
    if q in ["exit", "quit"]:
        break
    print(dkf.process(q))
