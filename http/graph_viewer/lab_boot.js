import { D4GrowthEngine } from "./kernel/d4_growth_engine.js";
import {
  createUIState,
  setDisplayMode,
  setPauseAt,
  setHz,
  setStatus,
  applyLadderDefaults,
  buildUIReadout,
  stageLabelText,
  cameraReadoutText
} from "./kernel/d4_ui_state.js";
import {
  createDefaultCamera,
  zoomCamera,
  rotateCamera,
  panCamera,
  toggleOrbit,
  stepOrbit,
  applyCameraPreset,
  clamp
} from "./kernel/d4_camera.js";
import {
  resizeCanvasToDisplaySize,
  createProjector,
  clearStage,
  drawStageGrid,
  drawCenterGuides,
  drawStageFrame,
  drawStageLabel,
  drawTopRightReadout
} from "./kernel/d4_projector.js";
import { buildScaffoldPoints, renderScaffold } from "./kernel/d4_render_scaffold.js";
import { renderPrimeScene } from "./kernel/d4_render_prime.js";
import { renderCompositeOverlay } from "./kernel/d4_render_composite.js";

const engine = new D4GrowthEngine();
const ui = createUIState();
ui.camera = createDefaultCamera();

const canvas = document.getElementById("stage-canvas");
const ctx = canvas.getContext("2d");

const els = {
  homeBtn: document.getElementById("home-btn"),
  toggleGrid: document.getElementById("toggle-grid"),
  toggleFaces: document.getElementById("toggle-faces"),
  toggleLabels: document.getElementById("toggle-labels"),
  displayModeSelect: document.getElementById("display-mode-select"),
  pauseAtInput: document.getElementById("pause-at-input"),
  hzSelect: document.getElementById("hz-select"),
  zoomSlider: document.getElementById("zoom-slider"),
  orbitBtn: document.getElementById("orbit-btn"),
  resetBtn: document.getElementById("reset-btn"),
  stepBtn: document.getElementById("step-btn"),
  playBtn: document.getElementById("play-btn"),
  presetJunctionBtn: document.getElementById("preset-junction-btn"),
  presetTopBtn: document.getElementById("preset-top-btn"),
  statusText: document.getElementById("status-text"),
  currentReadout: document.getElementById("current-readout"),
  residueReadout: document.getElementById("residue-readout"),
  metricCurrent: document.getElementById("metric-current"),
  metricTurn: document.getElementById("metric-turn"),
  metricCells: document.getElementById("metric-cells"),
  metricFaces: document.getElementById("metric-faces"),
  metricOpenVertices: document.getElementById("metric-open-vertices"),
  metricPhase: document.getElementById("metric-phase"),
  metricResidue: document.getElementById("metric-residue"),
  metricIncrement: document.getElementById("metric-increment"),
  metricRegime: document.getElementById("metric-regime"),
  metricRung: document.getElementById("metric-rung"),
  metricAggregation: document.getElementById("metric-aggregation"),
  metricActiveTetra: document.getElementById("metric-active-tetra"),
  metricActiveFace: document.getElementById("metric-active-face"),
  metricActiveChirality: document.getElementById("metric-active-chirality"),
  metricCameraDistance: document.getElementById("metric-camera-distance"),
  metricCameraYaw: document.getElementById("metric-camera-yaw"),
  metricCameraPitch: document.getElementById("metric-camera-pitch"),
  metricCameraPreset: document.getElementById("metric-camera-preset"),
  mobileCurrent: document.getElementById("mobile-current"),
  mobileTurn: document.getElementById("mobile-turn"),
  mobilePhase: document.getElementById("mobile-phase"),
  mobileResidue: document.getElementById("mobile-residue"),
  mobileRegime: document.getElementById("mobile-regime"),
  mobileActiveTetra: document.getElementById("mobile-active-tetra")
};

let snapshot = engine.snapshot();
let projector = createProjector(canvas, ui.camera);
let orbitFrame = null;
let playTimer = null;

function syncUIFlags() {
  ui.display.showStageGrid = els.toggleGrid.checked;
  ui.display.showFaces = els.toggleFaces.checked;
  ui.display.showLabels = els.toggleLabels.checked;
}

function syncZoomSlider() {
  els.zoomSlider.value = String(ui.camera.distance);
}

