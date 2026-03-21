from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

Point2 = Tuple[float, float]
Triangle = Tuple[Point2, Point2, Point2]

TRACE_KEYS = {
    "front": ("A", "O", "O", "O"),
    "top": ("A", "E1", "E1", "E1"),
    "right": ("A", "E2", "E2", "E2"),
    "left": ("D", "E1", "E1", "E2"),
    "bottom": ("D", "E1", "O", "M+"),
    "back": ("E1", "E1", "E1", "O"),
}


def load_kernel(path: str) -> dict:
    return json.loads(Path(path).read_text())


def trace_map(A: int, sigma: int, tau: int) -> Dict[Tuple[str, ...], int]:
    out: Dict[Tuple[str, ...], int] = {}
    if A == 0:
        out[("A", "O", "O", "O")] = tau
        out[("A", "E1", "E1", "E1")] = sigma
        out[("A", "E2", "E2", "E2")] = 0
    else:
        out[("A", "E2", "E2", "E2")] = 1
        out[("A", "E1", "E1", "E1")] = 1 if (sigma, tau) in {(0, 0), (0, 1)} else 0
        out[("A", "O", "O", "O")] = 1 if (sigma, tau) in {(0, 0), (1, 0)} else 0

    out[("E1", "E1", "E1", "O")] = 1 if (sigma, tau) in {(0, 0), (1, 1)} else 0
    out[("E1", "E1", "E1", "E2")] = sigma

    out[("D", "E1", "E1", "E2")] = 1
    out[("D", "E1", "E1", "M+")] = 1
    out[("D", "E1", "E2", "E2")] = 1
    out[("E2", "E2", "E2", "E2")] = 1

    out[("D", "E1", "O", "M+")] = 0
    out[("E1", "E1", "M+", "M+")] = 0
    out[("E1", "E2", "E2", "E2")] = 0
    out[("E1", "E2", "M+", "M+")] = 0
    out[("E1", "M+", "M+", "O")] = 0
    out[("E2", "E2", "E2", "O")] = 0
    return out


def net_face_origins(face_size: float, gap: float) -> Dict[str, Point2]:
    s = face_size
    g = gap
    return {
        "top": (s + g, 0.0),
        "left": (0.0, s + g),
        "front": (s + g, s + g),
        "right": (2 * (s + g), s + g),
        "back": (3 * (s + g), s + g),
        "bottom": (s + g, 2 * (s + g)),
    }


def square_triangles(origin: Point2, size: float, n: int) -> List[Triangle]:
    ox, oy = origin
    step = size / n
    tris: List[Triangle] = []
    for r in range(n):
        for c in range(n):
            x0 = ox + c * step
            y0 = oy + r * step
            x1 = x0 + step
            y1 = y0 + step
            tris.append(((x0, y0), (x1, y0), (x1, y1)))
            tris.append(((x0, y0), (x1, y1), (x0, y1)))
    return tris


def role_tag(face: str) -> str:
    return {
        "front": "H/O",
        "top": "E1",
        "right": "E2",
        "left": "Do",
        "bottom": "De",
        "back": "C",
    }[face]


def face_triangle_fill(face: str, idx: int, traces: Dict[Tuple[str, ...], int]) -> bool:
    bit = traces[TRACE_KEYS[face]]
    if face == "front":
        return bit == 1 and idx % 2 == 0
    if face == "top":
        return bit == 1 and idx % 3 != 1
    if face == "right":
        return bit == 1 and idx % 3 == 0
    if face == "left":
        return idx % 4 == 0
    if face == "bottom":
        return bit == 1 and idx % 4 != 0
    if face == "back":
        return bit == 1 and idx % 2 == 1
    return False


