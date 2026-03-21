from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import tomllib  # py311+
except Exception:  # pragma: no cover
    tomllib = None


DEFAULT_CONFIG = "config/app.toml"


def load_toml(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    if tomllib is None:
        raise RuntimeError("tomllib not available; use Python 3.11+")
    with p.open("rb") as fh:
        return tomllib.load(fh)


def run_module(module: str) -> int:
    cmd = [sys.executable, "-m", module]
    return subprocess.call(cmd)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xalchemy",
        description="Alchemy Lab app CLI",
    )
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help=f"TOML config path (default: {DEFAULT_CONFIG})",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("cube", help="export the single semantic cube SVG")
    sub.add_parser("png", help="export the single semantic cube PNG")
    sub.add_parser("gallery", help="export all state cube SVG/PNG renders")
    sub.add_parser("contact", help="build contact sheet from gallery renders")
    sub.add_parser("sheet", help="export unfolded state sheet SVG/PNG renders")
    sub.add_parser("dxf", help="export unfolded state sheet DXF renders")
    sub.add_parser("stress", help="run stressed vertex controller demo")
    sub.add_parser("all", help="run gallery, contact, sheet, and dxf")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Load config now so future subcommands can use it.
    # For this first version, loading it mainly validates presence and format.
    try:
        _cfg = load_toml(args.config)
    except Exception as exc:
        print(f"error loading config {args.config}: {exc}", file=sys.stderr)
        return 2

    command_to_module = {
        "cube": "xalchemy_lab.app.export_g60_cube_svg",
        "png": "xalchemy_lab.app.export_g60_cube_png",
        "gallery": "xalchemy_lab.app.export_g60_state_cube_svg",
        "contact": "xalchemy_lab.app.export_g60_state_contact_sheet",
        "sheet": "xalchemy_lab.app.export_g60_state_sheet_svg",
        "dxf": "xalchemy_lab.app.export_g60_state_sheet_dxf",
        "stress": "xalchemy_lab.app.hello_vertex_controller_stress",
    }

    if args.command == "all":
        for name in ["gallery", "contact", "sheet", "dxf"]:
            rc = run_module(command_to_module[name])
            if rc != 0:
                return rc
        return 0

    return run_module(command_to_module[args.command])


if __name__ == "__main__":
    raise SystemExit(main())
