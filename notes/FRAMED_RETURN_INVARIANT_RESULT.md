# Framed Return Invariant Result

## Result

A first derived framed return invariant was computed from the chart trace.

For a chart trace:

- `c_1, ..., c_n`

define transition signs by:

- `+1` if consecutive chart symbols are the same
- `-1` if consecutive chart symbols differ

Then define:

- `H = product of transition signs`

This gives the parity of chart-coordinate flips along the trace.

## Observed values

### return_A
- chart trace: `chart_right, chart_left, chart_right`
- transition signs: `[-1, -1]`
- `H = +1`

### return_B
- chart trace: `chart_left, chart_right, chart_left`
- transition signs: `[-1, -1]`
- `H = +1`

### return_C_mixed_chart
- chart trace: `chart_right, chart_right, chart_right`
- transition signs: `[+1, +1]`
- `H = +1`

### return_D_unary_mixed
- chart trace: `chart_right, chart_left, chart_left`
- transition signs: `[-1, +1]`
- `H = -1`

## Strongest conclusion

The current coarse framed return split is recovered by a derived invariant of the full chart trace.

So the return behavior is not merely heuristic.
It is already expressible as a simple framed quantity.

## Strongest sentence

The first derived framed return invariant is the parity of chart-coordinate flips along the transport trace.

## Status

This is a v0.1 invariant candidate, not yet a final theory.
But it is the first genuine derived return quantity in the controller runtime.

