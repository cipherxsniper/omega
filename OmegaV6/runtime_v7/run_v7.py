import time

from core.engine import OmegaEngineV6
from civilization.civilization_engine import CivilizationEngineV6
from governance.governance_engine import GovernanceEngineV6
from economy.economy_engine import EconomyEngineV6

from mesh_v7.node_v7 import OmegaNodeV7
from mesh_v7.orchestrator import MeshOrchestratorV7
from sensors.environment_sensor import EnvironmentSensor


def main():

    print("[Ω-V7] Cognitive Internet Mesh ONLINE")

    engine = OmegaEngineV6(
        CivilizationEngineV6(),
        GovernanceEngineV6(),
        EconomyEngineV6()
    )

    sensor = EnvironmentSensor()
    mesh = MeshOrchestratorV7()

    nodes = [
        OmegaNodeV7("alpha", engine, 6001),
        OmegaNodeV7("beta", engine, 6002),
        OmegaNodeV7("gamma", engine, 6003)
    ]

    for n in nodes:
        n.start()

    while True:

        frames = []
        env = sensor.read()

        for n in nodes:
            f = n.step()
            f["environment"] = env
            frames.append(f)

        merged = mesh.merge(frames)

        print({
            "internet_consensus": merged["governance"]["internet_consensus"],
            "mesh_size": merged["mesh_size"],
            "environment": env,
            "economy": merged.get("economy", {})
        })

        time.sleep(0.5)


if __name__ == "__main__":
    main()
