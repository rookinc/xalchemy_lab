import { text, poly, circle } from "./render.js";

const SIDE = 64;
const H = Math.sqrt(3) * SIDE / 2;
const ORIGIN_X = 44;
const ORIGIN_Y = 78;
const GRID_W = 34;
const GRID_H = 12;

function cellKey(i, j, up) {
  return `${i}:${j}:${up ? "u" : "d"}`;
}

function parseKey(key) {
  const [i, j, u] = key.split(":");
  return { i: Number(i), j: Number(j), up: u === "u" };
}

function triCellCenter(i, j, up) {
  return {
    x: ORIGIN_X + i * (SIDE / 2),
    y: ORIGIN_Y + j * H,
    side: SIDE,
    h: H,
    up,
  };
}

function triPoints(cell) {
  const { x, y, side, h, up } = cell;
  if (up) {
    return [
      { x, y: y - (2 * h / 3) },
      { x: x - side / 2, y: y + h / 3 },
      { x: x + side / 2, y: y + h / 3 },
    ];
  }
  return [
    { x, y: y + (2 * h / 3) },
    { x: x - side / 2, y: y - h / 3 },
    { x: x + side / 2, y: y - h / 3 },
  ];
}

function inBounds(i, j) {
  return i >= 0 && i < GRID_W && j >= 0 && j < GRID_H;
}

function neighborsOf(i, j, up) {
  if (up) {
    return [
      { i: i - 1, j, up: false },
      { i: i + 1, j, up: false },
      { i, j: j - 1, up: false },
    ].filter(n => inBounds(n.i, n.j));
  }
  return [
    { i: i - 1, j, up: true },
    { i: i + 1, j, up: true },
    { i, j: j + 1, up: true },
  ].filter(n => inBounds(n.i, n.j));
}

function ensureSheetState(state) {
  if (state.sheet) return;

  const seed = { i: 13, j: 4, up: true };
  const seedKey = cellKey(seed.i, seed.j, seed.up);

  state.sheet = {
    cells: {
      [seedKey]: {
        fill: "white",
        stage: 0,
        closed: false,
      },
    },
    activeKey: seedKey,
    frontier: [],
    walkIndex: 0,
    turnBias: 1,
  };

  state.currentIndex = 0;
  state.history = ["[flat_sheet] seed white triangle"];
}

function currentCellRecord(state) {
  ensureSheetState(state);
  return state.sheet.cells[state.sheet.activeKey];
}

function isOccupied(state, key) {
  return Boolean(state.sheet.cells[key]);
}

function frontierHas(state, key) {
  return state.sheet.frontier.includes(key);
}

function cellCenterFromKey(key) {
  const meta = parseKey(key);
  return triCellCenter(meta.i, meta.j, meta.up);
}

function perimeterCandidates(state, key) {
  const { i, j, up } = parseKey(key);
  const neighbors = neighborsOf(i, j, up);

  return neighbors
    .map(n => ({ ...n, key: cellKey(n.i, n.j, n.up) }))
    .filter(n => !isOccupied(state, n.key));
}

function scoreCandidate(state, fromKey, candidate) {
  const fromMeta = parseKey(fromKey);
  const fromCenter = triCellCenter(fromMeta.i, fromMeta.j, fromMeta.up);
  const candCenter = triCellCenter(candidate.i, candidate.j, candidate.up);

  const dx = candCenter.x - fromCenter.x;
  const dy = candCenter.y - fromCenter.y;

  const frontierNeighbors = neighborsOf(candidate.i, candidate.j, candidate.up)
    .map(n => cellKey(n.i, n.j, n.up))
    .filter(k => !isOccupied(state, k)).length;

  const boundaryBias = candidate.j === 0 || candidate.j === GRID_H - 1 ? -4 : 0;
  const lateralBias = dx * state.sheet.turnBias;
  const upwardBias = -Math.abs(dy) * 0.08;

  return lateralBias + upwardBias + frontierNeighbors * 0.25 + boundaryBias;
}

function chooseContinuation(state, key) {
  const candidates = perimeterCandidates(state, key);
  if (!candidates.length) return null;

  let best = null;
  let bestScore = -Infinity;

  for (const candidate of candidates) {
    const score = scoreCandidate(state, key, candidate);
    if (score > bestScore) {
      best = candidate;
      bestScore = score;
    }
  }

  return best;
}

function addFrontierFromClosedCell(state, key) {
  const chosen = chooseContinuation(state, key);
  if (!chosen) {
    state.history.push(`[flat_sheet] ${key} has no admissible continuation`);
    state.sheet.turnBias *= -1;
    return;
  }

  if (!frontierHas(state, chosen.key)) {
    state.sheet.frontier.push(chosen.key);
    state.history.push(`[flat_sheet] frontier <- ${chosen.key}`);
  }

  state.sheet.turnBias *= -1;
}

function spawnNextFrontierCell(state) {
  ensureSheetState(state);

  while (state.sheet.frontier.length > 0) {
    const nextKey = state.sheet.frontier.shift();
    if (isOccupied(state, nextKey)) continue;

    const prev = parseKey(state.sheet.activeKey);
    const next = parseKey(nextKey);
    const fill = prev.up === next.up ? "white" : "black";

    state.sheet.cells[nextKey] = {
      fill,
      stage: 1,
      closed: false,
    };
    state.sheet.activeKey = nextKey;
    state.currentIndex += 1;
    state.history.push(`[flat_sheet] continue -> cell ${nextKey}`);
    state.history.push(`[flat_sheet] ${fill} triangle, stage 1 = point`);
    return;
  }

  state.history.push("[flat_sheet] no frontier left");
}