class DxfWriter:
    def __init__(self) -> None:
        self.parts: List[str] = []

    def add(self, code: int, value: object) -> None:
        self.parts.append(f"{code}\n{value}")

    def start(self) -> None:
        self.add(0, "SECTION")
        self.add(2, "HEADER")
        self.add(0, "ENDSEC")

        self.add(0, "SECTION")
        self.add(2, "TABLES")
        self._layers_table()
        self.add(0, "ENDSEC")

        self.add(0, "SECTION")
        self.add(2, "ENTITIES")

    def finish(self) -> str:
        self.add(0, "ENDSEC")
        self.add(0, "EOF")
        return "\n".join(self.parts) + "\n"

    def _layers_table(self) -> None:
        layers = [
            ("FRAME", 7),
            ("TRI_GRID", 8),
            ("BLACK_FILL", 0),
            ("LABELS", 2),
        ]
        self.add(0, "TABLE")
        self.add(2, "LAYER")
        self.add(70, len(layers))
        for name, color in layers:
            self.add(0, "LAYER")
            self.add(2, name)
            self.add(70, 0)
            self.add(62, color)
            self.add(6, "CONTINUOUS")
        self.add(0, "ENDTAB")

    def line(self, a: Point2, b: Point2, layer: str = "TRI_GRID") -> None:
        self.add(0, "LINE")
        self.add(8, layer)
        self.add(10, f"{a[0]:.6f}")
        self.add(20, f"{-a[1]:.6f}")
        self.add(30, 0.0)
        self.add(11, f"{b[0]:.6f}")
        self.add(21, f"{-b[1]:.6f}")
        self.add(31, 0.0)

    def polyline_closed(self, pts: List[Point2], layer: str = "FRAME") -> None:
        self.add(0, "LWPOLYLINE")
        self.add(8, layer)
        self.add(90, len(pts))
        self.add(70, 1)
        for x, y in pts:
            self.add(10, f"{x:.6f}")
            self.add(20, f"{-y:.6f}")

    def text(self, p: Point2, text: str, height: float = 8.0, layer: str = "LABELS") -> None:
        safe = text.replace("\n", " ")
        self.add(0, "TEXT")
        self.add(8, layer)
        self.add(10, f"{p[0]:.6f}")
        self.add(20, f"{-p[1]:.6f}")
        self.add(30, 0.0)
        self.add(40, f"{height:.6f}")
        self.add(1, safe)


def render_state(state_name: str, state: dict, output_dxf: Path) -> None:
    A = int(state["A"])
    sigma = int(state["sigma"])
    tau = int(state["tau"])
    traces = trace_map(A, sigma, tau)

    face_size = 180.0
    gap = 18.0
    n = 4
    y_offset = 20.0
    origins = net_face_origins(face_size, gap)

    dxf = DxfWriter()
    dxf.start()

    # page labels
    dxf.text((180.0, -20.0), f"state sheet {state_name}", height=12.0)
    dxf.text((180.0, -5.0), f"(A,sigma,tau)=({A},{sigma},{tau})", height=8.0)

    for face, origin in origins.items():
        ox, oy = origin
        oy += y_offset

        tris = square_triangles((ox, oy), face_size, n)

        for idx, tri in enumerate(tris):
            if face_triangle_fill(face, idx, traces):
                dxf.polyline_closed(list(tri), layer="BLACK_FILL")

        # grid lines from triangle edges
        seen = set()
        for tri in tris:
            edges = [(tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])]
            for a, b in edges:
                key = tuple(sorted(((round(a[0], 6), round(a[1], 6)), (round(b[0], 6), round(b[1], 6)))))
                if key in seen:
                    continue
                seen.add(key)
                dxf.line(a, b, layer="TRI_GRID")

        square = [(ox, oy), (ox + face_size, oy), (ox + face_size, oy + face_size), (ox, oy + face_size)]
        dxf.polyline_closed(square, layer="FRAME")

        dxf.text((ox + face_size / 2 - 10, oy - 6), role_tag(face), height=10.0)
        dxf.text(
            (ox + face_size / 2 - 40, oy + face_size + 12),
            f"{''.join(TRACE_KEYS[face])}={'1' if traces[TRACE_KEYS[face]] else '0'}",
            height=6.0,
        )

    output_dxf.write_text(dxf.finish(), encoding="utf-8")


def main() -> None:
    kernel = load_kernel("specs/app/g60_cube_state_kernel_v1.json")
    outdir = Path("renders/state_sheet_gallery_v1")
    outdir.mkdir(parents=True, exist_ok=True)

    for state_name, state in kernel["states"].items():
        path = outdir / f"{state_name}.dxf"
        render_state(state_name, state, path)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
