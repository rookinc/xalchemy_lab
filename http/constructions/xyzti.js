import { polarFrom, dist } from "../kernel/geometry.js";

export function derivedGeometry(state) {
  const t0 = state.origin;
  const phase = state.T * 3.6;
  const s = Math.sin(phase * Math.PI / 180);

  const zAngle = 0;
  const iAngle = 180;
  const rAngle = 45;

  const spread = 110 + 18 * s;

  const xAngle = 360 - spread;
  const yAngle = spread;

  const xLength = state.rayLength + 8 * Math.sin((phase + 120) * Math.PI / 180);
  const yLength = state.rayLength + 8 * Math.sin((phase + 240) * Math.PI / 180);
  const zLength = state.zLength + 8 * Math.sin((phase + 0) * Math.PI / 180);

  const iRadius = state.iRadius + 10 * Math.sin((phase + 180) * Math.PI / 180);
  const rLength = state.rLength + 10 * Math.sin((phase + 60) * Math.PI / 180);

  const xEnd = polarFrom(t0, xAngle, xLength);
  const yEnd = polarFrom(t0, yAngle, yLength);
  const zEnd = polarFrom(t0, zAngle, zLength);
  const I = polarFrom(t0, iAngle, iRadius);
  const rEnd = polarFrom(t0, rAngle, rLength);

  return { t0, I, xEnd, yEnd, zEnd, rEnd };
}

export function derivedCircles(geom) {
  return {
    rx: dist(geom.t0, geom.xEnd),
    ry: dist(geom.t0, geom.yEnd),
    rz: dist(geom.t0, geom.zEnd),
  };
}
