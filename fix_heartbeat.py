file = "omega_process_supervisor_v3.py"

with open(file, "r") as f:
    lines = f.readlines()

new_lines = []
inside = False

for line in lines:
    if line.strip().startswith("def heartbeat"):
        inside = True
        new_lines.append("def heartbeat():\n")
        new_lines.append("    while True:\n")
        new_lines.append("        print(\"[OMEGA HEARTBEAT] \" + datetime.utcnow().isoformat())\n")
        new_lines.append("        time.sleep(10)\n")
        continue

    if inside:
        if line.startswith("def ") and not line.strip().startswith("def heartbeat"):
            inside = False
            new_lines.append(line)
        continue

    new_lines.append(line)

with open(file, "w") as f:
    f.writelines(new_lines)

print("[FIXED] Heartbeat repaired")
