import { text, line, circle, poly } from "./render.js";

export const WALK = [0, 3, 1, 4, 2, 7, 5, 8, 6, 9];

function regularPentagon(cx, cy, r, startDeg) {
  const pts = [];
  for (let i = 0; i < 5; i++) {
    const a = (startDeg + i * 72) * Math.PI / 180;
    pts.push({ x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) });
  }
  return pts;
}

function buildLayout() {
  const cx = 590, cy = 390;
  const outer = regularPentagon(cx, cy, 255, -90);
  const inner = regularPentagon(cx, cy, 118, -54);

  const nodes = {};
  for (let i = 0; i < 5; i++) nodes[i] = outer[i];
  for (let i = 0; i < 5; i++) nodes[5 + i] = inner[i];

  const edges = [];
  for (let i = 0; i < 5; i++) edges.push({ a: i, b: (i + 1) % 5, kind: "outer" });
  for (let i = 0; i < 5; i++) edges.push({ a: i, b: 5 + i, kind: "spoke" });
  for (const [a, b] of [[5, 7], [7, 9], [9, 6], [6, 8], [8, 5]]) edges.push({ a, b, kind: "inner" });

  return { nodes, edges };
}

const LAYOUT = buildLayout();

function unit(vx, vy) {
  const len = Math.hypot(vx, vy) || 1;
  return { x: vx / len, y: vy / len };
}

function add(p, v, s = 1) {
  return { x: p.x + v.x * s, y: p.y + v.y * s };
}

function drawLocked(svg, p, label = "", showLabels = true) {
  circle(svg, p, 9, "#152432", "#7cc4ff", 2.4);
  if (label && showLabels) text(svg, p.x, p.y - 14, label, 10, "#8ea0b3");
}

function drawOpen(svg, p, label = "", showLabels = true) {
  circle(svg, p, 8, "rgba(0,0,0,0)", "#ffd479", 2.2, "5 5");
  if (label && showLabels) text(svg, p.x, p.y - 14, label, 10, "#ffd479");
}

function orientedGeometry(nodeId, walkIndex) {
  const curr = LAYOUT.nodes[nodeId];
  const prevId = WALK[(walkIndex - 1 + WALK.length) % WALK.length];
  const nextId = WALK[(walkIndex + 1) % WALK.length];
  const prev = LAYOUT.nodes[prevId];
  const next = LAYOUT.nodes[nextId];

  const vin = unit(prev.x - curr.x, prev.y - curr.y);
  const vout = unit(next.x - curr.x, next.y - curr.y);

  const p2 = add(curr, vin, 78);
  const p3 = add(curr, vout, 78);
  const bis = unit(vin.x + vout.x, vin.y + vout.y);
  const outward = unit(-bis.x, -bis.y);
  const p5 = add(curr, outward, 92);
  const qA = add(p2, outward, 58);
  const qB = add(p3, outward, 58);
  const qC = add(p5, outward, 62);

  return { curr, p2, p3, p5, qA, qB, qC };
}

function drawMotif(svg, nodeId, walkIndex, stage, completedSigns, layers) {
  const g = orientedGeometry(nodeId, walkIndex);
  const { curr, p2, p3, p5, qA, qB, qC } = g;

  if (layers.nodes && stage >= 1) drawLocked(svg, curr, "1", layers.labels);
  if (layers.nodes && stage >= 2) drawLocked(svg, p2, "2", layers.labels);
  if (layers.nodes && stage >= 3) drawLocked(svg, p3, "3", layers.labels);
  if (layers.nodes && stage >= 5) drawLocked(svg, p5, "5", layers.labels);

  if (layers.cells && stage >= 2) line(svg, curr, p2, "#ffd166", 2.6);
  if (layers.cells && stage >= 3) line(svg, curr, p3, "#ffd166", 2.6);
  if (layers.cells && stage >= 4) {
    line(svg, p2, p3, "#6fb2ff", 2.6);
    poly(svg, [p2, p3, curr], "rgba(124,196,255,0.08)", "#55718c", 1.8, 1);
  }
  if (layers.cells && stage >= 5) {
    line(svg, curr, p5, "#ffd166", 2.6);
    poly(svg, [curr, p2, qA], "rgba(156,255,176,0.14)", "#4e6d57", 1.4, 1);
    poly(svg, [curr, p3, qB], "rgba(255,156,188,0.14)", "#7a5061", 1.4, 1);
    poly(svg, [curr, p5, qC], "rgba(255,156,188,0.14)", "#7a5061", 1.4, 1);
  }

  if (layers.frontier && stage >= 5) {
    drawOpen(svg, qA, "2.5", layers.labels);
    drawOpen(svg, qB, "2.5", layers.labels);
    drawOpen(svg, qC, "2.5", layers.labels);
  }

  if (layers.signs && stage >= 5) {
    text(svg, (curr.x + p2.x + qA.x) / 3, (curr.y + p2.y + qA.y) / 3, "+", 15, "#9cffb0");
    text(svg, (curr.x + p3.x + qB.x) / 3, (curr.y + p3.y + qB.y) / 3, "-", 15, "#ff9cbc");
    text(svg, (curr.x + p5.x + qC.x) / 3, (curr.y + p5.y + qC.y) / 3, "-", 15, "#ff9cbc");
  }

  if (layers.labels && completedSigns) {
    text(svg, curr.x, curr.y + 24, "K_R_2_top", 10, "#8ea0b3");
  }
}

