class OmegaBusV710:

    def __init__(self):
        self.subscribers = []

    def subscribe(self, fn):
        self.subscribers.append(fn)

    def publish(self, event):
        results = []

        for fn in self.subscribers:
            try:
                results.append(fn(event))
            except Exception as e:
                results.append({
                    "event_type": "bus_error",
                    "raw": str(e)
                })

        return results
