import { state } from "./kernel/state.js";
import { buildControls } from "./kernel/controls.js";
import { renderScene } from "./kernel/renderer.js";

function init() {
  const app = document.getElementById("app");
  app.innerHTML = `<div id="scene"></div>`;
  buildControls(state, renderScene);
  renderScene(state);
}

init();