function addPoint(bounds, p) {
  bounds.minX = Math.min(bounds.minX, p.x);
  bounds.maxX = Math.max(bounds.maxX, p.x);
  bounds.minY = Math.min(bounds.minY, p.y);
  bounds.maxY = Math.max(bounds.maxY, p.y);
}

function emptyBounds() {
  return { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity };
}

export function getViewBox(state) {
  const bounds = emptyBounds();

  for (let i = 0; i < WALK.length; i++) {
    const nodeId = WALK[i];
    const rec = state.completed[nodeId];
    if (!rec || rec.maxStage < 4) continue;

    const { curr, p2, p3, p5, qA, qB, qC } = orientedGeometry(nodeId, i);
    [curr, p2, p3, p5, qA, qB, qC].forEach((p) => addPoint(bounds, p));
  }

  if (!Number.isFinite(bounds.minX)) {
    return "140 40 900 700";
  }

  const width = Math.max(220, bounds.maxX - bounds.minX);
  const height = Math.max(220, bounds.maxY - bounds.minY);
  const margin = Math.max(90, Math.max(width, height) * 0.22);

  return `${bounds.minX - margin} ${bounds.minY - margin} ${width + margin * 2} ${height + margin * 2}`;
}

export function step(state, stages) {
  const nodeId = WALK[state.currentIndex];
  if (!state.completed[nodeId]) state.completed[nodeId] = { maxStage: 0, classLabel: "", signs: [] };

  if (state.stage < 5) {
    state.stage += 1;
    state.ticks += 1;
    state.completed[nodeId].maxStage = Math.max(state.completed[nodeId].maxStage, state.stage);
    state.history.push(`[petersen] node ${nodeId}, stage ${state.stage} = ${stages[state.stage]}`);
    if (state.stage === 5) {
      state.completed[nodeId].classLabel = "K_R_2_top";
      state.completed[nodeId].signs = ["+", "-", "-"];
      state.history.push(`[petersen] node ${nodeId} closes -> K_R_2_top / (+,-,-)`);
    }
  } else {
    state.currentIndex = (state.currentIndex + 1) % WALK.length;
    state.stage = 1;
    state.ticks += 1;
    const nextId = WALK[state.currentIndex];
    if (!state.completed[nextId]) state.completed[nextId] = { maxStage: 0, classLabel: "", signs: [] };
    state.completed[nextId].maxStage = Math.max(state.completed[nextId].maxStage, 1);
    state.history.push(`[petersen] continue -> node ${nextId}`);
    state.history.push(`[petersen] node ${nextId}, stage 1 = point`);
  }
}

export function render(svg, state) {
  const { layers } = state;

  if (layers.scaffold) {
    for (const e of LAYOUT.edges) {
      const stroke = e.kind === "outer" ? "#6fb2ff" : e.kind === "spoke" ? "#ffd166" : "#ff78b0";
      line(svg, LAYOUT.nodes[e.a], LAYOUT.nodes[e.b], stroke, 3);
    }
  }

  if (layers.nodes) {
    for (let i = 0; i < 10; i++) {
      const p = LAYOUT.nodes[i];
      circle(svg, p, 17, "#e8eef5", "#9aaaba", 1.5);
      if (layers.labels) text(svg, p.x, p.y + 6, String(i), 15, "#1a2430", "middle", "700");
    }
  }

  for (let i = 0; i < WALK.length; i++) {
    const nodeId = WALK[i];
    const rec = state.completed[nodeId];
    if (rec && rec.maxStage > 0) drawMotif(svg, nodeId, i, rec.maxStage, rec.maxStage >= 5 ? rec.signs : null, layers);
  }

  if (layers.frontier) {
    const active = LAYOUT.nodes[WALK[state.currentIndex]];
    circle(svg, active, 24, "rgba(0,0,0,0)", "#ffd479", 2.4, "7 6");
  }
}

export function status(state, stages) {
  return {
    line1: `node: ${WALK[state.currentIndex]}`,
    line2: `stage: ${state.stage} = ${stages[state.stage]}`,
  };
}
