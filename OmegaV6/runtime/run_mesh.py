import time
from core.engine import OmegaEngineV6
from civilization.civilization_engine import CivilizationEngineV6
from governance.governance_engine import GovernanceEngineV6
from economy.economy_engine import EconomyEngineV6

from nodes.node import OmegaNodeV6
from mesh.mesh_orchestrator import MeshOrchestrator


def main():

    print("[Ω-V6.1] Mesh Civilization Booting...")

    base_engine = OmegaEngineV6(
        CivilizationEngineV6(),
        GovernanceEngineV6(),
        EconomyEngineV6()
    )

    # create distributed nodes
    nodes = [
        OmegaNodeV6("alpha", base_engine),
        OmegaNodeV6("beta", base_engine),
        OmegaNodeV6("gamma", base_engine)
    ]

    mesh = MeshOrchestrator()

    while True:

        frames = []

        for n in nodes:
            frames.append(n.step())

        global_frame = mesh.aggregate()

        if global_frame:
            print({
                "mesh_consensus": global_frame["governance"].get("mesh_consensus"),
                "economy": global_frame["economy"],
                "last_events": global_frame["memory"]["events"][-3:]
            })

        time.sleep(0.3)


if __name__ == "__main__":
    main()
