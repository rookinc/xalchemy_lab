from __future__ import annotations


def main() -> None:
    coarse_edge = 290
    even_edge = 160
    odd_edge = 130

    prism_bit0 = 140
    prism_rung = 145
    prism_bit1 = 150

    triangle_mid = (even_edge + odd_edge) / 2
    prism_mid = prism_rung

    print("G900 SCALAR DESCENT PROBE")
    print("=========================")

    print("\ntriangle edge scalars")
    print(f"  coarse = {coarse_edge}")
    print(f"  even   = {even_edge}")
    print(f"  odd    = {odd_edge}")

    print("\ntriangle total weights")
    print(f"  coarse total = {3 * coarse_edge}")
    print(f"  even total   = {3 * even_edge}")
    print(f"  odd total    = {3 * odd_edge}")

    print("\ntriangle parity normalization")
    print(f"  midpoint = {triangle_mid}")
    print(f"  even offset from midpoint = {even_edge - triangle_mid}")
    print(f"  odd  offset from midpoint = {odd_edge - triangle_mid}")

    print("\nprism normalization")
    print(f"  midpoint = {prism_mid}")
    print(f"  bit0 face offset = {prism_bit0 - prism_mid}")
    print(f"  rung      offset = {prism_rung - prism_mid}")
    print(f"  bit1 face offset = {prism_bit1 - prism_mid}")

    print("\nshared center test")
    print(f"  prism midpoint == triangle midpoint -> {prism_mid == triangle_mid}")

    print("\nratio checks")
    print(f"  even/odd = {even_edge / odd_edge:.12f}")
    print(f"  coarse/even = {coarse_edge / even_edge:.12f}")
    print(f"  coarse/odd = {coarse_edge / odd_edge:.12f}")


if __name__ == "__main__":
    main()
