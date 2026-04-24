from core.config import PRIMARY_MODEL, FALLBACK_MODEL, MAX_RETRIES
from obs.logger import log_event
from obs.metrics import Metrics
import time

class ModelRouter:
    def __init__(self, client):
        self.client = client
        self.metrics = Metrics()

    def generate(self, prompt, memory):

        memory.add("user", prompt)
        context = memory.build_context() or prompt

        models = [PRIMARY_MODEL, FALLBACK_MODEL]
        last_error = None

        for model in models:
            for attempt in range(MAX_RETRIES):

                self.metrics.start(model, prompt)

                try:
                    log_event("model_try", {
                        "model": model,
                        "attempt": attempt + 1
                    })

                    response = self.client.generate(
                        model,
                        context + "\nassistant:",
                        timeout=120
                    )

                    latency = self.metrics.end(model, response)

                    if response and response.strip():
                        memory.add("assistant", response)

                        log_event("model_success", {
                            "model": model,
                            "latency": latency
                        })

                        return response

                except Exception as e:
                    last_error = str(e)

                    log_event("model_error", {
                        "model": model,
                        "error": last_error
                    })

                    time.sleep(2)

        return f"[DKF FAILED] {last_error}"
