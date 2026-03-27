export const STAGES = ["null", "point", "segment", "fork", "triangle", "sheeted closure"];

export const DEFAULT_LAYERS = {
  scaffold: true,
  cells: true,
  nodes: true,
  frontier: true,
  labels: true,
  signs: true,
};

export function makeAppState() {
  return {
    lens: "flat_sheet",
    currentIndex: 0,
    stage: 0,
    ticks: 0,
    completed: {},
    history: ["seed", "stage 0 = null"],
    layers: { ...DEFAULT_LAYERS },
  };
}

export function resetAppState(state) {
  const lens = state.lens;
  const layers = { ...state.layers };
  const fresh = makeAppState();
  fresh.lens = lens;
  fresh.layers = layers;
  return fresh;
}

export function toggleLayer(state, layerName) {
  if (!(layerName in state.layers)) return;
  state.layers[layerName] = !state.layers[layerName];
}