function drawLocked(svg, p, label = "", showLabels = true) {
  circle(svg, p, 8, "#152432", "#7cc4ff", 2.2);
  if (label && showLabels) text(svg, p.x, p.y - 14, label, 10, "#8ea0b3");
}

function drawOpen(svg, p, label = "", showLabels = true) {
  circle(svg, p, 7, "rgba(0,0,0,0)", "#ffd479", 2, "5 5");
  if (label && showLabels) text(svg, p.x, p.y - 14, label, 10, "#ffd479");
}

function drawCellGeometry(svg, cell, record, isActive, layers) {
  const pts = triPoints(cell);
  const c = { x: cell.x, y: cell.y };

  const midAB = { x: (pts[0].x + pts[1].x) / 2, y: (pts[0].y + pts[1].y) / 2 };
  const midAC = { x: (pts[0].x + pts[2].x) / 2, y: (pts[0].y + pts[2].y) / 2 };
  const midBC = { x: (pts[1].x + pts[2].x) / 2, y: (pts[1].y + pts[2].y) / 2 };

  const fillColor = record.fill === "white" ? "rgba(255,255,255,0.16)" : "rgba(255,156,188,0.26)";
  const strokeColor = record.fill === "white" ? "#d8e3ee" : "#b56b86";

  if (layers.nodes && record.stage >= 1) drawLocked(svg, c, isActive ? "1" : "", layers.labels);
  if (layers.nodes && record.stage >= 2) drawLocked(svg, midAB, isActive ? "2" : "", layers.labels);
  if (layers.nodes && record.stage >= 3) drawLocked(svg, midAC, isActive ? "3" : "", layers.labels);
  if (layers.nodes && record.stage >= 5) drawLocked(svg, midBC, isActive ? "5" : "", layers.labels);

  if (layers.cells && record.stage >= 2) {
    poly(svg, [c, midAB, midAC], "rgba(255,255,255,0.04)", "#55718c", 1.2, 1);
  }

  if (layers.cells && record.stage >= 4) {
    poly(svg, pts, fillColor, strokeColor, 1.6, 1);
  }

  if (layers.frontier && record.stage >= 5) {
    const outA = { x: pts[0].x + (pts[0].x - c.x) * 0.35, y: pts[0].y + (pts[0].y - c.y) * 0.35 };
    const outB = { x: pts[1].x + (pts[1].x - c.x) * 0.35, y: pts[1].y + (pts[1].y - c.y) * 0.35 };
    const outC = { x: pts[2].x + (pts[2].x - c.x) * 0.35, y: pts[2].y + (pts[2].y - c.y) * 0.35 };

    drawOpen(svg, outA, "2.5", layers.labels);
    drawOpen(svg, outB, "2.5", layers.labels);
    drawOpen(svg, outC, "2.5", layers.labels);
  }

  if (layers.signs && record.stage >= 5) {
    const outC = { x: pts[2].x + (pts[2].x - c.x) * 0.35, y: pts[2].y + (pts[2].y - c.y) * 0.35 };
    text(
      svg,
      (c.x + midAB.x + midAC.x) / 3,
      (c.y + midAB.y + midAC.y) / 3,
      "+",
      14,
      record.fill === "white" ? "#9cffb0" : "#ff9cbc"
    );
    text(svg, (c.x + midBC.x + outC.x) / 3, (c.y + midBC.y + outC.y) / 3, "-", 14, "#ff9cbc");
  }

  if (layers.labels && record.closed) {
    text(svg, c.x, c.y + 24, record.fill === "white" ? "W" : "B", 11, "#8ea0b3");
  }
}

export function step(state, stages) {
  ensureSheetState(state);
  const rec = currentCellRecord(state);

  if (rec.stage < 5) {
    rec.stage += 1;
    state.stage = rec.stage;
    state.history.push(`[flat_sheet] ${state.sheet.activeKey}, stage ${rec.stage} = ${stages[rec.stage]}`);

    if (rec.stage === 5) {
      rec.closed = true;
      state.history.push(`[flat_sheet] ${state.sheet.activeKey} closes as ${rec.fill}`);
      addFrontierFromClosedCell(state, state.sheet.activeKey);
    }
    return;
  }

  spawnNextFrontierCell(state);
  state.stage = currentCellRecord(state).stage;
}

export function render(svg, state) {
  ensureSheetState(state);
  const { layers } = state;

  if (layers.scaffold) {
    for (let i = 0; i < GRID_W; i++) {
      for (let j = 0; j < GRID_H; j++) {
        poly(svg, triPoints(triCellCenter(i, j, true)), "rgba(255,255,255,0.01)", "#273645", 1);
        poly(svg, triPoints(triCellCenter(i, j, false)), "rgba(255,255,255,0.01)", "#273645", 1);
      }
    }
  }

  for (const [key, record] of Object.entries(state.sheet.cells)) {
    const meta = parseKey(key);
    drawCellGeometry(svg, triCellCenter(meta.i, meta.j, meta.up), record, key === state.sheet.activeKey, layers);
  }

  if (layers.frontier) {
    for (const key of state.sheet.frontier) {
      const center = cellCenterFromKey(key);
      drawOpen(svg, { x: center.x, y: center.y });
    }
  }

  if (layers.labels) {
    text(svg, 590, 38, "Flat Sheet = perimeter-guided triangle growth", 22, "#8ea0b3");
    text(svg, 590, 66, "one continuation per closure; no blanket fill", 15, "#8ea0b3");
  }
}

export function status(state, stages) {
  ensureSheetState(state);
  return {
    line1: `cell: ${state.sheet.activeKey}`,
    line2: `stage: ${state.stage} = ${stages[state.stage]}`,
  };
}
