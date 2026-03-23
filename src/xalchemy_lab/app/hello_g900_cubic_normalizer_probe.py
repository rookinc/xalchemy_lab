from __future__ import annotations

import math


def f(x: float) -> float:
    return 64 * x**3 + 64 * x**2 + 7 * x - 9


def positive_root_bisection(a: float = 0.0, b: float = 1.0, steps: int = 100) -> float:
    fa = f(a)
    fb = f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("interval does not bracket a root")

    left = a
    right = b
    for _ in range(steps):
        mid = (left + right) / 2
        fm = f(mid)
        if fm == 0:
            return mid
        if fa * fm < 0:
            right = mid
            fb = fm
        else:
            left = mid
            fa = fm
    return (left + right) / 2


def main() -> None:
    I = 145
    d = 5
    L = 10

    x = positive_root_bisection(0.0, 1.0, 120)

    ratios = [
        ("d / I", d / I),
        ("L / I", L / I),
        ("d / L", d / L),
        ("I / d", I / d),
        ("I / L", I / L),
        ("L / d", L / d),
        ("1 / 29", 1 / 29),
        ("2 / 29", 2 / 29),
        ("sqrt(x)", math.sqrt(x)),
        ("x^2", x * x),
        ("1 - x", 1 - x),
        ("x / (1 - x)", x / (1 - x)),
        ("(1 - x) / x", (1 - x) / x),
    ]

    print("\nG900 CUBIC NORMALIZER PROBE")
    print("===========================")
    print("Cubic: 64x^3 + 64x^2 + 7x - 9 = 0")
    print(f"positive root x*   : {x:.15f}")
    print(f"check f(x*)        : {f(x):.15e}")

    print("\nCURRENT G900 DATA")
    print("=================")
    print(f"I                 : {I}")
    print(f"d                 : {d}")
    print(f"L                 : {L}")

    print("\nNORMALIZED QUANTITIES")
    print("=====================")
    for name, value in ratios:
        print(f"{name:16} = {value:.15f}")

    print("\nDIFFERENCES FROM x*")
    print("===================")
    for name, value in ratios:
        print(f"|x* - {name:10}| = {abs(x - value):.15f}")

    print("\nINTERPRETATION")
    print("==============")
    print("Use x* as a candidate dimensionless normalizer for extension data.")
    print("Do not assume a match is meaningful unless it is both numerically close and structurally interpretable.")


if __name__ == "__main__":
    main()
