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
    sub.add_parser("stateful", help="run stateful vertex controller demo")
    sub.add_parser("state-table", help="print current state-sensitive routing table")
    sub.add_parser("state-sweep", help="write full state-sensitive routing sweep artifact")
    sub.add_parser("mixed-symmetry", help="probe chart covariance of mixed reopening")
    sub.add_parser("holonomic-loop", help="run local holonomic loop probe")
    sub.add_parser("holonomy-probe", help="run multi-controller holonomy probe")
    sub.add_parser("framed-return", help="run framed return probe")
    sub.add_parser("framed-invariant", help="compute framed return invariant from chart traces")
    sub.add_parser("framed-displacement", help="compute signed framed displacement from chart traces")
    sub.add_parser("framed-signature", help="compute combined framed signature (H,S) from chart traces")
    sub.add_parser("framed-compose", help="test composition law for framed signatures")
    sub.add_parser("native-accumulator", help="run native framed signature accumulator")
    sub.add_parser("predict-signature", help="predict framed signature from controller sequence")
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
        "stateful": "xalchemy_lab.app.hello_vertex_controller_stateful",
        "state-table": "xalchemy_lab.app.hello_state_sensitive_table",
        "state-sweep": "xalchemy_lab.app.hello_state_sensitive_sweep",
        "mixed-symmetry": "xalchemy_lab.app.hello_mixed_reopening_symmetry_probe",
        "holonomic-loop": "xalchemy_lab.app.hello_holonomic_loop_probe",
        "holonomy-probe": "xalchemy_lab.app.hello_multi_controller_holonomy_probe",
        "framed-return": "xalchemy_lab.app.hello_framed_return_probe",
        "framed-invariant": "xalchemy_lab.app.hello_framed_return_invariant",
        "framed-displacement": "xalchemy_lab.app.hello_signed_framed_displacement",
        "framed-signature": "xalchemy_lab.app.hello_framed_signature",
        "framed-compose": "xalchemy_lab.app.hello_framed_signature_composition",
        "native-accumulator": "xalchemy_lab.app.hello_native_framed_accumulator",
        "predict-signature": "xalchemy_lab.app.hello_predict_framed_signature",
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
