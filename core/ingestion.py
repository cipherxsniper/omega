import random
import time


class DataStreamBus:
    def __init__(self):
        self.latest = []

    def run(self):
        while True:
            self.latest = [
                random.random(),
                random.random(),
                random.random()
            ]
            time.sleep(1)

    def get_features(self):
        return self.latest
