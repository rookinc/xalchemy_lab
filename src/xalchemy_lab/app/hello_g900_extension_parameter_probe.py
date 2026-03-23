from __future__ import annotations

CENTER = 145
OFFSETS = [0, 1, 2, 5, 10, 15]


def main() -> None:
    print("\nG900 EXTENSION PARAMETER PROBE")
    print("==============================")
    print("Testing centered families (I-d, I, I+d) with fixed quotient image 2I.\n")

    for d in OFFSETS:
        top = CENTER - d
        rung = CENTER
        bottom = CENTER + d
        image = top + bottom

        print(f"d = {d}")
        print(f"  centered triple   : ({top}, {rung}, {bottom})")
        print(f"  quotient image    : {top} + {bottom} = {image}")
        print(f"  equals 2I         : {image == 2 * CENTER}")
        print()

    print("INTERPRETATION")
    print("==============")
    print("For fixed center I, the quotient image 2I is insensitive to d.")
    print("So d is invisible to the base quotient image and must be fixed by extra structure.")


if __name__ == "__main__":
    main()
