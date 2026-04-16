import threading
import time


class SwarmExecutionEngineV83:
    def __init__(self, node):
        self.node = node
        self.task_queue = []
        self.running = True

    # -------------------------
    # ADD TASK
    # -------------------------
    def submit_task(self, task):
        self.task_queue.append(task)

    # -------------------------
    # PROCESS TASKS
    # -------------------------
    def worker_loop(self):
        while self.running:
            if self.task_queue:
                task = self.task_queue.pop(0)

                try:
                    result = self.execute(task.payload)
                    task.complete(result)

                    print(f"[NODE {self.node.port}] TASK DONE:", task.task_id)

                except Exception as e:
                    print("[TASK ERROR]", e)

            time.sleep(0.5)

    # -------------------------
    # SIMPLE EXECUTION LOGIC
    # -------------------------
    def execute(self, payload):
        # simulate cognitive computation
        if isinstance(payload, dict):
            return {
                "processed_keys": list(payload.keys()),
                "size": len(str(payload)),
                "node": self.node.node_id
            }

        if isinstance(payload, str):
            return {
                "length": len(payload),
                "words": len(payload.split()),
                "node": self.node.node_id
            }

        return {"error": "unsupported payload type"}

    # -------------------------
    # START ENGINE
    # -------------------------
    def start(self):
        threading.Thread(target=self.worker_loop, daemon=True).start()
