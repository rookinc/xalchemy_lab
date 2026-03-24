const svg = document.getElementById("g900-svg");
const modeSelect = document.getElementById("mode");
const resetBtn = document.getElementById("reset-btn");
const captionEl = document.getElementById("caption");
const weightsEl = document.getElementById("weights-readout");

const NS = "http://www.w3.org/2000/svg";

const MODES = {
  coarse: {
    title: "coarse prism",
    caption:
      "G900 descends through an exact weighted triangular prism. The coarse prism law is centered at 145, with top-face edges 140, rung edges 145, and bottom-face edges 150. Under collapse, the two off-center branches recombine to the coarse triangle edge law 290.",
    prismWeights: {
      top: 140,
      rung: 145,
      bottom: 150,
    },
    readout: [
      "coarse prism",
      "  top_face    = 140",
      "  macro_rung  = 145",
      "  bottom_face = 150",
      "",
      "centered form",
      "  140 = 145 - 5",
      "  145 = 145",
      "  150 = 145 + 5",
      "",
      "collapse",
      "  140 + 150 = 290",
      "  290 = 2 * 145",
    ].join("\n"),
  },
  even: {
    title: "even parity prism",
    caption:
      "Even slices preserve the prism support but redistribute weights across it. The currently extracted even-slice kind totals are 160 on the bit-0 face, 240 on the macro rungs, and 320 on the bit-1 face.",
    prismWeights: {
      top: 160,
      rung: 240,
      bottom: 320,
    },
    readout: [
      "even parity prism",
      "  bit0_face   = 160",
      "  macro_rung  = 240",
      "  bit1_face   = 320",
      "",
      "support",
      "  triangular prism",
      "  parity changes weights, not support",
    ].join("\n"),
  },
  odd: {
    title: "odd parity prism",
    caption:
      "Odd slices also preserve the prism support while shifting the weight law. The currently extracted odd-slice kind totals are 260 on the bit-0 face, 195 on the macro rungs, and 130 on the bit-1 face.",
    prismWeights: {
      top: 260,
      rung: 195,
      bottom: 130,
    },
    readout: [
      "odd parity prism",
      "  bit0_face   = 260",
      "  macro_rung  = 195",
      "  bit1_face   = 130",
      "",
      "support",
      "  triangular prism",
      "  parity changes weights, not support",
    ].join("\n"),
  },
  collapse: {
    title: "triangle collapse",
    caption:
      "The prism collapses by identifying paired top and bottom vertices. At coarse level, each triangle edge inherits base candidate 290. The parity refinement gives even triangle edges 160 and odd triangle edges 130.",
    triangleWeights: {
      coarse: 290,
      even: 160,
      odd: 130,
    },
    readout: [
      "triangle collapse",
      "  coarse_edge = 290",
      "  even_edge   = 160",
      "  odd_edge    = 130",
      "",
      "relations",
      "  coarse = even + odd",
      "  290 = 160 + 130",
      "  center = (160 + 130) / 2 = 145",
    ].join("\n"),
  },
};

const GEOM = {
  top: {
    a: [250, 250],
    b: [450, 250],
    c: [350, 120],
  },
  bottom: {
    a: [320, 430],
    b: [520, 430],
    c: [420, 300],
  },
  tri: {
    a: [280, 420],
    b: [560, 420],
    c: [420, 170],
  },
};

function clearSvg() {
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }
}

function el(name, attrs = {}) {
  const node = document.createElementNS(NS, name);
  for (const [key, value] of Object.entries(attrs)) {
    node.setAttribute(key, String(value));
  }
  return node;
}

function line(x1, y1, x2, y2, attrs = {}) {
  return el("line", { x1, y1, x2, y2, ...attrs });
}

function circle(cx, cy, r, attrs = {}) {
  return el("circle", { cx, cy, r, ...attrs });
}

function text(x, y, content, attrs = {}) {
  const t = el("text", { x, y, ...attrs });
  t.textContent = content;
  return t;
}

function rect(x, y, width, height, attrs = {}) {
  return el("rect", { x, y, width, height, ...attrs });
}

function weightLabel(x, y, value, attrs = {}) {
  const g = el("g");
  g.appendChild(
    rect(x - 22, y - 18, 44, 24, {
      rx: 6,
      fill: "#101010",
      stroke: "#555",
      "stroke-width": 1.5,
    }),
  );
  g.appendChild(
    text(x, y, String(value), {
      fill: "#f0f0f0",
      "font-size": 18,
      "font-weight": "700",
      "text-anchor": "middle",
      "dominant-baseline": "middle",
      ...attrs,
    }),
  );
  return g;
}

