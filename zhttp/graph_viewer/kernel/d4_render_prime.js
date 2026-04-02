function rgba(rgb, alpha = 1) {
  return `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${alpha})`;
}

function projectPoint(projector, p) {
  const q = projector.project(p);
  return q ? { x: q.x, y: q.y, depth: q.depth } : null;
}

function faceNormal(a, b, c) {
  const ux = b[0] - a[0];
  const uy = b[1] - a[1];
  const uz = b[2] - a[2];
  const vx = c[0] - a[0];
  const vy = c[1] - a[1];
  const vz = c[2] - a[2];
  return [
    uy * vz - uz * vy,
    uz * vx - ux * vz,
    ux * vy - uy * vx
  ];
}

function avgDepth(points) {
  return points.reduce((s, p) => s + p.depth, 0) / points.length;
}

function drawFace(ctx, pts, fillStyle) {
  ctx.beginPath();
  ctx.moveTo(pts[0].x, pts[0].y);
  ctx.lineTo(pts[1].x, pts[1].y);
  ctx.lineTo(pts[2].x, pts[2].y);
  ctx.closePath();
  ctx.fillStyle = fillStyle;
  ctx.fill();
}

function drawEdge(ctx, a, b, strokeStyle, width = 2) {
  ctx.beginPath();
  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x, b.y);
  ctx.lineWidth = width;
  ctx.strokeStyle = strokeStyle;
  ctx.stroke();
}

export function renderPrimeScene(ctx, snapshot, projector, opts = {}) {
  const {
    showFaces = true,
    showEdges = true,
    edgeOpacity = 1,
    showColorEdges = false,
    showLabels = false,
    highlightActive = true,
    leftFaceOpacity = 0.8,
    rightFaceOpacity = 0.8
  } = opts;

  const verts3 = [
    [-1.35, -1.15, -1.1],
    [ 1.35, -1.15, -1.1],
    [ 0.00,  1.15, -1.1],
    [ 0.00,  0.00,  1.25]
  ];

  const verts2 = verts3.map((p) => projectPoint(projector, p));
  if (verts2.some((v) => !v)) return;

  const faces = [
    { ids: [0, 1, 2], fill: rgba([120, 255, 180], 0.18) },
    { ids: [0, 1, 3], fill: rgba([255, 255, 255], 0.10) },
    { ids: [1, 2, 3], fill: rgba([255, 120, 120], rightFaceOpacity) },
    { ids: [2, 0, 3], fill: rgba([120, 160, 255], leftFaceOpacity) }
  ];

  const visibleFaces = faces
    .map((f) => {
      const tri3 = f.ids.map((i) => verts3[i]);
      const tri2 = f.ids.map((i) => verts2[i]);
      const n = faceNormal(tri3[0], tri3[1], tri3[2]);
      return { ...f, tri2, tri3, nz: n[2], depth: avgDepth(tri2) };
    })
    .sort((a, b) => a.depth - b.depth);

  if (showFaces) {
    ctx.save();
    visibleFaces.forEach((f) => drawFace(ctx, f.tri2, f.fill));
    ctx.restore();
  }

  if (showEdges && edgeOpacity > 0) {
    const edges = [
      [0, 1], [1, 2], [2, 0],
      [0, 3], [1, 3], [2, 3]
    ];

    const width = 0.25 + edgeOpacity * 2.25;

    ctx.save();
    ctx.globalAlpha = Math.max(0, Math.min(1, edgeOpacity));

    edges.forEach(([i, j]) => {
      const color = showColorEdges ? "rgb(180, 220, 255)" : "rgb(255, 255, 255)";
      drawEdge(ctx, verts2[i], verts2[j], color, width);
    });

    ctx.restore();
  }

  if (highlightActive && snapshot?.currentD4s === 0 && edgeOpacity > 0) {
    ctx.save();
    ctx.globalAlpha = Math.max(0, Math.min(1, edgeOpacity));
    drawEdge(ctx, verts2[2], verts2[3], "rgb(255,255,255)", 0.4 + edgeOpacity * 2.6);
    ctx.restore();
  }

  if (showLabels) {
    ctx.save();
    ctx.font = "12px sans-serif";
    ctx.fillStyle = "rgba(255,255,255,0.78)";
    verts2.forEach((p, i) => {
      ctx.fillText(`v${i}`, p.x + 6, p.y - 6);
    });
    ctx.restore();
  }
}
