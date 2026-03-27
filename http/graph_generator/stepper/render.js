export function text(svg, x, y, value, size = 16, fill = "white", anchor = "middle", weight = "500") {
  const el = document.createElementNS("http://www.w3.org/2000/svg", "text");
  el.setAttribute("x", x);
  el.setAttribute("y", y);
  el.setAttribute("fill", fill);
  el.setAttribute("font-size", size);
  el.setAttribute("text-anchor", anchor);
  el.setAttribute("font-weight", weight);
  el.textContent = value;
  svg.appendChild(el);
  return el;
}

export function line(svg, a, b, stroke, width = 3, dash = "") {
  const el = document.createElementNS("http://www.w3.org/2000/svg", "line");
  el.setAttribute("x1", a.x);
  el.setAttribute("y1", a.y);
  el.setAttribute("x2", b.x);
  el.setAttribute("y2", b.y);
  el.setAttribute("stroke", stroke);
  el.setAttribute("stroke-width", width);
  if (dash) el.setAttribute("stroke-dasharray", dash);
  svg.appendChild(el);
  return el;
}

export function circle(svg, p, r, fill, stroke, width = 2, dash = "") {
  const el = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  el.setAttribute("cx", p.x);
  el.setAttribute("cy", p.y);
  el.setAttribute("r", r);
  el.setAttribute("fill", fill);
  el.setAttribute("stroke", stroke);
  el.setAttribute("stroke-width", width);
  if (dash) el.setAttribute("stroke-dasharray", dash);
  svg.appendChild(el);
  return el;
}

export function poly(svg, pts, fill, stroke = "#2a3948", width = 2, opacity = 1) {
  const el = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
  el.setAttribute("points", pts.map(p => `${p.x},${p.y}`).join(" "));
  el.setAttribute("fill", fill);
  el.setAttribute("stroke", stroke);
  el.setAttribute("stroke-width", width);
  el.setAttribute("opacity", opacity);
  svg.appendChild(el);
  return el;
}