function updateReadouts() {
  const readout = buildUIReadout(ui, snapshot);

  els.statusText.textContent = readout.statusText;
  els.currentReadout.textContent = String(readout.currentD4s);
  els.residueReadout.textContent = String(readout.cycleResidue);

  els.metricCurrent.textContent = String(readout.currentD4s);
  els.metricTurn.textContent = String(readout.turnIndex);
  els.metricCells.textContent = String(readout.topology.cells);
  els.metricFaces.textContent = String(readout.topology.exposedFaces);
  els.metricOpenVertices.textContent = String(readout.topology.openVertices);

  els.metricPhase.textContent = readout.cyclePhase;
  els.metricResidue.textContent = String(readout.cycleResidue);
  els.metricIncrement.textContent = String(readout.incrementTarget);

  els.metricRegime.textContent = readout.regime;
  els.metricRung.textContent = String(readout.rungValue);
  els.metricAggregation.textContent = readout.display.aggregationMode;

  els.metricActiveTetra.textContent = readout.activeTetraId ?? "-";
  els.metricActiveFace.textContent = readout.activeFaceLabel ?? "-";
  els.metricActiveChirality.textContent = readout.activeChirality ?? "-";

  els.metricCameraDistance.textContent = readout.camera.distance;
  els.metricCameraYaw.textContent = readout.camera.yaw;
  els.metricCameraPitch.textContent = readout.camera.pitch;
  els.metricCameraPreset.textContent = ui.display.cameraPreset;

  els.mobileCurrent.textContent = String(readout.currentD4s);
  els.mobileTurn.textContent = String(readout.turnIndex);
  els.mobilePhase.textContent = readout.cyclePhase;
  els.mobileResidue.textContent = String(readout.cycleResidue);
  els.mobileRegime.textContent = readout.regime;
  els.mobileActiveTetra.textContent = readout.activeTetraId ?? "-";
}

function draw() {
  resizeCanvasToDisplaySize(canvas, ctx);
  projector = createProjector(canvas, ui.camera);
  syncUIFlags();
  syncZoomSlider();

  clearStage(ctx, canvas);
  drawStageGrid(ctx, canvas, ui.display.showStageGrid);
  drawCenterGuides(ctx, canvas);

  applyLadderDefaults(ui, snapshot.currentD4s);

  const mode = ui.display.mode;
  const scaffoldPoints = buildScaffoldPoints(snapshot.currentD4s);

  if (mode === "scaffold" || mode === "hybrid") {
    renderScaffold(ctx, scaffoldPoints, projector, {
      showFaces: ui.display.showFaces,
      showLabels: ui.display.showLabels,
      alphaScale: mode === "hybrid" ? 0.34 : 1
    });
  }

  if (mode === "prime" || mode === "prime_plus_composite" || mode === "hybrid") {
    renderPrimeScene(ctx, snapshot, projector, {
      showFaces: ui.display.showFaces,
      showLabels: ui.display.showLabels,
      highlightActive: true
    });
  }

  if (mode === "prime_plus_composite" || mode === "hybrid") {
    renderCompositeOverlay(ctx, snapshot, projector, {
      showLabels: ui.display.showLabels,
      activeOnly: true
    });
  }

  drawStageFrame(ctx, canvas);
  drawStageLabel(ctx, canvas, stageLabelText(snapshot), snapshot.currentD4s > 0);
  drawTopRightReadout(ctx, canvas, cameraReadoutText(ui));
  updateReadouts();
}

function stopPlayTimer() {
  if (playTimer !== null) {
    clearInterval(playTimer);
    playTimer = null;
  }
  ui.playback.isPlaying = false;
  els.playBtn.textContent = "▶";
}

function startPlayTimer() {
  stopPlayTimer();
  ui.playback.isPlaying = true;
  els.playBtn.textContent = "❚❚";
  const delay = Math.max(16, Math.round(1000 / Math.max(1, ui.playback.hz)));
  playTimer = setInterval(() => {
    snapshot = engine.step();
    if (snapshot.currentD4s >= ui.playback.pauseAtD4s) {
      stopPlayTimer();
      setStatus(ui, `auto-paused at ${snapshot.currentD4s}`);
    }
    draw();
  }, delay);
}

