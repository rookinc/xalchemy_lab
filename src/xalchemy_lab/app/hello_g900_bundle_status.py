from __future__ import annotations

import subprocess
import sys


MODULES = [
    "xalchemy_lab.app.hello_g900_weighted_prism",
    "xalchemy_lab.app.hello_g900_weight_table",
    "xalchemy_lab.app.hello_g900_descent_table",
    "xalchemy_lab.app.hello_g900_pushforward_probe",
    "xalchemy_lab.app.hello_g900_centered_prism_lemma",
    "xalchemy_lab.app.hello_g900_centered_quotient",
    "xalchemy_lab.app.hello_g900_offset_law_probe",
    "xalchemy_lab.app.hello_g900_extension_parameter_probe",
]


def run_module(module: str) -> None:
    print("\n" + "#" * 72)
    print(f"# RUNNING {module}")
    print("#" * 72)
    subprocess.run([sys.executable, "-m", module], check=True)


def main() -> None:
    print("\nG900 BUNDLE STATUS")
    print("==================")
    for module in MODULES:
        run_module(module)
    print("\nG900 bundle status: PASS")


if __name__ == "__main__":
    main()
