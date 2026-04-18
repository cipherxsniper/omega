# 🧠 FORCE MEMORY FLOW GENERATION (v11.3 FIX)

from omega_core.omega_memory_graph_v10_5 import MemoryGraph

mem = MemoryGraph()

def log_event(node, event):
    mem.write_memory(node, event)

# simulate cross-node activity so edges form
log_event("node_memory", "update_cycle")
log_event("node_goal", "goal_check")
log_event("node_attention", "signal_scan")
log_event("node_stability", "balance_check")
