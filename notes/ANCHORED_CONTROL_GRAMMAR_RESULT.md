# Anchored Control Grammar Result

## Checkpoint

The anchored trace grammar splits into two distinct charts.

## A = 0 chart

- (A,O,O,O) tracks tau
- (A,E1,E1,E1) tracks sigma
- (A,E2,E2,E2) stays even
- shuttle traces depend on sigma/tau interaction

So A=0 is the baseline odd/E1 control chart.

## A = 1 chart

- (A,E2,E2,E2) is always odd
- (A,E1,E1,E1) is odd except at (sigma,tau)=(1,0)
- (A,O,O,O) is odd except at (sigma,tau)=(0,1)

So A=1 is not a simple swap of the A=0 chart.
It is a distinct E2-dominant anchored control chart.

## Strongest current reading

The A-control acts as a chart selector on anchored control grammar.

