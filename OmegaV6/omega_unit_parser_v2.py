import os

class OmegaUnitParserV2:
    def parse(self, file):
        """
        VERY SIMPLE UNIT FORMAT:

        [Unit]
        Name=omega_kernel
        Exec=omega_kernel_v15.py
        After=omega_identity_kernel_v25.py
        Requires=omega_meta_brain_v10.py
        """
        unit = {
            "name": None,
            "exec": None,
            "after": [],
            "requires": []
        }

        if not os.path.exists(file):
            return None

        with open(file, "r") as f:
            for line in f:
                line = line.strip()

                if line.startswith("Name="):
                    unit["name"] = line.split("=")[1]

                elif line.startswith("Exec="):
                    unit["exec"] = line.split("=")[1]

                elif line.startswith("After="):
                    unit["after"] = line.split("=")[1].split(",")

                elif line.startswith("Requires="):
                    unit["requires"] = line.split("=")[1].split(",")

        return unit
