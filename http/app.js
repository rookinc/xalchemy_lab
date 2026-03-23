const svg = document.getElementById('view');

function addSvg(tag, attrs = {}) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [key, value] of Object.entries(attrs)) {
    el.setAttribute(key, String(value));
  }
  svg.appendChild(el);
  return el;
}

function addLine(x1, y1, x2, y2, stroke = 'white', width = 2, opacity = 1) {
  return addSvg('line', {
    x1, y1, x2, y2,
    stroke,
    'stroke-width': width,
    opacity
  });
}

function addCircle(cx, cy, r, fill = 'white', stroke = 'none', strokeWidth = 0, opacity = 1) {
  return addSvg('circle', {
    cx, cy, r, fill, stroke,
    'stroke-width': strokeWidth,
    opacity
  });
}

function addText(x, y, text, fill = 'white', size = 18) {
  const el = addSvg('text', {
    x, y, fill,
    'font-size': size,
    'font-family': 'Arial, sans-serif'
  });
  el.textContent = text;
  return el;
}

function pointOnRay(origin, dir, step) {
  return {
    x: origin.x + dir.x * step,
    y: origin.y + dir.y * step
  };
}

function normalize(v) {
  const mag = Math.hypot(v.x, v.y) || 1;
  return { x: v.x / mag, y: v.y / mag };
}

const state = {
  O: { x: 400, y: 250 },
  x: { x: 250, y: 300 },
  y: { x: 550, y: 300 },
  z: { x: 400, y: 120 },
  I: { x: 340, y: 210 },
  stepSize: 70,
  steps: 4
};

svg.innerHTML = '';

// local channels
addLine(state.O.x, state.O.y, state.x.x, state.x.y, '#4fc3f7', 2);
addLine(state.O.x, state.O.y, state.y.x, state.y.y, '#81c784', 2);
addLine(state.O.x, state.O.y, state.z.x, state.z.y, '#ef9a9a', 2);

// core points
addCircle(state.O.x, state.O.y, 4, 'white');
addCircle(state.x.x, state.x.y, 6, '#4fc3f7');
addCircle(state.y.x, state.y.y, 6, '#81c784');
addCircle(state.z.x, state.z.y, 6, '#ef9a9a');
addCircle(state.I.x, state.I.y, 6, '#ffd54f');

// labels
addText(state.O.x + 10, state.O.y - 10, 'O', '#aaa', 16);
addText(state.x.x + 10, state.x.y, 'x', '#4fc3f7');
addText(state.y.x + 10, state.y.y, 'y', '#81c784');
addText(state.z.x + 10, state.z.y, 'z', '#ef9a9a');
addText(state.I.x + 10, state.I.y - 6, 'I', '#ffd54f');

// admissible direction from xyz
const dir = normalize({
  x: (state.x.x + state.y.x + state.z.x) / 3 - state.O.x,
  y: (state.x.y + state.y.y + state.z.y) / 3 - state.O.y
});

// t0 starts at the decision site
const t0 = { x: state.O.x, y: state.O.y };
addCircle(t0.x, t0.y, 5, '#ffffff');
addText(t0.x + 10, t0.y - 14, 't0', '#ffffff', 16);

// draw I -> t0
addLine(state.I.x, state.I.y, t0.x, t0.y, '#ffd54f', 2);

let prev = t0;

for (let n = 1; n <= state.steps; n++) {
  const t = pointOnRay(t0, dir, state.stepSize * n);

  addLine(prev.x, prev.y, t.x, t.y, n === state.steps ? '#ffffff' : '#cccccc', 2);
  addCircle(t.x, t.y, 5, n === state.steps ? '#ffffff' : '#dddddd');
  addText(t.x + 10, t.y - 8, `t${n}`, '#ffffff', 16);

  prev = t;
}

addText(prev.x + 18, prev.y + 4, 'R', '#ffffff', 20);

console.log('admissible action renderer alive: t0 -> t1 -> ... -> R');
