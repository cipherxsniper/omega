from omega_supervisor_v9_3 import Supervisor

print("[Ω KERNEL v9.3 BOOTING]")

sup = Supervisor()

sup.register("bus", "omega_neural_bus_v9_3.py")
sup.register("mesh", "omega_cognitive_mesh_v9_3.py")
sup.register("balancer", "omega_swarm_balancer_v9_3.py")
sup.register("runtime", "omega_node_runtime_v9_3.py")
sup.register("chat", "omega_chat_assistant_v9_3.py")

sup.start_all()

while True:
    sup.monitor()
