import os

NODE_TEMPLATE = """
# Omega Node: {name}

def run(input_data):
    return "🧠 Node {name} processed: " + str(input_data)
"""

def spawn_node(name, directory="nodes"):
    os.makedirs(directory, exist_ok=True)

    path = f"{directory}/{name}.py"

    with open(path, "w") as f:
        f.write(NODE_TEMPLATE.format(name=name))

    return f"🧠 Node spawned: {path}"
