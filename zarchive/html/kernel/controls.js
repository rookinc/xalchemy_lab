export function buildControls(state, renderScene) {
  const app = document.getElementById("app");

  const controls = document.createElement("div");
  controls.id = "controls";

  const row = document.createElement("label");
  row.className = "control-row";

  const label = document.createElement("div");
  label.className = "control-label";
  label.textContent = "T";

  const value = document.createElement("div");
  value.className = "control-value";
  value.id = "T-value";
  value.textContent = String(state.T);

  const input = document.createElement("input");
  input.type = "range";
  input.min = "0";
  input.max = "100";
  input.step = "1";
  input.value = String(state.T);
  input.id = "T";
  input.className = "control-slider";

  row.appendChild(label);
  row.appendChild(value);
  row.appendChild(input);
  controls.appendChild(row);

  const buttonRow = document.createElement("div");
  buttonRow.className = "button-row";

  const playPauseBtn = document.createElement("button");
  playPauseBtn.id = "playPauseBtn";
  playPauseBtn.className = "control-button";
  playPauseBtn.textContent = "Play";

  const resetBtn = document.createElement("button");
  resetBtn.className = "control-button";
  resetBtn.textContent = "Reset";

  function updateControls() {
    input.value = String(state.T);
    value.textContent = String(state.T);
    playPauseBtn.textContent = state.playing ? "Pause" : "Play";
  }

  function tick() {
    state.T = (state.T + state.step) % 101;
    updateControls();
    renderScene(state);
  }

  function startLoop() {
    if (state.timer) return;
    state.playing = true;
    updateControls();
    state.timer = setInterval(tick, 1000 / state.fps);
  }

  function stopLoop() {
    state.playing = false;
    updateControls();
    if (state.timer) {
      clearInterval(state.timer);
      state.timer = null;
    }
  }

  playPauseBtn.addEventListener("click", () => {
    if (state.playing) stopLoop();
    else startLoop();
  });

  resetBtn.addEventListener("click", () => {
    stopLoop();
    state.T = 0;
    updateControls();
    renderScene(state);
  });

  input.addEventListener("input", () => {
    state.T = Number(input.value);
    updateControls();
    renderScene(state);
  });

  buttonRow.appendChild(playPauseBtn);
  buttonRow.appendChild(resetBtn);
  controls.appendChild(buttonRow);
  app.appendChild(controls);

  updateControls();
}
