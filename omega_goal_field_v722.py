class OmegaGoalFieldV722:

    def __init__(self):
        self.goal_vector = {}

    def update(self, memory_field, patterns):

        new_goals = {}

        for key, entry in memory_field.items():

            weight = entry.get("weight", 1.0)

            # convert memory strength → priority signal
            if weight > 2.0:
                new_goals[f"stabilize_{key}"] = 0.9

            elif weight > 1.2:
                new_goals[f"reinforce_{key}"] = 0.6

            else:
                new_goals[f"monitor_{key}"] = 0.3

        # merge with previous goals (temporal continuity)
        for k, v in new_goals.items():
            self.goal_vector[k] = max(self.goal_vector.get(k, 0.0), v)

        # decay old goals
        for k in list(self.goal_vector.keys()):
            self.goal_vector[k] *= 0.97

            if self.goal_vector[k] < 0.1:
                del self.goal_vector[k]

        return self.goal_vector

    def select_top_goals(self, limit=3):

        sorted_goals = sorted(
            self.goal_vector.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return dict(sorted_goals[:limit])
