import random
from worker_agent import WorkerAgent
from kernel_controller import KernelController

class SelfImprover:
    def __init__(self):
        self.kernel = KernelController()
        self.workers = [WorkerAgent(i) for i in range(3)]

    def fitness(self, patch):
        # Omega-style scoring (placeholder for your field simulation)
        base = patch["confidence"]

        complexity_penalty = len(patch["proposed"]) * 0.0001

        return base - complexity_penalty

    def run_cycle(self, file_path):
        for worker in self.workers:
            patch = worker.propose_patch(file_path)

            score = self.fitness(patch)
            patch["confidence"] = score

            if self.kernel.approve(patch):
                self.kernel.apply_patch(patch)
                print("✔ Applied patch:", patch["patch_id"])
            else:
                print("✖ Rejected patch:", patch["patch_id"])
