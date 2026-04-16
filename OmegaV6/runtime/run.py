import os
import time

from core.engine import OmegaEngineV6
from civilization.civilization_engine import CivilizationEngineV6
from governance.governance_engine import GovernanceEngineV6
from economy.economy_engine import EconomyEngineV6


def main():
    print("[Ω-V6] Booting unified civilization kernel...")

    engine = OmegaEngineV6(
        CivilizationEngineV6(),
        GovernanceEngineV6(),
        EconomyEngineV6()
    )

    while True:
        frame = engine.step()
        print(frame)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
