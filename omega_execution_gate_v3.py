class ExecutionGateV3:

    def __init__(self, threshold=0.85):
        self.threshold = threshold

    def approve(self, repair):
        return repair.get("confidence", 0) >= self.threshold


if __name__ == "__main__":
    gate = ExecutionGateV3()

    test_repair = {"confidence": 0.82}

    print("APPROVED:", gate.approve(test_repair))
