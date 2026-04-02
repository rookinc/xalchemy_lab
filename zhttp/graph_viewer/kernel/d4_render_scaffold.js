function projectPoint(projector, p) {
  const q = projector.project(p);
  return q ? { x: q.x, y: q.y, depth: q.depth } : null;
}

const EDGE_COLORS = [
  "rgb(130, 190, 255)",
  "rgb(255, 120, 120)",
  "rgb(120, 255, 180)"
];

export function buildScaffoldPoints(currentD4s = 0) {
  const r = 1.75 + Math.max(0, currentD4s) * 0.015;
  return [
    { id: "a", pos: [-r, -r, -r] },
    { id: "b", pos: [ r, -r, -r] },
    { id: "c", pos: [ 0,  r, -r] },
    { id: "d", pos: [ 0,  0,  r] }
  ];
}

export function renderScaffold(ctx, points, projector, opts = {}) {
  const {
    showEdges = true,
    edgeOpacity = 1,
    showColorEdges = false,
    showLabels = false,
    alphaScale = 0.28
  } = opts;

  const projected = points
    .map((p) => ({ ...p, q: projectPoint(projector, p.pos) }))
    .filter((p) => p.q);

  if (projected.length < 2) return;

  const edges = [
    [0, 1], [1, 2], [2, 0],
    [0, 3], [1, 3], [2, 3]
  ];

  if (showEdges && edgeOpacity > 0) {
    ctx.save();
    ctx.lineWidth = 1.25;
    ctx.globalAlpha = Math.max(0, Math.min(1, alphaScale * edgeOpacity));

    edges.forEach(([i, j], idx) => {
      const a = projected[i];
      const b = projected[j];
      if (!a || !b) return;

      ctx.beginPath();
      ctx.moveTo(a.q.x, a.q.y);
      ctx.lineTo(b.q.x, b.q.y);
      ctx.strokeStyle = showColorEdges
        ? EDGE_COLORS[idx % EDGE_COLORS.length]
        : "rgb(255, 255, 255)";
      ctx.stroke();
    });

    ctx.restore();
  }

  if (showLabels) {
    ctx.save();
    ctx.font = "12px sans-serif";
    ctx.fillStyle = "rgba(255,255,255,0.72)";
    projected.forEach((p) => {
      ctx.fillText(p.id, p.q.x + 6, p.q.y - 6);
    });
    ctx.restore();
  }
}
