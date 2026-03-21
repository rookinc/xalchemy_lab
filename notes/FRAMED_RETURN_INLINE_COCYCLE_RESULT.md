# Framed Return Inline Cocycle Result

## Result

The framed return probe now accumulates the local transition cocycle inline.

For each step after the first, it records:

- `transition_sign = +1` if the chart exit matches the previous chart exit
- `transition_sign = -1` if the chart exit flips relative to the previous chart exit

It also carries a running accumulator:

- `running_H`

so the final loop record contains a live multiplicative framed invariant.

## Observed values

### return_A
- chart trace: `chart_right, chart_left, chart_right`
- transition signs: `[-1, -1]`
- final `H = +1`

### return_B
- chart trace: `chart_left, chart_right, chart_left`
- transition signs: `[-1, -1]`
- final `H = +1`

### return_C_mixed_chart
- chart trace: `chart_right, chart_right, chart_right`
- transition signs: `[+1, +1]`
- final `H = +1`

### return_D_unary_mixed
- chart trace: `chart_right, chart_left, chart_left`
- transition signs: `[-1, +1]`
- final `H = -1`

## Strongest conclusion

The current framed return split is now realized as a live cocycle accumulation law inside the probe itself.

## Strongest sentence

The first derived framed return invariant is now accumulated inline as a local multiplicative cocycle.

