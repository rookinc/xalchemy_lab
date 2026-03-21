# Next Step: Promote Chart-Coordinate Primacy

## Goal

Update the vertex-controller spec so that chart-coordinate interpretation is primary and physical edge labels are understood as projected/readout data.

## Reason

Recent probes showed:

- identical physical traces can carry different chart-coordinate meanings
- chart assignment changes transport meaning
- framed meaning can accumulate across multiple controllers

Therefore the controller law is not best described in raw edge labels alone.

## Required spec upgrades

The controller spec should explicitly state:

- `A` defines local chart orientation
- `sigma` and `tau` act as chart-relative collapse operators
- mixed reopening is interpreted in chart coordinates
- physical exits are a derived physical readout
- framed transport meaning may accumulate across multiple controllers

## Strongest sentence

The primary local transport object is the chart-relative exit, while the physical edge label is a projected representation of that local framed choice.

