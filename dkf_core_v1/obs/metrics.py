import time
from obs.logger import log_event

class Metrics:
    def __init__(self):
        self.start_time = None

    def start(self, model, prompt):
        self.start_time = time.time()
        log_event("request_start", {
            "model": model,
            "prompt_length": len(prompt)
        })

    def end(self, model, response):
        latency = time.time() - self.start_time

        log_event("request_end", {
            "model": model,
            "latency": latency,
            "response_length": len(response) if response else 0
        })

        return latency
