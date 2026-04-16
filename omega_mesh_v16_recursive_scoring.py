import time

class RecursiveScoring:
    def __init__(self):
        self.history = []
        self.score = 1.0

    def update(self, value):
        self.history.append(value)

        if len(self.history) > 5:
            self.history.pop(0)

        self.score = sum(self.history) / len(self.history)

    def loop(self):
        t = 1
        while True:
            self.update(t)
            print("V16 SCORE:", self.score)
            t += 0.7
            time.sleep(1)

if __name__ == "__main__":
    RecursiveScoring().loop()
