import { D4GrowthEngine } from "./kernel/d4_growth_engine.js";
import {
  createUIState,
  setDisplayMode,
  setPauseAt,
  setHz
} from "./kernel/d4_ui_state.js";
import { createDefaultCamera } from "./kernel/d4_camera.js";
import { getLabElements } from "./lab/lab_dom.js";
import { draw } from "./lab/lab_render_loop.js";
import {
  bindLabInteractions,
  ensureOrbitLoop,
  applyInitialPreset
} from "./lab/lab_interaction.js";

const engine = new D4GrowthEngine();
const ui = createUIState();
ui.camera = createDefaultCamera();

ui.display.spinorOpacity = 0.28;
ui.display.showSpinors = ui.display.spinorOpacity > 0;
ui.display.showTrurtle = true;
ui.display.showFaces = true;
ui.display.showEdges = true;
ui.display.showColorEdges = true;
ui.display.leftFaceOpacity = 0.8;
ui.display.rightFaceOpacity = 0.8;
ui.display.showAxes = false;
ui.display.cameraPreset = "perspective_default";

const canvas = document.getElementById("stage-canvas");
const ctx = canvas.getContext("2d");
const els = getLabElements();

const state = {
  engine,
  ui,
  canvas,
  ctx,
  els,
  snapshot: engine.snapshot(),
  witnessSnapshot: null,
  witnessCacheKey: null,
  projector: null,
  orbitFrame: null,
  playTimer: null
};

const render = () => draw(state);

bindLabInteractions(state, render);

setDisplayMode(ui, els.displayModeSelect?.value || "prime");

const initialPause = String(els.pauseAtInput?.value ?? "").trim();
if (initialPause) {
  setPauseAt(ui, initialPause);
} else {
  ui.playback.pauseAtD4s = Infinity;
}

setHz(ui, els.hzInput?.value || 30);
applyInitialPreset(state, "front");

void render();
ensureOrbitLoop(state, render);
