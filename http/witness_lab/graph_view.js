function edgeStroke(edge) {
  if (edge.is_payload_edge) return "rgba(255, 210, 120, 0.95)";
  if (edge.type === "diad") return "rgba(120, 170, 255, 0.92)";
  return "rgba(120, 255, 190, 0.92)";
}

function nodeFill(node) {
  if (node.is_payload) return "rgba(255, 210, 120, 0.18)";
  if (node.kind === "o") return "rgba(120, 170, 255, 0.16)";
  if (node.kind === "s") return "rgba(120, 255, 190, 0.14)";
  return "rgba(255, 120, 120, 0.14)";
}

function nodeStroke(node) {
  if (node.is_payload) return "rgba(255, 210, 120, 0.98)";
  if (node.kind === "o") return "rgba(120, 170, 255, 0.95)";
  if (node.kind === "s") return "rgba(120, 255, 190, 0.95)";
  return "rgba(255, 120, 120, 0.95)";
}

export function renderWitnessGraph(canvas, structure) {
  const ctx = canvas.getContext("2d");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const width = Math.max(1, Math.floor(rect.width * dpr));
  const height = Math.max(1, Math.floor(rect.height * dpr));

  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(dpr, dpr);

  ctx.clearRect(0, 0, rect.width, rect.height);

  if (!structure || !structure.nodes || !structure.edges) return;

  const cx = rect.width * 0.5;
  const cy = rect.height * 0.52;
  const radius = Math.min(rect.width, rect.height) * 0.33;

  const positioned = new Map();

  structure.nodes.forEach((node, idx) => {
    const angle = -Math.PI / 2 + (idx * Math.PI * 2) / structure.nodes.length;
    positioned.set(node.id, {
      ...node,
      x: cx + Math.cos(angle) * radius,
      y: cy + Math.sin(angle) * radius,
    });
  });

  ctx.save();
  ctx.strokeStyle = "rgba(255,255,255,0.06)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();

  ctx.save();
  structure.edges.forEach((edge) => {
    const a = positioned.get(edge.source);
    const b = positioned.get(edge.target);
    if (!a || !b) return;

    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.strokeStyle = edgeStroke(edge);
    ctx.lineWidth = edge.is_payload_edge ? 3 : 2;
    ctx.stroke();
  });
  ctx.restore();

  ctx.save();
  structure.nodes.forEach((node) => {
    const p = positioned.get(node.id);
    if (!p) return;

    ctx.beginPath();
    ctx.arc(p.x, p.y, node.is_payload ? 19 : 16, 0, Math.PI * 2);
    ctx.fillStyle = nodeFill(node);
    ctx.fill();
    ctx.strokeStyle = nodeStroke(node);
    ctx.lineWidth = node.is_payload ? 2.5 : 2;
    ctx.stroke();

    ctx.fillStyle = "rgba(232,240,248,0.96)";
    ctx.font = "600 13px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(node.label, p.x, p.y);

    ctx.fillStyle = "rgba(159,176,195,0.92)";
    ctx.font = "11px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace";
    ctx.fillText(node.role, p.x, p.y + 28);
  });
  ctx.restore();

  ctx.save();
  ctx.fillStyle = "rgba(159,176,195,0.92)";
  ctx.font = "12px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace";
  ctx.textAlign = "left";
  ctx.textBaseline = "top";
  ctx.fillText(`phase: ${structure.phase_label}`, 16, 16);
  ctx.fillText(`payload: ${structure.meta.payload}`, 16, 34);
  ctx.fillText(`code: ${structure.code}`, 16, 52);
  ctx.restore();
}
