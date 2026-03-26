const svg = document.getElementById("graphSvg");
const vertexCountInput = document.getElementById("vertexCount");
const grammarSelect = document.getElementById("grammarKey");
const walkerSelect = document.getElementById("walkerKey");
const layoutSelect = document.getElementById("layoutKey");
const generateBtn = document.getElementById("generateBtn");
const animateBtn = document.getElementById("animateBtn");
const resetBtn = document.getElementById("resetBtn");
const logBox = document.getElementById("logBox");
const metaBox = document.getElementById("metaBox");

let currentGraph = null;
let animationTimer = null;

function clearAnimationTimer() {
  if (animationTimer) {
    clearInterval(animationTimer);
    animationTimer = null;
  }
}

async function fetchRegistry() {
  const res = await fetch("/api/extruder/registry");
  if (!res.ok) throw new Error("Failed to load registry.");
  return await res.json();
}

async function fetchGraph(params) {
  const qs = new URLSearchParams(params);
  const res = await fetch(`/api/extruder/generate?${qs.toString()}`);
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || "Failed to generate graph.");
  }
  return await res.json();
}

function fillSelect(select, items) {
  select.innerHTML = "";
  for (const item of items) {
    const opt = document.createElement("option");
    opt.value = item.key;
    opt.textContent = item.label;
    select.appendChild(opt);
  }
}

function resetView() {
  clearAnimationTimer();
  currentGraph = null;
  svg.innerHTML = `
    <text x="420" y="300" class="emptyState">Generate a shape.</text>
  `;
  logBox.innerHTML = "";
  metaBox.textContent = "No graph loaded.";
}

function renderMeta(graph) {
  const meta = graph.meta || {};
  const params = graph.params || {};
  metaBox.textContent =
`graph: ${graph.graph?.label ?? "unknown"}
grammar: ${params.grammar_key ?? "-"}
walker: ${params.walker_key ?? "-"}
layout: ${params.layout_key ?? "-"}
vertices: ${meta.node_count ?? 0}
edges: ${meta.edge_count ?? 0}
steps: ${meta.step_count ?? 0}
closed: ${meta.is_closed ?? false}`;
}

function renderLog(log) {
  logBox.innerHTML = "";
  for (const step of log) {
    const div = document.createElement("div");
    div.className = "logEntry";
    div.dataset.stepIndex = String(step.step_index);

    const rule = step.rule_key || "rule";
    const active = step.active_vertex || "-";
    const note = step.note || "";

    div.innerHTML = `
      <div class="logStep">step ${step.step_index}</div>
      <div class="logRule">${rule} · active ${active}</div>
      <div class="logNote">${note}</div>
    `;
    logBox.appendChild(div);
  }
}

function edgeMap(graph) {
  const m = new Map();
  for (const edge of graph.edges) {
    const forward = `${edge.source}->${edge.target}`;
    const reverse = `${edge.target}->${edge.source}`;
    m.set(forward, edge.id);
    m.set(reverse, edge.id);
  }
  return m;
}

function renderGraph(graph, highlightedEdgeIds = new Set(), highlightedNodeIds = new Set()) {
  svg.innerHTML = "";

  const edgeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
  const nodeLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
  svg.appendChild(edgeLayer);
  svg.appendChild(nodeLayer);

  const nodeById = new Map(graph.nodes.map((n) => [n.id, n]));

  for (const edge of graph.edges) {
    const a = nodeById.get(edge.source);
    const b = nodeById.get(edge.target);
    if (!a || !b) continue;

    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", a.x);
    line.setAttribute("y1", a.y);
    line.setAttribute("x2", b.x);
    line.setAttribute("y2", b.y);
    line.setAttribute("class", highlightedEdgeIds.has(edge.id) ? "edge active" : "edge");
    edgeLayer.appendChild(line);
  }

  for (const node of graph.nodes) {
    const group = document.createElementNS("http://www.w3.org/2000/svg", "g");

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", node.x);
    circle.setAttribute("cy", node.y);
    circle.setAttribute("r", 18);
    circle.setAttribute("class", highlightedNodeIds.has(node.id) ? "node active" : "node");

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", node.x);
    text.setAttribute("y", node.y);
    text.setAttribute("class", "nodeLabel");
    text.textContent = node.label;

    group.appendChild(circle);
    group.appendChild(text);
    nodeLayer.appendChild(group);
  }
}

function markActiveLog(stepIndex) {
  for (const el of logBox.querySelectorAll(".logEntry")) {
    el.classList.toggle("active", Number(el.dataset.stepIndex) === stepIndex);
  }
}

function replayDerivation(graph) {
  clearAnimationTimer();
  if (!graph?.derivation_log?.length) return;

  const eMap = edgeMap(graph);
  let idx = -1;

  animationTimer = setInterval(() => {
    idx += 1;
    if (idx >= graph.derivation_log.length) {
      clearAnimationTimer();
      renderGraph(graph);
      markActiveLog(-1);
      return;
    }

    const step = graph.derivation_log[idx];
    const highlightedEdgeIds = new Set();
    const highlightedNodeIds = new Set();

    const addedEdges = step.added_edges || [];
    for (const raw of addedEdges) {
      const id = eMap.get(raw);
      if (id) highlightedEdgeIds.add(id);
    }

    if (step.active_vertex) {
      highlightedNodeIds.add(step.active_vertex);
    }

    renderGraph(graph, highlightedEdgeIds, highlightedNodeIds);
    markActiveLog(step.step_index);
  }, 550);
}

async function generate() {
  clearAnimationTimer();

  const params = {
    vertex_count: vertexCountInput.value || "10",
    grammar_key: grammarSelect.value || "cycle",
    walker_key: walkerSelect.value || "sequential",
    layout_key: layoutSelect.value || "circle",
  };

  generateBtn.disabled = true;
  generateBtn.textContent = "Generating...";
  try {
    const graph = await fetchGraph(params);
    currentGraph = graph;
    renderGraph(graph);
    renderLog(graph.derivation_log || []);
    renderMeta(graph);
  } catch (err) {
    resetView();
    metaBox.textContent = String(err);
  } finally {
    generateBtn.disabled = false;
    generateBtn.textContent = "Generate";
  }
}

async function init() {
  resetView();
  const registry = await fetchRegistry();
  fillSelect(grammarSelect, registry.grammars || []);
  fillSelect(walkerSelect, registry.walkers || []);
  fillSelect(layoutSelect, registry.layouts || []);

  grammarSelect.value = "cycle";
  walkerSelect.value = "sequential";
  layoutSelect.value = "circle";

  generateBtn.addEventListener("click", generate);
  animateBtn.addEventListener("click", () => {
    if (currentGraph) replayDerivation(currentGraph);
  });
  resetBtn.addEventListener("click", resetView);
}

init().catch((err) => {
  metaBox.textContent = `Init failed: ${err}`;
});
