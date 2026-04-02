import { setStatus } from "../kernel/d4_ui_state.js";

export function stopPlayTimer(state) {
  if (state.playTimer !== null) {
    clearInterval(state.playTimer);
    state.playTimer = null;
  }
  state.ui.playback.isPlaying = false;
  if (state.els.playBtn) state.els.playBtn.textContent = "▶";
}

export function startPlayTimer(state, draw) {
  stopPlayTimer(state);
  state.ui.playback.isPlaying = true;
  if (state.els.playBtn) state.els.playBtn.textContent = "❚❚";

  const delay = Math.max(16, Math.round(1000 / Math.max(1, state.ui.playback.hz)));
  state.playTimer = setInterval(() => {
    state.snapshot = state.engine.step();

    if (
      Number.isFinite(state.ui.playback.pauseAtD4s) &&
      state.ui.playback.pauseAtD4s > 0 &&
      state.snapshot.currentD4s >= state.ui.playback.pauseAtD4s
    ) {
      const hit = state.ui.playback.pauseAtD4s;
      stopPlayTimer(state);
      state.ui.playback.pauseAtD4s = Infinity;

      if (state.els.pauseAtInput) {
        state.els.pauseAtInput.value = "";
        state.els.pauseAtInput.placeholder = "off";
      }

      setStatus(state.ui, `auto-paused at ${state.snapshot.currentD4s}; threshold ${hit} cleared`);
      void draw();
      return;
    }

    void draw();
  }, delay);
}
