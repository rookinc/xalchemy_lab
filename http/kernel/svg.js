export const NS = "http://www.w3.org/2000/svg";

export function svgEl(name, attrs = {}) {
  const el = document.createElementNS(NS, name);
  for (const [k, v] of Object.entries(attrs)) {
    el.setAttribute(k, String(v));
  }
  return el;
}

export function line(a, b, attrs = {}) {
  return svgEl("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, ...attrs });
}

export function circle(c, r, attrs = {}) {
  return svgEl("circle", { cx: c.x, cy: c.y, r, ...attrs });
}

export function text(p, str, attrs = {}) {
  const el = svgEl("text", { x: p.x, y: p.y, ...attrs });
  el.textContent = str;
  return el;
}

export function poly(points, attrs = {}) {
  return svgEl("polygon", {
    points: points.map(p => `${p.x},${p.y}`).join(" "),
    ...attrs,
  });
}
