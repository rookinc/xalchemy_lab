import { clamp } from "../kernel/d4_camera.js";

export function sliderPctToAlpha(value) {
  return clamp(Number(value) / 100, 0, 1);
}

export function syncUIFlags(ui, els) {
  ui.display.showFaces = els.toggleFaces?.checked ?? true;

  if (els.edgeModeOff?.checked) {
    ui.display.showEdges = false;
    ui.display.showColorEdges = false;
  } else if (els.edgeModeBw?.checked) {
    ui.display.showEdges = true;
    ui.display.showColorEdges = false;
  } else {
    ui.display.showEdges = true;
    ui.display.showColorEdges = true;
  }

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
    els.zoomSlider.value = String(ui.camera.distance);
  }
}

export function syncDisplayModeControl(ui, els) {
  if (els.displayModeSelect) {
    els.displayModeSelect.value = ui.display.mode;
  }
}

export function syncCameraViewControls(ui, els) {
  const preset = ui.display.cameraPreset;
  if (els.cameraViewTop) els.cameraViewTop.checked = preset === "top";
  if (els.cameraViewFront) els.cameraViewFront.checked = preset !== "top";
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
