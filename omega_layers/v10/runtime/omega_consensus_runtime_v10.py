import time
from omega_layers.v10.core.omega_consensus_engine_v10 import ConsensusField, Node, classify
field = ConsensusField()
nodes = [Node('swarm_bus', 'SERVICE'), Node('memory', 'TASK'), Node('assistant', 'SERVICE'), Node('emitter', 'TASK')]
for n in nodes:
    field.add_node(n)
field.link('swarm_bus', 'memory')
field.link('memory', 'assistant')
field.link('emitter', 'swarm_bus')
print('\n🧠 OMEGA CONSENSUS v10 RUNTIME\n')
while True:
    field.propagate_trust()
    state = field.compute_consensus()
    system_state = classify(state)
    print('\n──────── CONSENSUS CYCLE ────────')
    for k, v in state.items():
        print(f'{k:10} → {round(v, 4)}')
    print('\nSYSTEM STATE:', system_state)
    if system_state == 'CONSENSUS_COLLAPSE':
        print('🚨 SYSTEM COLLAPSE DETECTED → entering stabilization mode')
    time.sleep(5)