function ensureOrbitLoop() {
  if (orbitFrame !== null) return;
  const loop = () => {
    orbitFrame = requestAnimationFrame(loop);
    if (ui.camera.orbitEnabled && !ui.playback.isPlaying) {
      stepOrbit(ui.camera, 0.004);
      draw();
    }
  };
  orbitFrame = requestAnimationFrame(loop);
}

function pointerPos(event) {
  const rect = canvas.getBoundingClientRect();
  return { x: event.clientX - rect.left, y: event.clientY - rect.top };
}

els.homeBtn.addEventListener("click", () => {
  window.location.href = "/";
});

els.displayModeSelect.addEventListener("change", () => {
  setDisplayMode(ui, els.displayModeSelect.value);
  setStatus(ui, `display mode: ${ui.display.mode}`);
  draw();
});

els.pauseAtInput.addEventListener("change", () => {
  setPauseAt(ui, els.pauseAtInput.value);
  setStatus(ui, `pause threshold set to ${ui.playback.pauseAtD4s}`);
  draw();
});

els.hzSelect.addEventListener("change", () => {
  setHz(ui, els.hzSelect.value);
  if (ui.playback.isPlaying) startPlayTimer();
  setStatus(ui, `rate set to ${ui.playback.hz} hz`);
  draw();
});

els.zoomSlider.addEventListener("input", () => {
  ui.camera.distance = clamp(Number(els.zoomSlider.value), 4.5, 60);
  setStatus(ui, `zoom set to ${ui.camera.distance.toFixed(1)}`);
  draw();
});

els.toggleGrid.addEventListener("change", draw);
els.toggleFaces.addEventListener("change", draw);
els.toggleLabels.addEventListener("change", draw);

els.orbitBtn.addEventListener("click", () => {
  const enabled = toggleOrbit(ui.camera);
  setStatus(ui, enabled ? "orbit on" : "orbit off");
  draw();
});

els.resetBtn.addEventListener("click", () => {
  engine.reset();
  snapshot = engine.snapshot();
  stopPlayTimer();
  setStatus(ui, "reset to seed");
  draw();
});

els.stepBtn.addEventListener("click", () => {
  stopPlayTimer();
  snapshot = engine.step();
  setStatus(ui, "stepped");
  draw();
});

els.playBtn.addEventListener("click", () => {
  if (ui.playback.isPlaying) {
    stopPlayTimer();
    setStatus(ui, "paused");
  } else {
    startPlayTimer();
    setStatus(ui, `running at ${ui.playback.hz} hz`);
  }
  draw();
});

els.presetJunctionBtn.addEventListener("click", () => {
  applyCameraPreset(ui.camera, "junction");
  ui.display.cameraPreset = "junction";
  setStatus(ui, "camera preset: junction");
  draw();
});

els.presetTopBtn.addEventListener("click", () => {
  applyCameraPreset(ui.camera, "top");
  ui.display.cameraPreset = "top";
  setStatus(ui, "camera preset: top");
  draw();
});

canvas.addEventListener("contextmenu", (event) => event.preventDefault());

canvas.addEventListener("pointerdown", (event) => {
  ui.drag.lastPointer = pointerPos(event);
  if (event.button === 2 || event.shiftKey) {
    ui.drag.mode = "pan";
    canvas.classList.remove("rotating");
    canvas.classList.add("panning");
  } else {
    ui.drag.mode = "rotate";
    canvas.classList.add("rotating");
    canvas.classList.remove("panning");
  }
});

window.addEventListener("pointermove", (event) => {
  if (!ui.drag.mode) return;
  const p = pointerPos(event);
  const dx = p.x - ui.drag.lastPointer.x;
  const dy = p.y - ui.drag.lastPointer.y;
  ui.drag.lastPointer = p;

  if (ui.drag.mode === "rotate") {
    rotateCamera(ui.camera, dx, dy);
  } else {
    panCamera(ui.camera, dx, dy);
  }
  draw();
});

window.addEventListener("pointerup", () => {
  ui.drag.mode = null;
  canvas.classList.remove("rotating");
  canvas.classList.remove("panning");
});

canvas.addEventListener("wheel", (event) => {
  event.preventDefault();
  zoomCamera(ui.camera, event.deltaY);
  draw();
}, { passive: false });

window.addEventListener("resize", draw);

setDisplayMode(ui, "prime");
syncZoomSlider();
draw();
ensureOrbitLoop();
