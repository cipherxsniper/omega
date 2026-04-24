import json

class LongTermMemory:
    def save(self, data):
        open("memory.json", "w").write(json.dumps(data))

    def load(self):
        try:
            return json.loads(open("memory.json").read())
        except:
            return {}
