import {
  applyLadderDefaults,
  buildUIReadout,
  setStatus,
  stageLabelText
} from "../kernel/d4_ui_state.js";
import {
  resizeCanvasToDisplaySize,
  createProjector,
  clearStage,
  drawStageGrid,
  drawCenterGuides,
  drawStageFrame,
  drawStageLabel
} from "../kernel/d4_projector.js";
import { buildScaffoldPoints, renderScaffold } from "../kernel/d4_render_scaffold.js";
import { renderPrimeScene } from "../kernel/d4_render_prime.js";
import { renderWitnessScene } from "../kernel/d4_render_witness.js";
import {
  syncUIFlags,
  syncZoomSlider,
  syncDisplayModeControl,
  syncCameraViewControls,
  syncPauseAtInput,
  syncSpinorOpacitySlider
} from "./lab_controls.js";
import { ensureWitnessSnapshot } from "./lab_witness.js";

function formatConsole(ui, readout) {
  return [
    `current_d4s      : ${readout.currentD4s}`,
    `turn             : ${readout.turnIndex}`,
    `cells            : ${readout.topology.cells}`,
    `exposed_faces    : ${readout.topology.exposedFaces}`,
    `open_vertices    : ${readout.topology.openVertices}`,
    `phase            : ${readout.cyclePhase}`,
    `residue          : ${readout.cycleResidue}`,
    `increment_target : ${readout.incrementTarget}`,
    `regime           : ${readout.regime}`,
    `rung             : ${readout.rungValue}`,
    `aggregation      : ${readout.display.aggregationMode}`,
    `active_tetra     : ${readout.activeTetraId ?? "-"}`,
    `active_face      : ${readout.activeFaceLabel ?? "-"}`,
    `active_chirality : ${readout.activeChirality ?? "-"}`,
    `spinors          : ${ui.display.showSpinors ? "on" : "off"}`,
    `spinor_opacity   : ${Math.round((ui.display.spinorOpacity ?? 0.28) * 100)}%`,
    `trurtle          : ${ui.display.showTrurtle ? "on" : "off"}`,
    `edges            : ${ui.display.showEdges ? "on" : "off"}`,
    `color_edges      : ${ui.display.showColorEdges ? "on" : "off"}`,
    `left_opacity     : ${Math.round(ui.display.leftFaceOpacity * 100)}%`,
    `right_opacity    : ${Math.round(ui.display.rightFaceOpacity * 100)}%`,
    `camera_distance  : ${readout.camera.distance}`,
    `camera_yaw       : ${readout.camera.yaw}`,
    `camera_pitch     : ${readout.camera.pitch}`,
    `camera_preset    : ${ui.display.cameraPreset}`
  ].join("\n");
}

