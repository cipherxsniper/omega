MAX_IDEAS = 200

# 🧹 pruning step
to_delete = []

for k, v in self.state["ideas"].items():
    if v.get("strength", 0) < 0.3:
        to_delete.append(k)

for k in to_delete:
    del self.state["ideas"][k]

# 🧠 enforce max capacity
if len(self.state["ideas"]) > MAX_IDEAS:
    weakest = sorted(
        self.state["ideas"].items(),
        key=lambda x: x[1].get("strength", 0)
    )

    for k, _ in weakest[:len(self.state["ideas"]) - MAX_IDEAS]:
        del self.state["ideas"][k]
