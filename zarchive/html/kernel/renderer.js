import { svgEl, line, circle, text, poly } from "./svg.js";
import { derivedGeometry, derivedCircles } from "../constructions/xyzti.js";

export function renderScene(state) {
  const scene = document.getElementById("scene");
  scene.innerHTML = "";

  const svg = svgEl("svg", {
    viewBox: `0 0 ${state.width} ${state.height}`,
    width: "100%",
    height: "100%",
    style: `background:${state.colors.bg}`,
  });

  const framePad = 24;
  svg.appendChild(
    svgEl("rect", {
      x: framePad,
      y: framePad,
      width: state.width - framePad * 2,
      height: state.height - framePad * 2,
      fill: "none",
      stroke: state.colors.frame,
      "stroke-width": 2,
    })
  );

  const { t0, I, xEnd, yEnd, zEnd, rEnd } = derivedGeometry(state);
  const { rx, ry, rz } = derivedCircles({ t0, xEnd, yEnd, zEnd });

  // T is the loop itself, so keep only the origin-centered circles.
  svg.appendChild(circle(t0, rx, {
    fill: "none",
    stroke: state.colors.x,
    "stroke-width": 1.5,
    "stroke-dasharray": "6 6",
    opacity: 0.45,
  }));
  svg.appendChild(circle(t0, ry, {
    fill: "none",
    stroke: state.colors.y,
    "stroke-width": 1.5,
    "stroke-dasharray": "6 6",
    opacity: 0.45,
  }));
  svg.appendChild(circle(t0, rz, {
    fill: "none",
    stroke: state.colors.z,
    "stroke-width": 1.5,
    "stroke-dasharray": "6 6",
    opacity: 0.45,
  }));

  svg.appendChild(line(t0, xEnd, { stroke: state.colors.x, "stroke-width": 3 }));
  svg.appendChild(line(t0, yEnd, { stroke: state.colors.y, "stroke-width": 3 }));
  svg.appendChild(line(t0, zEnd, { stroke: state.colors.z, "stroke-width": 3 }));
  svg.appendChild(line(t0, I,   { stroke: state.colors.i, "stroke-width": 3 }));

  svg.appendChild(line(t0, rEnd, {
    stroke: state.colors.r,
    "stroke-width": 2.5,
    "stroke-dasharray": "7 5",
    opacity: 0.9,
  }));

  svg.appendChild(poly([t0, xEnd, I], {
    fill: "none",
    stroke: state.colors.tri1,
    "stroke-width": 2,
    opacity: 0.8,
  }));
  svg.appendChild(poly([t0, yEnd, I], {
    fill: "none",
    stroke: state.colors.tri2,
    "stroke-width": 2,
    opacity: 0.8,
  }));
  svg.appendChild(poly([t0, xEnd, yEnd], {
    fill: "none",
    stroke: state.colors.tri3,
    "stroke-width": 2,
    opacity: 0.8,
  }));
  svg.appendChild(poly([I, zEnd, rEnd], {
    fill: "none",
    stroke: state.colors.tri4,
    "stroke-width": 1.5,
    "stroke-dasharray": "5 5",
    opacity: 0.8,
  }));

  const points = [
    { p: t0, label: "0", color: state.colors.t },
    { p: I, label: "I", color: state.colors.i },
    { p: xEnd, label: "x", color: state.colors.x },
    { p: yEnd, label: "y", color: state.colors.y },
    { p: zEnd, label: "z", color: state.colors.z },
    { p: rEnd, label: "r", color: state.colors.r },
  ];

  for (const { p, label, color } of points) {
    svg.appendChild(circle(p, 6, { fill: color, stroke: "#111", "stroke-width": 1.5 }));
    svg.appendChild(text({ x: p.x + 10, y: p.y - 10 }, label, {
      fill: color === state.colors.i ? state.colors.i : state.colors.text,
      "font-size": 22,
      "font-family": "Arial, sans-serif",
    }));
  }

  scene.appendChild(svg);
}
