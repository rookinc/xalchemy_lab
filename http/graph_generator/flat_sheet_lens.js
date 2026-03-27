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
    handedness: "left",
    lastClosedKey: seedKey,
    previousClosedKey: null,
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

function angleOf(dx, dy) {
  return Math.atan2(dy, dx);
}

function normalizeAngle(theta) {
  while (theta <= -Math.PI) theta += 2 * Math.PI;
  while (theta > Math.PI) theta -= 2 * Math.PI;
  return theta;
}

function boundaryExposure(state, key) {
  const { i, j, up } = parseKey(key);
  return neighborsOf(i, j, up)
    .map(n => cellKey(n.i, n.j, n.up))
    .filter(k => !isOccupied(state, k)).length;
}

function candidatePool(state, fromKey) {
  const { i, j, up } = parseKey(fromKey);
  return neighborsOf(i, j, up)
    .map(n => ({ ...n, key: cellKey(n.i, n.j, n.up) }))
    .filter(n => !isOccupied(state, n.key));
}

function headingAngle(state, fromKey) {
  const last = cellCenterFromKey(fromKey);

  if (state.sheet.previousClosedKey) {
    const prev = cellCenterFromKey(state.sheet.previousClosedKey);
    return angleOf(last.x - prev.x, last.y - prev.y);
  }

  return 0;
}

function turnScore(state, heading, candidateAngle) {
  const delta = normalizeAngle(candidateAngle - heading);
  if (state.sheet.handedness === "left") {
    return delta >= 0 ? delta : (2 * Math.PI + delta);
  }
  return delta <= 0 ? -delta : (2 * Math.PI - delta);
}

function pickBoundaryFollower(state, fromKey) {
  const pool = candidatePool(state, fromKey);
  if (!pool.length) return null;

  const fromCenter = cellCenterFromKey(fromKey);
  const heading = headingAngle(state, fromKey);

  let best = null;
  let bestTuple = null;

  for (const candidate of pool) {
    const candCenter = triCellCenter(candidate.i, candidate.j, candidate.up);
    const candAngle = angleOf(candCenter.x - fromCenter.x, candCenter.y - fromCenter.y);
    const turn = turnScore(state, heading, candAngle);
    const exposure = boundaryExposure(state, candidate.key);
    const radial = candCenter.x + 0.18 * candCenter.y;

    const tuple = [
      turn,
      -exposure,
      radial,
    ];

    if (!bestTuple) {
      best = candidate;
      bestTuple = tuple;
      continue;
    }

    for (let k = 0; k < tuple.length; k++) {
      if (tuple[k] < bestTuple[k]) {
        best = candidate;
        bestTuple = tuple;
        break;
      }
      if (tuple[k] > bestTuple[k]) break;
    }
  }

  return best;
}

function enqueueContinuation(state, key) {
  const chosen = pickBoundaryFollower(state, key);

  if (!chosen) {
    state.history.push(`[flat_sheet] ${key} has no admissible continuation`);
    state.sheet.handedness = state.sheet.handedness === "left" ? "right" : "left";
    return;
  }

  if (!frontierHas(state, chosen.key)) {
    state.sheet.frontier.push(chosen.key);
    state.history.push(`[flat_sheet] frontier <- ${chosen.key} (${state.sheet.handedness})`);
  }

  state.sheet.handedness = state.sheet.handedness === "left" ? "right" : "left";
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

      state.sheet.previousClosedKey = state.sheet.lastClosedKey;
      state.sheet.lastClosedKey = state.sheet.activeKey;

      enqueueContinuation(state, state.sheet.activeKey);
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
    text(svg, 590, 38, "Flat Sheet = handed boundary follower", 22, "#8ea0b3");
    text(svg, 590, 66, "continuation chosen by alternating left/right turn preference", 15, "#8ea0b3");
  }
}

export function status(state, stages) {
  ensureSheetState(state);
  return {
    line1: `cell: ${state.sheet.activeKey}`,
    line2: `stage: ${state.stage} = ${stages[state.stage]}`,
  };
}
