from __future__ import annotations

import math


def main() -> None:
    I = 145
    d = 5
    L = 10

    phi = (1 + math.sqrt(5)) / 2

    quantities = [
        ("d / I", d / I),
        ("L / I", L / I),
        ("d / L", d / L),
        ("I / d", I / d),
        ("I / L", I / L),
        ("L / d", L / d),
    ]

    phi_forms = [
        ("phi", phi),
        ("1/phi", 1 / phi),
        ("phi-1", phi - 1),
        ("2-phi", 2 - phi),
        ("1/phi^2", 1 / (phi * phi)),
        ("phi^2", phi * phi),
        ("phi/2", phi / 2),
        ("1/(2phi)", 1 / (2 * phi)),
    ]

    print("\nG900 PHI EXTENSION PROBE")
    print("========================")
    print(f"phi               : {phi:.15f}")

    print("\nG900 RATIOS")
    print("===========")
    for name, value in quantities:
        print(f"{name:12} = {value:.15f}")

    print("\nPHI FORMS")
    print("=========")
    for name, value in phi_forms:
        print(f"{name:12} = {value:.15f}")

    print("\nDIFFERENCES")
    print("===========")
    for qname, qvalue in quantities:
        best = min(phi_forms, key=lambda item: abs(qvalue - item[1]))
        bname, bvalue = best
        diff = abs(qvalue - bvalue)
        print(f"{qname:12} best match {bname:8} diff={diff:.15f}")

    print("\nINTERPRETATION")
    print("==============")
    print("A clean match would support phi as a direct extension normalizer.")
    print("A miss does not kill the hypothesis; phi may still act upstream in the 5-side geometry.")


if __name__ == "__main__":
    main()
