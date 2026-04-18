file = "nano_omega_base_quantum_field_v12.py"

with open(file, "r") as f:
    lines = f.readlines()

out = []
inside_init = False
patched = False

for line in lines:
    out.append(line)

    # detect Particle constructor
    if "def __init__(self" in line:
        inside_init = True

    # inject after first self assignment block
    if inside_init and not patched and "self.y" in line:
        out.append("        self.memory = [0.0, 0.0, 0.0]\n")
        out.append("        self.cluster_id = -1\n")
        patched = True
        inside_init = False

with open(file, "w") as f:
    f.writelines(out)

print("✅ v12 memory + cluster patch applied safely")
