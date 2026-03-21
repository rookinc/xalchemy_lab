# Derivation of Framed Return Invariant v0.1

## Goal

Derive the framed return invariant from local framed transition updates rather than only by post-processing the completed chart trace.

## Chart trace

Let a transport path produce a chart-relative trace

- c_1, c_2, ..., c_n

where each c_k is one of:

- chart_left
- chart_right

## Local framed transition sign

Define the local transition cocycle

- omega(c_{k-1}, c_k)

by:

- +1 if c_k = c_{k-1}
- -1 if c_k != c_{k-1}

Interpretation:

- staying on the same chart side contributes +1
- flipping chart side contributes -1

## Derived invariant

Define the framed return invariant

- H = product over k=2..n of omega(c_{k-1}, c_k)

Equivalently:

- H = parity of chart-coordinate flips along the trace

## Accumulator form

Define a transported accumulator h_k by:

- h_1 = +1
- h_k = h_{k-1} * omega(c_{k-1}, c_k)

Then the final framed return invariant is:

- H = h_n

So H is not merely a post-processed statistic.
It is the accumulated product of local framed transition signs.

## Interpretation

- H = +1 means an even number of chart flips
- H = -1 means an odd number of chart flips

## Check against current probes

- return_A: chart_right, chart_left, chart_right
  - omega = [-1, -1]
  - H = +1

- return_B: chart_left, chart_right, chart_left
  - omega = [-1, -1]
  - H = +1

- return_C_mixed_chart: chart_right, chart_right, chart_right
  - omega = [+1, +1]
  - H = +1

- return_D_unary_mixed: chart_right, chart_left, chart_left
  - omega = [-1, +1]
  - H = -1

## Strongest sentence

The framed return invariant is the multiplicative accumulation of a local framed transition cocycle.

