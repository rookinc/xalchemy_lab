export class CanvasGraphRenderer {
  constructor(canvas, graph, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.graph = graph;
    this.nodes = graph.nodes;
    this.edges = graph.edges;
    this.nodeRadius = options.nodeRadius ?? 10;
    this.dragged = null;

    this.resize = this.resize.bind(this);
    this.onPointerDown = this.onPointerDown.bind(this);
    this.onPointerMove = this.onPointerMove.bind(this);
    this.onPointerUp = this.onPointerUp.bind(this);

    window.addEventListener("resize", this.resize);
    canvas.addEventListener("pointerdown", this.onPointerDown);
    canvas.addEventListener("pointermove", this.onPointerMove);
    window.addEventListener("pointerup", this.onPointerUp);

    this.resize();
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  pointerPos(event) {
    const rect = this.canvas.getBoundingClientRect();
    return {
      x: (event.clientX - rect.left) * (this.canvas.width / rect.width),
      y: (event.clientY - rect.top) * (this.canvas.height / rect.height),
    };
  }

  nearestNode(x, y) {
    let best = null;
    let bestD2 = Infinity;

    for (const n of this.nodes) {
      const dx = n.x - x;
      const dy = n.y - y;
      const d2 = dx * dx + dy * dy;
      if (d2 < bestD2) {
        bestD2 = d2;
        best = n;
      }
    }

    return bestD2 <= 30 * 30 ? best : null;
  }

  onPointerDown(event) {
    const p = this.pointerPos(event);
    this.dragged = this.nearestNode(p.x, p.y);
    if (this.dragged) {
      this.dragged.vx = 0;
      this.dragged.vy = 0;
    }
  }

  onPointerMove(event) {
    if (!this.dragged) return;
    const p = this.pointerPos(event);
    this.dragged.x = p.x;
    this.dragged.y = p.y;
    this.dragged.vx = 0;
    this.dragged.vy = 0;
  }

  onPointerUp() {
    this.dragged = null;
  }

  draw() {
    const ctx = this.ctx;
    const { canvas } = this;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#6aa9ff";
    ctx.lineWidth = 2;

    for (const [i, j] of this.edges) {
      const a = this.nodes[i];
      const b = this.nodes[j];
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }

    for (const n of this.nodes) {
      ctx.beginPath();
      ctx.arc(n.x, n.y, this.nodeRadius, 0, Math.PI * 2);
      ctx.fillStyle = n === this.dragged ? "#ffd166" : "#e8f1ff";
      ctx.fill();
      ctx.strokeStyle = "#0f1318";
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.fillStyle = "#0f1318";
      ctx.font = "12px sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(String(n.id), n.x, n.y);
    }
  }
}
