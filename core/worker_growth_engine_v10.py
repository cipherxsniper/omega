import threading
import time
from omega.core.global_memory import GLOBAL_MEMORY

class WorkerGrowthEngineV10:
    """
    Spawns new cognitive workers based on load + entropy pressure.
    """

    def __init__(self):
        self.workers = []

    def spawn_worker(self, name, target_fn):
        t = threading.Thread(target=target_fn, daemon=True)
        t.start()

        self.workers.append({
            "name": name,
            "thread": t
        })

        return t

    def auto_expand(self):
        """
        If system load increases → spawn new cognitive workers.
        """

        load = len(GLOBAL_MEMORY.get("packets", []))

        if load % 10 == 0 and load > 0:
            self.spawn_worker(
                f"worker_{len(self.workers)}",
                lambda: print("🧠 cognitive worker active")
            )
