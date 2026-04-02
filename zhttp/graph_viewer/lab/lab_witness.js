export async function fetchWitnessState(frame, phase, scale = 1) {
  const res = await fetch(`/api/witness/state?frame=${frame}&phase=${phase}&r=${scale}`);
  if (!res.ok) {
    throw new Error(`witness fetch failed: ${res.status}`);
  }
  const data = await res.json();
  return data.payload;
}

export async function ensureWitnessSnapshot(state) {
  const key = `${state.ui.witness.frame}:${state.ui.witness.phase}:${state.ui.witness.scale}`;
  if (state.witnessSnapshot && state.witnessCacheKey === key) return;

  state.witnessSnapshot = await fetchWitnessState(
    state.ui.witness.frame,
    state.ui.witness.phase,
    state.ui.witness.scale
  );
  state.witnessCacheKey = key;
}

export function invalidateWitnessCache(state) {
  state.witnessSnapshot = null;
  state.witnessCacheKey = null;
}