function midpoint([x1, y1], [x2, y2]) {
  return [(x1 + x2) / 2, (y1 + y2) / 2];
}

function appendFrame() {
  svg.appendChild(
    rect(25, 25, 850, 650, {
      fill: "#000",
      stroke: "#444",
      "stroke-width": 2,
    }),
  );
}

function appendTitle(title) {
  svg.appendChild(
    text(50, 70, title, {
      fill: "#e8e8e8",
      "font-size": 28,
      "font-weight": "700",
    }),
  );
}

function drawNode([x, y], label, fill = "#e8e8e8") {
  svg.appendChild(circle(x, y, 7, { fill, stroke: "#111", "stroke-width": 2 }));
  svg.appendChild(
    text(x + 12, y - 10, label, {
      fill: "#f0f0f0",
      "font-size": 20,
      "font-weight": "600",
    }),
  );
}

function drawPrism(weights, title) {
  clearSvg();
  appendFrame();
  appendTitle(title);

  const ta = GEOM.top.a;
  const tb = GEOM.top.b;
  const tc = GEOM.top.c;

  const ba = GEOM.bottom.a;
  const bb = GEOM.bottom.b;
  const bc = GEOM.bottom.c;

  const edgeStyleTop = { stroke: "#6ca6ff", "stroke-width": 4, "stroke-linecap": "round" };
  const edgeStyleBottom = { stroke: "#7ad97a", "stroke-width": 4, "stroke-linecap": "round" };
  const edgeStyleRung = { stroke: "#f0d36c", "stroke-width": 4, "stroke-linecap": "round" };
  const guideStyle = {
    stroke: "#555",
    "stroke-width": 1.5,
    "stroke-dasharray": "8 8",
    fill: "none",
  };

  svg.appendChild(line(...ta, ...tb, edgeStyleTop));
  svg.appendChild(line(...tb, ...tc, edgeStyleTop));
  svg.appendChild(line(...tc, ...ta, edgeStyleTop));

  svg.appendChild(line(...ba, ...bb, edgeStyleBottom));
  svg.appendChild(line(...bb, ...bc, edgeStyleBottom));
  svg.appendChild(line(...bc, ...ba, edgeStyleBottom));

  svg.appendChild(line(...ta, ...ba, edgeStyleRung));
  svg.appendChild(line(...tb, ...bb, edgeStyleRung));
  svg.appendChild(line(...tc, ...bc, edgeStyleRung));

  svg.appendChild(
    line(ta[0], ta[1], bc[0], bc[1], guideStyle),
  );
  svg.appendChild(
    line(tc[0], tc[1], bb[0], bb[1], guideStyle),
  );

  drawNode(ta, "top_a", "#8ec5ff");
  drawNode(tb, "top_b", "#8ec5ff");
  drawNode(tc, "top_c", "#8ec5ff");

  drawNode(ba, "bottom_a", "#8fe38f");
  drawNode(bb, "bottom_b", "#8fe38f");
  drawNode(bc, "bottom_c", "#8fe38f");

  const topMid = midpoint(ta, tb);
  const topMid2 = midpoint(tb, tc);
  const topMid3 = midpoint(tc, ta);

  const bottomMid = midpoint(ba, bb);
  const bottomMid2 = midpoint(bb, bc);
  const bottomMid3 = midpoint(bc, ba);

  const rungMid1 = midpoint(ta, ba);
  const rungMid2 = midpoint(tb, bb);
  const rungMid3 = midpoint(tc, bc);

  svg.appendChild(weightLabel(topMid[0], topMid[1] - 24, weights.top));
  svg.appendChild(weightLabel(topMid2[0] + 28, topMid2[1], weights.top));
  svg.appendChild(weightLabel(topMid3[0] - 28, topMid3[1], weights.top));

  svg.appendChild(weightLabel(bottomMid[0], bottomMid[1] + 28, weights.bottom));
  svg.appendChild(weightLabel(bottomMid2[0] + 28, bottomMid2[1], weights.bottom));
  svg.appendChild(weightLabel(bottomMid3[0] - 28, bottomMid3[1], weights.bottom));

  svg.appendChild(weightLabel(rungMid1[0] - 30, rungMid1[1], weights.rung));
  svg.appendChild(weightLabel(rungMid2[0] + 30, rungMid2[1], weights.rung));
  svg.appendChild(weightLabel(rungMid3[0], rungMid3[1] - 24, weights.rung));

  svg.appendChild(
    text(60, 620, "top face", {
      fill: "#6ca6ff",
      "font-size": 22,
      "font-weight": "700",
    }),
  );
  svg.appendChild(
    text(220, 620, `= ${weights.top}`, {
      fill: "#f0f0f0",
      "font-size": 22,
    }),
  );
  svg.appendChild(
    text(360, 620, "rungs", {
      fill: "#f0d36c",
      "font-size": 22,
      "font-weight": "700",
    }),
  );
  svg.appendChild(
    text(460, 620, `= ${weights.rung}`, {
      fill: "#f0f0f0",
      "font-size": 22,
    }),
  );
  svg.appendChild(
    text(600, 620, "bottom face", {
      fill: "#7ad97a",
      "font-size": 22,
      "font-weight": "700",
    }),
  );
  svg.appendChild(
    text(790, 620, `= ${weights.bottom}`, {
      fill: "#f0f0f0",
      "font-size": 22,
      "text-anchor": "end",
    }),
  );
}

