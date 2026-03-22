# G60 First Framed Readout

## Goal

Define the first framed readout on the chosen G60 local patch.

The chosen patch is:

- an oriented chamber-centered local adjacency patch

The immediate task is not yet to run a full transport law.
The immediate task is to define what the local framed readout even is.

## Question

Given one oriented chamber-centered local patch, how do we read a local continuation as:

- left-like
- right-like

relative to a chosen local chart?

This is the G60 lift of the toy notion:

- `chart_left`
- `chart_right`

## Minimal ingredients

The first framed readout requires only:

1. a chosen local carrier
   - one oriented chamber

2. a chosen local chart
   - an ordering or orientation convention on the local patch

3. a set of locally admissible continuations
   - the adjacent oriented continuations from that chamber

4. a partition of those continuations into framed classes
   - left-like
   - right-like

## Proposed v0.1 readout shape

For each oriented chamber-centered patch, define:

- `carrier`
- `chart_choice`
- `incoming_oriented_incidence`
- `candidate_continuations`
- `left_like_continuations`
- `right_like_continuations`

The key object is not the raw continuation alone.
It is the continuation as read through the local chart.

## Working principle

A continuation class is framed if changing the local chart can change how the same raw continuation is read.

That is the exact phenomenon the toy layer exposed.

So the first G60 readout should be designed to detect this:

- same raw continuation
- different chart-relative classification

## Minimal success condition

The readout succeeds if, on one explicit chamber-centered patch, you can exhibit:

- at least two locally distinct continuation classes
- a chart-relative labeling of those classes
- and a chart change that alters the framing of at least one continuation

## What not to do yet

Do not yet try to define:

- full global transport
- full G60 holonomy
- full invariant machinery
- full simulator semantics

Stay local.

## Deliverable target

The next artifact after this note should be a concrete patch description, something like:

- one named chamber
- its local adjacent continuations
- a local chart convention
- the resulting left-like/right-like partition

## Strongest sentence

The first G60 framed readout is the assignment of local continuations into chart-relative classes on a single oriented chamber-centered patch.

