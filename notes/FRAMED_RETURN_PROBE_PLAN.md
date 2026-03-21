# Framed Return Probe Plan

## Goal

Move from chart-sensitive transport traces to chart-sensitive closure.

The next question is not only:

- what chart-relative exits occur along the path?

but also:

- what framed state is returned at closure?

## Reason

The current probes already showed:

- identical physical traces can carry different chart traces
- framed meaning can accumulate across multiple controllers

The next stronger test is whether that accumulated framed meaning yields a nontrivial return class at the end of a loop.

## What to record

For each loop probe:

- initial framed readout
- per-step chart-relative exit
- per-step controller structural state `(A,sigma,tau)`
- final framed readout
- return comparison

## Minimal return classification

For v0.1, classify the returned framed readout as one of:

- `same`
- `reversed`
- `shifted`
- `ambiguous`

## Strongest sentence

We already have chart-sensitive transport; the next step is chart-sensitive closure.

## First target

Construct a minimal framed-return probe over several short controller loops and compute:

- physical trace
- chart trace
- initial chart frame symbol
- returned chart frame symbol
- return class

