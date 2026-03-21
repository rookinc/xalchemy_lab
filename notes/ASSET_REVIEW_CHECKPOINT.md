# Asset Review Checkpoint

## Status

This note records the current asset base of the project after the local state-space, automaton, sheet renderer, DXF export, packaging, and CLI milestones.

It is a checkpoint note, not a final paper claim.

---

## 1. Formal assets

These are the strongest current theory objects.

### Canonical local state register
- local state register: `(A, sigma, tau)`

### Realized local state space
- full realized 3-bit cube:
  - `000`
  - `001`
  - `010`
  - `011`
  - `100`
  - `101`
  - `110`
  - `111`

### Anchored chart split
- `A = 0` chart = odd/E1 anchored chart
- `A = 1` chart = E2-dominant anchored chart

### Canonical local readout objects
- anchored receipt law
- rigid distal backbone
- quotient bridge signature
- canonical local state-space spec

### Strongest formal result
- Toy G60 Automaton v2 matches the full realized local cube exactly.

---

## 2. Validation assets

These are the objects that validate the local formal story.

### Trace and sector assets
- trace catalogs by state
- trace class catalog
- trace-to-invariant descent table
- refined sector trace probes
- exception probe
- parity probe

### State machine assets
- local trace state machine delta table
- anchored control grammar inference
- chart split evidence

### Automaton validation
- Toy G60 Automaton v1
- Toy G60 Automaton v2
- comparison against measured local cube
- comparison against full realized cube
- full 120/120 pass for v2

### Bridge / signed-lift / cocycle assets
- bridge alias resolution
- signed-lift source and validator
- signed-lift bridge loops
- resolved cocycle artifact path
- tree gauge artifacts
- bridge phase portrait and related JSON outputs

### Tri-patch experimental lane
- holonomy probes
- lift-bit probes
- stress / burden / route / lock probes
- tri-patch comparison and defect experiments

These remain preserved as paper-supporting reproducibility artifacts.

---

## 3. Visualization assets

These are the current inspection surfaces.

### Cube view
- single semantic cube SVG exporter
- single semantic cube PNG exporter
- state cube gallery
- cube contact sheet

### Unfolded sheet view
- unfolded triangular state-sheet SVG exporter
- unfolded triangular state-sheet PNG exporter
- unfolded triangular state-sheet DXF exporter

### Current strongest visual diagnostic
- unfolded black/white triangular state sheet

This is currently the clearest diagnostic rendering of the local state law.

---

## 4. Packaging and app assets

These are the project-operational assets.

### Package / install
- `pyproject.toml`
- editable install working
- package import path healthy

### CLI
- Python CLI entrypoint
- installed console script:
  - `summon`

### Config
- TOML config introduced
- config directory established

### App lane
- `src/xalchemy_lab/app`
- app scripts separated from paper scripts

These assets convert the project from script pile to functioning toolchain.

---

## 5. Provenance assets

These are the historical and paper-trail objects.

### Notes
- theorem notes
- proposition notes
- checkpoint notes
- working-principle notes
- interface and roadmap notes

### JSON artifacts
- `specs/paper/bridge`
- `specs/paper/g60`

### Tracked renders
- state galleries
- contact sheets
- state sheet exports
- DXF outputs
- single cube exports

### Tags
- `g60-local-automaton-v2`
- `canonical-state-space-v1`

These form the provenance and publication backbone.

---

## 6. Structural repo assets

The repo layout is now itself an asset.

### App lane
- `src/xalchemy_lab/app`
- `specs/app`

### Paper lane
- `src/xalchemy_lab/paper/bridge`
- `src/xalchemy_lab/paper/tri_patch`
- `specs/paper/bridge`
- `specs/paper/g60`

### True shared/core objects
- `tri_patch_core.py`
- `tri_turtle_core.py`
- `shared/`

This structure now supports both active building and paper preservation.

---

## 7. Highest-value unlocked assets

If compressed to the strongest current assets, they are:

1. canonical local state-space spec
2. validated local automaton
3. visual receipt model
4. reproducible artifact trail
5. functioning CLI + package toolchain

These five together represent the main checkpoint gain.

---

## 8. Assets not yet unlocked

The following are still open:

- a global G60 derivation
- a canonical global gluing law
- a geometric derivation of the chart split
- a final publication-grade visual plate
- a fully TOML-driven renderer pipeline
- a more intrinsic geometric principle replacing charted local rules

So the project is currently strongest in:
- local law
- validation
- projection
- tooling

and still open in:
- global geometry
- intrinsic derivation
- final presentation

---

## 9. Strongest current summary sentence

The project now possesses a canonical local state-space, a validated local automaton, a readable visual receipt model, a preserved reproducibility trail, and a working command-line toolchain for rendering and exporting the local law.