export function updateReadouts(state) {
  const { ui, snapshot, els } = state;
  const readout = buildUIReadout(ui, snapshot);

  if (els.statusText) els.statusText.textContent = readout.statusText;
  if (els.metricTurn) els.metricTurn.textContent = String(readout.turnIndex);
  if (els.metricCameraDistance) els.metricCameraDistance.textContent = readout.camera.distance;
  if (els.metricCameraYaw) els.metricCameraYaw.textContent = readout.camera.yaw;
  if (els.metricCameraPitch) els.metricCameraPitch.textContent = readout.camera.pitch;

  if (els.metricCurrent) els.metricCurrent.textContent = String(readout.currentD4s);
  if (els.metricCells) els.metricCells.textContent = String(readout.topology.cells);
  if (els.metricFaces) els.metricFaces.textContent = String(readout.topology.exposedFaces);
  if (els.metricOpenVertices) els.metricOpenVertices.textContent = String(readout.topology.openVertices);
  if (els.metricPhase) els.metricPhase.textContent = readout.cyclePhase;
  if (els.metricResidue) els.metricResidue.textContent = String(readout.cycleResidue);
  if (els.metricIncrement) els.metricIncrement.textContent = String(readout.incrementTarget);
  if (els.metricRegime) els.metricRegime.textContent = readout.regime;
  if (els.metricRung) els.metricRung.textContent = String(readout.rungValue);
  if (els.metricAggregation) els.metricAggregation.textContent = readout.display.aggregationMode;
  if (els.metricActiveTetra) els.metricActiveTetra.textContent = readout.activeTetraId ?? "-";
  if (els.metricActiveFace) els.metricActiveFace.textContent = readout.activeFaceLabel ?? "-";
  if (els.metricActiveChirality) els.metricActiveChirality.textContent = readout.activeChirality ?? "-";
  if (els.metricTrurtle) els.metricTrurtle.textContent = ui.display.showTrurtle ? "on" : "off";
  if (els.metricEdges) els.metricEdges.textContent = ui.display.showEdges ? "on" : "off";
  if (els.metricColorEdges) els.metricColorEdges.textContent = ui.display.showColorEdges ? "on" : "off";
  if (els.metricLeftOpacity) els.metricLeftOpacity.textContent = `${Math.round(ui.display.leftFaceOpacity * 100)}%`;
  if (els.metricRightOpacity) els.metricRightOpacity.textContent = `${Math.round(ui.display.rightFaceOpacity * 100)}%`;
  if (els.metricCameraPreset) els.metricCameraPreset.textContent = ui.display.cameraPreset;

  if (els.mobileCurrent) els.mobileCurrent.textContent = String(readout.currentD4s);
  if (els.mobilePhase) els.mobilePhase.textContent = readout.cyclePhase;
  if (els.mobileResidue) els.mobileResidue.textContent = String(readout.cycleResidue);
  if (els.mobileRegime) els.mobileRegime.textContent = readout.regime;
  if (els.mobileActiveTetra) els.mobileActiveTetra.textContent = readout.activeTetraId ?? "-";

  if (els.metricsConsole) {
    els.metricsConsole.textContent = formatConsole(ui, readout);
  }
}

export async function draw(state) {
  const { canvas, ctx, ui } = state;

  resizeCanvasToDisplaySize(canvas, ctx);
  syncUIFlags(ui, state.els);

  applyLadderDefaults(ui, state.snapshot.currentD4s);

  const mode = ui.display.mode;
  ui.camera.projectionMode = mode === "cubic" ? "orthographic" : "perspective";
  state.projector = createProjector(canvas, ui.camera);

  syncZoomSlider(ui, state.els);
  syncDisplayModeControl(ui, state.els);
  syncCameraViewControls(ui, state.els);
  syncPauseAtInput(ui, state.els);
  syncSpinorOpacitySlider(ui, state.els);

  clearStage(ctx, canvas);
  drawStageGrid(ctx, canvas, ui.display.showStageGrid);
  drawCenterGuides(ctx, canvas);

  if (ui.display.mode === "witness") {
    try {
      await ensureWitnessSnapshot(state);
      renderWitnessScene(ctx, canvas, state.witnessSnapshot, {
        showWitnessCycle: ui.witness.showWitnessCycle,
        showActionCell: ui.witness.showActionCell
      });
      setStatus(ui, `witness (${ui.witness.frame},${ui.witness.phase})`);
    } catch (err) {
      console.error(err);
      setStatus(ui, "witness fetch failed");
    }
  } else {
    const spinorPoints = buildScaffoldPoints(state.snapshot.currentD4s);

    if (ui.display.showSpinors) {
      renderScaffold(ctx, spinorPoints, state.projector, {
        showEdges: ui.display.showEdges,
        showColorEdges: ui.display.showColorEdges,
        showLabels: ui.display.showLabels,
        alphaScale: ui.display.spinorOpacity ?? 0.28
      });
    }

    renderPrimeScene(ctx, state.snapshot, state.projector, {
      showFaces: ui.display.showFaces,
      showEdges: ui.display.showEdges,
      showColorEdges: ui.display.showColorEdges,
      showLabels: ui.display.showLabels,
      highlightActive: true,
      leftFaceOpacity: ui.display.leftFaceOpacity,
      rightFaceOpacity: ui.display.rightFaceOpacity
    });
  }

  drawStageFrame(ctx, canvas);
  drawStageLabel(ctx, canvas, stageLabelText(state.snapshot), state.snapshot.currentD4s > 0);
  updateReadouts(state);
}
