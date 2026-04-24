import uuid, random

class Particle:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.dna = "seed"
        self.node = "brain_01"
        self.energy = 1.0

    def propose(self):
        return {
            "type": random.choice(["CLONE","MUTATE","JUMP","WRITE"]),
            "target": f"brain_{random.randint(1,3):02d}"
        }

    def split(self):
        child = Particle()
        child.dna = self.dna + "-mut"
        return child
