import random
from worker_agent import WorkerAgent
from kernel_controller import KernelController

class SwarmEngine:
    def __init__(self):
        self.kernel = KernelController()
        self.populations = {
            "alpha": [WorkerAgent(f"A{i}") for i in range(5)],
            "beta": [WorkerAgent(f"B{i}") for i in range(5)],
        }

    def compete(self, file_path):
        results = []

        for group, workers in self.populations.items():
            for w in workers:
                patch = w.propose_patch(file_path)
                score = self.kernel.score_patch(patch)

                results.append((group, score, patch))

        # sort best evolutionary pressure wins
        results.sort(key=lambda x: x[1], reverse=True)

        best_group, best_score, best_patch = results[0]

        if self.kernel.approve(best_patch):
            self.kernel.apply_patch(best_patch)
            print(f"🏆 Winner: {best_group} score={best_score}")
