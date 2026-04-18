from sentence_engine import build_sentence
from belief_memory_core import load_memory, update_belief, save_memory
from multi_agent_reasoner import agents_think

def omega_process(message):
    mem = load_memory()

    concepts = message.lower().split()

    for c in concepts:
        update_belief(mem, c)

    agent_result = agents_think(message)

    sentence = build_sentence(concepts)

    mem["history"].append(message)
    save_memory(mem)

    return f"""{sentence}

🧠 Multi-Agent Decision:
Winner: {agent_result['winner']}
Insight: {agent_result['analysis']}
Votes: {agent_result['votes']}

🧠 Memory Drift:
Dominant concept: {max(mem['beliefs'], key=mem['beliefs'].get)}
"""
