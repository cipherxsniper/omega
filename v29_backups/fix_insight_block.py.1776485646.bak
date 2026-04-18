import re

file = "omega_process_supervisor_v3.py"

with open(file, "r") as f:
    content = f.read()

pattern = r"def generate_insight\\(.*?\\n\\s*return.*?\\n"
replacement = '''def generate_insight(state, script, line, insights):
    return f"""
[OMEGA AWARE OBSERVER v3]
Time: {datetime.utcnow().strftime('%H:%M:%S')}
Source Brain: {script}
Active Nodes: {len(state['active_nodes'])}
Total Events: {len(state['events'])}

Signal:
{line}

Cognitive Interpretation:
""" + "\\n".join([f"- {i}" for i in insights]) + "\\n"
'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file, "w") as f:
    f.write(new_content)

print("[FIXED] Insight block repaired")
