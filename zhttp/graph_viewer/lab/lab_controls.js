import { clamp } from "../kernel/d4_camera.js";

const ZOOM_MIN_DISTANCE = 4.5;
const ZOOM_MAX_DISTANCE = 60;

export function sliderPctToAlpha(value) {
  return clamp(Number(value) / 100, 0, 1);
}

export function zoomSliderToDistance(value) {
  const t = clamp(Number(value) / 100, 0, 1);
  return ZOOM_MAX_DISTANCE - t * (ZOOM_MAX_DISTANCE - ZOOM_MIN_DISTANCE);
}

export function distanceToZoomSlider(distance) {
  const d = clamp(Number(distance), ZOOM_MIN_DISTANCE, ZOOM_MAX_DISTANCE);
  const t = (ZOOM_MAX_DISTANCE - d) / (ZOOM_MAX_DISTANCE - ZOOM_MIN_DISTANCE);
  return Math.round(t * 100);
}

export function syncUIFlags(ui, els) {
  ui.display.showFaces = true;
  ui.display.edgeOpacity = sliderPctToAlpha(els.edgeOpacitySlider?.value ?? 100);
  ui.display.showEdges = ui.display.edgeOpacity > 0;
  ui.display.showColorEdges = false;

  ui.display.showTrurtle = true;
  ui.display.showSpinors = sliderPctToAlpha(els.spinorOpacitySlider?.value ?? 28) > 0;
  ui.display.showLabels = els.toggleLabels?.checked ?? false;
  ui.display.showStageGrid = els.toggleGrid?.checked ?? true;
  ui.display.showAxes = false;
  ui.display.spinorOpacity = sliderPctToAlpha(els.spinorOpacitySlider?.value ?? 28);
  ui.display.leftFaceOpacity = sliderPctToAlpha(els.leftFaceOpacitySlider?.value ?? 80);
  ui.display.rightFaceOpacity = sliderPctToAlpha(els.rightFaceOpacitySlider?.value ?? 80);
}

export function syncZoomSlider(ui, els) {
  if (els.zoomSlider) {
    els.zoomSlider.value = String(distanceToZoomSlider(ui.camera.distance));
  }
}

export function syncDisplayModeControl(ui, els) {
  if (els.displayModeSelect) {
    els.displayModeSelect.value = ui.display.mode;
  }
}

export function syncCameraViewControls(ui, els) {
  const preset = ui.display.cameraPreset;
  const isTop = preset === "top";

  if (els.cameraViewTop) {
    els.cameraViewTop.classList.toggle("is-active", isTop);
  }

  if (els.cameraViewFront) {
    els.cameraViewFront.classList.toggle("is-active", !isTop);
  }
}

export function syncPauseAtInput(ui, els) {
  if (!els.pauseAtInput) return;
  if (Number.isFinite(ui.playback.pauseAtD4s) && ui.playback.pauseAtD4s > 0) {
    els.pauseAtInput.value = String(ui.playback.pauseAtD4s);
    els.pauseAtInput.placeholder = "";
  } else {
    els.pauseAtInput.value = "";
    els.pauseAtInput.placeholder = "off";
  }
}

export function syncSpinorOpacitySlider(ui, els) {
  if (!els.spinorOpacitySlider) return;
  els.spinorOpacitySlider.value = String(Math.round((ui.display.spinorOpacity ?? 0.28) * 100));
}

export function syncEdgeOpacitySlider(ui, els) {
  if (!els.edgeOpacitySlider) return;
  els.edgeOpacitySlider.value = String(Math.round((ui.display.edgeOpacity ?? 1) * 100));
}
