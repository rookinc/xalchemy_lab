from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


SVG_PATH = Path("renders/g60_cube_kernel_v1.svg")
PNG_PATH = Path("renders/g60_cube_kernel_v1.png")


def run_cmd(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True)
        return True
    except Exception:
        return False


def main() -> None:
    if not SVG_PATH.exists():
        print(f"missing svg: {SVG_PATH}")
        print("run the svg exporter first:")
        print("  PYTHONPATH=src python -m xalchemy_lab.export_g60_cube_svg")
        raise SystemExit(1)

    PNG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 1. CairoSVG via python module
    try:
        import cairosvg  # type: ignore

        cairosvg.svg2png(
            url=str(SVG_PATH),
            write_to=str(PNG_PATH),
            output_width=1200,
            output_height=900,
        )
        print(f"wrote {PNG_PATH} via cairosvg")
        return
    except Exception:
        pass

    # 2. rsvg-convert
    if shutil.which("rsvg-convert"):
        if run_cmd([
            "rsvg-convert",
            "-w", "1200",
            "-h", "900",
            "-o", str(PNG_PATH),
            str(SVG_PATH),
        ]):
            print(f"wrote {PNG_PATH} via rsvg-convert")
            return

    # 3. ImageMagick magick
    if shutil.which("magick"):
        if run_cmd([
            "magick",
            "-background", "white",
            "-density", "200",
            str(SVG_PATH),
            str(PNG_PATH),
        ]):
            print(f"wrote {PNG_PATH} via magick")
            return

    # 4. legacy ImageMagick convert
    if shutil.which("convert"):
        if run_cmd([
            "convert",
            "-background", "white",
            "-density", "200",
            str(SVG_PATH),
            str(PNG_PATH),
        ]):
            print(f"wrote {PNG_PATH} via convert")
            return

    # 5. Inkscape CLI
    if shutil.which("inkscape"):
        if run_cmd([
            "inkscape",
            str(SVG_PATH),
            "--export-type=png",
            f"--export-filename={PNG_PATH}",
            "--export-width=1200",
            "--export-height=900",
        ]):
            print(f"wrote {PNG_PATH} via inkscape")
            return

    print("could not export PNG.")
    print("Install one of:")
    print("  pip install cairosvg")
    print("or a system tool:")
    print("  pkg install librsvg")
    print("  pkg install imagemagick")
    print("  pkg install inkscape")
    raise SystemExit(2)


if __name__ == "__main__":
    main()
