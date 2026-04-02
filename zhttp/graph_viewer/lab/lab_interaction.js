import {
  setDisplayMode,
  setPauseAt,
  setHz,
  setStatus
} from "../kernel/d4_ui_state.js";
import {
  zoomCamera,
  rotateCamera,
  panCamera,
  stepOrbit,
  applyCameraPreset
} from "../kernel/d4_camera.js";
import {
  sliderPctToAlpha,
  zoomSliderToDistance
} from "./lab_controls.js";
import { startPlayTimer, stopPlayTimer } from "./lab_playback.js";
import { invalidateWitnessCache } from "./lab_witness.js";

function pointerPos(canvas, event) {
  const rect = canvas.getBoundingClientRect();
  return { x: event.clientX - rect.left, y: event.clientY - rect.top };
}

function applyPreset(state, name) {
  if (!name) return;

  if (name === "front") {
    state.ui.camera.projectionMode = "perspective";
    state.ui.camera.panX = 0;
    state.ui.camera.panY = 0;
    state.ui.camera.distance = 15;
    state.ui.camera.yaw = 0;
    state.ui.camera.pitch = 0;
  } else {
    applyCameraPreset(state.ui.camera, name);
  }

  state.ui.display.cameraPreset = name;
  setStatus(state.ui, `camera preset: ${name}`);
}

export function bindLabInteractions(state, draw) {
  const { els, canvas, ui, engine } = state;

  els.displayModeSelect?.addEventListener("change", async () => {
    setDisplayMode(ui, els.displayModeSelect.value);

    if (ui.display.mode === "witness") {
      invalidateWitnessCache(state);
      setStatus(ui, "display mode: witness");
    } else {
      setStatus(ui, `display mode: ${ui.display.mode}`);
    }

    await draw();
  });

  els.pauseAtInput?.addEventListener("change", () => {
    const raw = String(els.pauseAtInput.value ?? "").trim();

    if (!raw) {
      ui.playback.pauseAtD4s = Infinity;
      els.pauseAtInput.placeholder = "off";
      setStatus(ui, "auto-pause off");
    } else {
      setPauseAt(ui, raw);
      setStatus(ui, `pause threshold set to ${ui.playback.pauseAtD4s}`);
    }

    void draw();
  });

  els.hzInput?.addEventListener("change", () => {
    setHz(ui, els.hzInput.value);
    if (ui.playback.isPlaying) startPlayTimer(state, draw);
    setStatus(ui, `rate set to ${ui.playback.hz} hz`);
    void draw();
  });

  els.zoomSlider?.addEventListener("input", () => {
    ui.camera.distance = zoomSliderToDistance(els.zoomSlider.value);
    setStatus(ui, `zoom set to ${ui.camera.distance.toFixed(1)}`);
    void draw();
  });

  els.cameraViewFront?.addEventListener("click", () => {
    applyPreset(state, "front");
    void draw();
  });

  els.cameraViewTop?.addEventListener("click", () => {
    applyPreset(state, "top");
    void draw();
  });

  els.edgeOpacitySlider?.addEventListener("input", () => {
    const alpha = sliderPctToAlpha(els.edgeOpacitySlider.value);
    ui.display.edgeOpacity = alpha;
    ui.display.showEdges = alpha > 0;
    ui.display.showColorEdges = false;
    setStatus(ui, `edge opacity set to ${els.edgeOpacitySlider.value}%`);
    void draw();
  });

  els.spinorOpacitySlider?.addEventListener("input", () => {
    ui.display.spinorOpacity = sliderPctToAlpha(els.spinorOpacitySlider.value);
    ui.display.showSpinors = ui.display.spinorOpacity > 0;
    setStatus(
      ui,
      ui.display.showSpinors
        ? `spinor opacity set to ${els.spinorOpacitySlider.value}%`
        : "spinors hidden"
    );
    void draw();
  });

  els.leftFaceOpacitySlider?.addEventListener("input", () => {
    setStatus(ui, `left opacity set to ${els.leftFaceOpacitySlider.value}%`);
    void draw();
  });

  els.rightFaceOpacitySlider?.addEventListener("input", () => {
    setStatus(ui, `right opacity set to ${els.rightFaceOpacitySlider.value}%`);
    void draw();
  });

  [
    els.toggleGrid,
    els.toggleLabels
  ].forEach((el) => el?.addEventListener("change", () => { void draw(); }));

  els.resetBtn?.addEventListener("click", () => {
    engine.reset();
    state.snapshot = engine.snapshot();
    stopPlayTimer(state);
    setStatus(ui, "reset to seed");
    void draw();
  });

  els.stepBackBtn?.addEventListener("click", () => {
    stopPlayTimer(state);
    engine.reset();
    state.snapshot = engine.snapshot();
    setStatus(ui, "step back not yet implemented");
    void draw();
  });

  els.stepBtn?.addEventListener("click", () => {
    stopPlayTimer(state);
    state.snapshot = engine.step();
    setStatus(ui, "stepped");
    void draw();
  });

  els.playBtn?.addEventListener("click", () => {
    if (ui.playback.isPlaying) {
      stopPlayTimer(state);
      setStatus(ui, "paused");
    } else {
      startPlayTimer(state, draw);
      setStatus(ui, `running at ${ui.playback.hz} hz`);
    }
    void draw();
  });

  canvas.addEventListener("contextmenu", (event) => event.preventDefault());

  canvas.addEventListener("pointerdown", (event) => {
    ui.drag.lastPointer = pointerPos(canvas, event);
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
    const p = pointerPos(canvas, event);
    const dx = p.x - ui.drag.lastPointer.x;
    const dy = p.y - ui.drag.lastPointer.y;
    ui.drag.lastPointer = p;

    if (ui.drag.mode === "rotate") {
      rotateCamera(ui.camera, dx, dy);
    } else {
      panCamera(ui.camera, dx, dy);
    }
    void draw();
  });

  window.addEventListener("pointerup", () => {
    ui.drag.mode = null;
    canvas.classList.remove("rotating");
    canvas.classList.remove("panning");
  });

  canvas.addEventListener(
    "wheel",
    (event) => {
      event.preventDefault();
      zoomCamera(ui.camera, event.deltaY);
      void draw();
    },
    { passive: false }
  );

  window.addEventListener("resize", () => { void draw(); });
}

export function ensureOrbitLoop(state, draw) {
  if (state.orbitFrame !== null) return;

  const loop = () => {
    state.orbitFrame = requestAnimationFrame(loop);
    if (state.ui.camera.orbitEnabled && !state.ui.playback.isPlaying) {
      stepOrbit(state.ui.camera, 0.004);
      void draw();
    }
  };

  state.orbitFrame = requestAnimationFrame(loop);
}

export function applyInitialPreset(state, name = "front") {
  applyPreset(state, name);
}
