# http

Browser sandbox for the local xyzti renderer.

This directory is intentionally small and modular. It is the browser-facing workspace for experimenting with local geometric / transport visualizations without entangling them with the heavier Python research machinery in `src/`, `specs/`, and `notes/`.

## Purpose

Right now, `http/` is not a full proof renderer for the Thalean / dodecahedral transport program.

It is a local conceptual renderer used to explore and communicate a constrained xyzti frame:

- a common origin `0`
- `z` fixed on the positive axis
- `I` fixed on the negative axis
- `x` and `y` spreading symmetrically from center
- `r` as a continuation ray at 45 degrees
- `T` as the single loop parameter

The point of this workspace is to keep a lightweight visual kernel separate from specific constructions so the browser code can evolve cleanly from:

1. local sketches
2. admissible-action toys
3. finite construction demos
4. more faithful renderings of the underlying transport theory

## Current status

The current renderer is law-shaped but not theorem-complete.

It demonstrates:

- a constrained local frame
- a single-parameter animated loop
- separation between reusable rendering utilities and construction-specific logic

It does not yet implement the finite combinatorial transport construction from the paper-level theory. In particular, it is not yet a renderer for:

- flag/chamber state systems
- explicit admissible move generators
- quotient descent `G60 -> G30 -> G15`
- sector incidence or overlap operators

So the current app should be understood as a conceptual kernel, not the finished construction engine.

## Directory layout

    http/
      README.md
      index.html
      styles.css
      app.js
      kernel/
        controls.js
        geometry.js
        renderer.js
        state.js
        svg.js
      constructions/
        xyzti.js

## Design split

### `index.html`
Very thin page shell.

Responsibilities:

- load styles
- provide the root mount node
- load the browser app entrypoint

### `app.js`
Boot file only.

Responsibilities:

- initialize the app
- mount controls
- invoke the renderer

### `kernel/`
Reusable browser-side rendering support.

#### `kernel/state.js`
Shared app state.

Contains:

- canvas dimensions
- origin
- animation parameter `T`
- color palette
- loop timing

#### `kernel/svg.js`
Low-level SVG helpers.

Contains simple primitives such as:

- `svgEl`
- `line`
- `circle`
- `text`
- `poly`

This should stay generic and construction-agnostic.

#### `kernel/geometry.js`
Small geometric utilities.

Contains operations like:

- polar coordinate placement
- Euclidean distance

This is generic math support, not theory-specific logic.

#### `kernel/renderer.js`
Scene assembly and drawing.

Responsibilities:

- clear and rebuild the SVG scene
- draw common frame elements
- draw the current construction instance
- render labels and overlays

This should depend on construction outputs, not hard-code theory details directly.

#### `kernel/controls.js`
UI controls and animation loop.

Responsibilities:

- slider setup
- play / pause
- reset
- animation timing for `T`

This should remain generic enough to drive other constructions later.

### `constructions/`
Construction-specific logic.

#### `constructions/xyzti.js`
Current local xyzti construction.

Responsibilities:

- derive geometry from the shared state
- define how `T` affects the local frame
- compute construction-specific radii / points / relations

This is where interpretation lives.
The renderer should draw what this module provides.

## Current visual grammar

The current xyzti construction uses the following reading:

- `0` : common origin
- `z` : positive axis witness
- `I` : negative axis counterpart
- `x`, `y` : symmetric spread from center
- `r` : continuation ray at 45 degrees
- `T` : loop parameter

The visible circles are treated as the loop itself, not as a separate timeline or witness axis.

That means older notions like a vertical `t` axis are currently suppressed in favor of a cleaner loop-centric reading.

## Why keep kernel and constructions separate?

Because the repo is already carrying multiple layers of work:

- Python search / derivation code
- specs and notes for G60 / G15
- renderer experiments
- conceptual local grammars

If the browser code stays monolithic, every new experiment will turn `app.js` into a junk drawer.

This split lets us preserve a stable rendering kernel while swapping in new constructions, such as:

- `constructions/flags.js`
- `constructions/chambers.js`
- `constructions/g60.js`
- `constructions/g15.js`

later.

## Development

From the repo root:

    cd http
    python -m http.server 8000

Then open:

    http://127.0.0.1:8000

If the server is already running, most edits only require a browser refresh.

## Current workflow

Typical loop:

1. edit files under `http/`
2. refresh browser
3. inspect whether the visual grammar matches the intended local law
4. refine construction logic first, styling second

The goal is to discover the right constraints, not merely produce nice pictures.

## Near-term direction

Likely next steps for this workspace:

- refine admissibility so fewer free geometric choices remain
- introduce discrete state-driven construction modes
- add alternate construction modules beside `xyzti`
- connect the browser renderer more explicitly to artifacts from `specs/paper/g60/`
- eventually test whether a finite move engine can be rendered here cleanly

## Guiding principle

No free geometry without lawful cause.

The browser layer should become a visual interpreter of constrained constructions, not a loose sketch pad.