function drawCollapse(title, weights) {
  clearSvg();
  appendFrame();
  appendTitle(title);

  const a = GEOM.tri.a;
  const b = GEOM.tri.b;
  const c = GEOM.tri.c;

  const edgeStyle = { stroke: "#d7d7a8", "stroke-width": 5, "stroke-linecap": "round" };
  const guideStyle = {
    stroke: "#666",
    "stroke-width": 1.5,
    "stroke-dasharray": "8 8",
  };

  svg.appendChild(line(...a, ...b, edgeStyle));
  svg.appendChild(line(...b, ...c, edgeStyle));
  svg.appendChild(line(...c, ...a, edgeStyle));

  drawNode(a, "A", "#8ec5ff");
  drawNode(b, "B", "#8fe38f");
  drawNode(c, "C", "#ffc6c6");

  const ab = midpoint(a, b);
  const bc = midpoint(b, c);
  const ca = midpoint(c, a);

  svg.appendChild(weightLabel(ab[0], ab[1] + 32, weights.coarse));
  svg.appendChild(weightLabel(bc[0] + 32, bc[1], weights.coarse));
  svg.appendChild(weightLabel(ca[0] - 32, ca[1], weights.coarse));

  svg.appendChild(line(a[0], a[1], a[0], a[1] - 70, guideStyle));
  svg.appendChild(line(b[0], b[1], b[0], b[1] - 70, guideStyle));
  svg.appendChild(line(c[0], c[1], c[0], c[1] - 70, guideStyle));

  svg.appendChild(
    text(70, 540, "coarse", {
      fill: "#f0f0f0",
      "font-size": 22,
      "font-weight": "700",
    }),
  );
  svg.appendChild(
    text(170, 540, `= ${weights.coarse}`, {
      fill: "#f0f0f0",
      "font-size": 22,
    }),
  );
  svg.appendChild(
    text(70, 580, "even", {
      fill: "#f0f0f0",
      "font-size": 22,
      "font-weight": "700",
    }),
  );
  svg.appendChild(
    text(170, 580, `= ${weights.even}`, {
      fill: "#f0f0f0",
      "font-size": 22,
    }),
  );
  svg.appendChild(
    text(70, 620, "odd", {
      fill: "#f0f0f0",
      "font-size": 22,
      "font-weight": "700",
    }),
  );
  svg.appendChild(
    text(170, 620, `= ${weights.odd}`, {
      fill: "#f0f0f0",
      "font-size": 22,
    }),
  );

  svg.appendChild(
    text(430, 580, "290 = 160 + 130", {
      fill: "#f0d36c",
      "font-size": 24,
      "font-weight": "700",
    }),
  );
  svg.appendChild(
    text(430, 620, "center = (160 + 130) / 2 = 145", {
      fill: "#f0d36c",
      "font-size": 24,
      "font-weight": "700",
    }),
  );
}

function render() {
  const mode = modeSelect.value;
  const conf = MODES[mode];

  captionEl.textContent = conf.caption;
  weightsEl.textContent = conf.readout;

  if (mode === "collapse") {
    drawCollapse(conf.title, conf.triangleWeights);
    return;
  }

  drawPrism(conf.prismWeights, conf.title);
}

modeSelect.addEventListener("change", render);
resetBtn.addEventListener("click", () => {
  modeSelect.value = "coarse";
  render();
});

render();
