# Relabeled Packet-Through-Cell Lens Sketch

## Purpose

This note reinterprets the old cube sketch as a packet-through-cell projection lens.

The old labels are treated as placeholders.
The cube is now read as a finite carrier cell that receives a unit packet, applies a local controller, and projects weighted receipts onto cube faces.

---

## Core picture

\[
\text{unit packet}
\;\longrightarrow\;
\text{chambered controller}
\;\longrightarrow\;
\text{face-weighted receipts}
\]

This is the smallest conceptual form of:

\[
G15 \;\to\; G30 \;\to\; \mathrm{Faces}(G60).
\]

---

## Relabeling of the sketch

### Cube
Interpret the cube as a **local carrier cell** or **minimal chamber packet**.

Suggested label:
- `carrier cell`
or
- `local chamber cell`

### Side length
The marked side length becomes:

- `cell scale = l_planck`

This does not yet claim final physics.
It says only that the cell is being treated as a finite minimal carrier.

### Bottom input arrow
The bottom arrow labeled `1` becomes:

- `unit packet insertion`
or
- `unit activation`

Meaning:
a single local packet is injected into the carrier cell.

### Top bifurcation arrows
The two top arrows labeled `0 or 1` become:

- `controller readout L`
- `controller readout R`

or more structurally:

- `anchored control branch 1`
- `anchored control branch 2`

Meaning:
the packet encounters a local bifurcation/controller at the anchor.

### Face fractions
The face labels like `f 1/4`, `f 3/4`, `f 4/4` become:

- `projected face weight`
- `face occupancy coefficient`
- `local receipt fraction`

Meaning:
these are not yet final constants.
They are the relative projection weights by which the packet is distributed onto the cube faces after the internal controller acts.

---

## Updated semantic reading

The sketch now says:

1. a unit packet enters the cube-cell from below,
2. the cell applies a local chamber/controller bifurcation,
3. the packet is redistributed into multiple face receipts,
4. those receipts appear on cube faces as weighted projections,
5. the top outputs record the active local control readout.

So the cube is not just a box.
It is a projection lens.

---

## Connection to current machinery

### G15
Supplies the local packet grammar:
- anchor controller
- odd branch
- E1 sheet
- E2 sheet
- rigid distal skeleton
- cancellation channel

### G30
Acts as the organizer:
- splits the packet into channels
- assigns weights
- determines adjacency and pairing
- prepares face deployment

### G60 cube
Acts as the visible carrier:
- receives the organized transport
- places it on faces
- displays the weighted receipts

So the sketch becomes a compact lens diagram:

\[
\text{packet from } G15
\to
\text{organization in } G30
\to
\text{face receipts on a } G60 \text{ cube}.
\]

---

## Suggested renamed labels for a clean redraw

### Bottom
- `unit packet`

### Top left arrow
- `control readout alpha`

### Top right arrow
- `control readout beta`

### Front face
- `face receipt w_front`

### Left face
- `face receipt w_left`

### Right face
- `face receipt w_right`

### Side length
- `l_planck`

### Cube title
- `local carrier cell`
or
- `G60 face-cell`

---

## More theory-flavored version

If you want the drawing to align directly with the automaton language, use:

### Bottom
- `G15 packet seed`

### Internal cube
- `G30 controller / organizer`

### Faces
- `G60 face receipts`

### Top outputs
- `anchored phase readouts`

Then the sketch says:

\[
G15 \text{ seed}
\to
G30 \text{ chamber controller}
\to
G60 \text{ face receipts}.
\]

---

## Strongest current reading

This old sketch can now be read as an early packet-through-cell lens:
a unit packet enters a finite chamber cell, undergoes anchored control, and is projected outward as weighted face receipts.

That is strongly compatible with the current two-phase anchored controller over a rigid distal backbone.

