# Holonomic Loop Probe Result

## Goal

Test whether the controller register `(A, sigma, tau)` behaves like a local framed transport state rather than a mere edge-labeled lookup state.

## Probe setup

Two controllers were compared:

- `v011 = (A,sigma,tau) = (0,1,1)`
- `v111 = (A,sigma,tau) = (1,1,1)`

Both were run on the same handedness sequence:

- left
- right
- left

Routing mode:
- `state_sensitive_under_load`

In this probe, no burden override fired, so the observed behavior reflects the structural local law directly.

## Physical-edge result

Both controllers produced the same physical exit sequence:

- `e_right`
- `e_left`
- `e_right`

They also produced the same runtime summary:

- same route counts
- same neutral switch state
- same event count

So in raw physical edge labels, the two controllers appear identical.

## Chart-coordinate result

After translating exits into chart-relative coordinates:

### v011 = (0,1,1)
- left  -> `chart_right`
- right -> `chart_left`
- left  -> `chart_right`

So the chart trace is:

- `chart_right`
- `chart_left`
- `chart_right`

### v111 = (1,1,1)
- left  -> `chart_left`
- right -> `chart_right`
- left  -> `chart_left`

So the chart trace is:

- `chart_left`
- `chart_right`
- `chart_left`

Thus the same physical trace carries opposite chart-coordinate meaning.

## Strongest conclusion

The operative local object is not the raw physical exit label.

It is the exit as read through the local chart.

That means the controller law is framed and holonomic in flavor.

## Strongest sentence

Two controllers can produce the same physical transport trace while producing opposite chart-coordinate traces; therefore the local law is not fully captured by edge labels alone.

## Interpretation

This supports the hypothesis that `(A, sigma, tau)` is acting as a local framed transport state.

In particular:

- `A` changes the chart-relative meaning of the same physical move
- the mixed reopened state is frame-sensitive
- physical transport data alone loses essential local structure

## What this does not yet prove

This probe does not yet prove a full holonomy theory.

It does not yet show:
- multi-vertex accumulation around a nontrivial loop
- a global return invariant
- or a derived connection law on a larger transport substrate

What it does show is the minimal local phenomenon that makes such a theory plausible.

## Next step

Construct a multi-controller loop probe and compare:

- physical-edge trace
- chart-coordinate trace
- returned local framed state

That will test whether framed meaning accumulates across a real loop rather than only at a single controller.

