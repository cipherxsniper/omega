def resolve_stack():
    swarm_bus = resolve_latest(
        [
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ],
        grep=["v14", "v15", "v16", "v17", "v13"]
    )

    if not swarm_bus:
        swarm_bus = resolve_latest([
            "*swarm_bus*.py",
            "*event_bus*.py",
            "*omega_bus*.py",
            "*bus*.py"
        ])

    memory = resolve_latest([
        "omega_crdt_memory_v*.py",
        "omega_memory*.py"
    ])

    assistant = resolve_latest([
        "omega_assistant*.py",
        "omega_*assistant*.py"
    ])

    emitter = str(CORE_DIR / "test_swarm_emitter.py")

    return {
        "swarm_bus": swarm_bus,
        "memory": memory,
        "assistant": assistant,
        "emitter": emitter
    }
