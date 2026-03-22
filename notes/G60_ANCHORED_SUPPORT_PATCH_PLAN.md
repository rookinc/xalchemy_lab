# G60 Anchored Support Patch Plan

## Goal

Replace the first purely chamber-centered G60 patch idea with an anchored support patch built on the 15-anchor cube skeleton.

## Hypothesis

The correct first G60-facing framed support set is:

- 8 corner anchors
- 6 face-center anchors
- 1 cube-center anchor

for a total of 15 anchored vertices.

## Interpretation

This 15-anchor cube is the rigid support scaffold.

- corners = extremal boundary anchors
- face centers = sheet / face mediators
- cube center = central coupling / reference anchor

Everything else may vary relative to this scaffold.

## Why this is better than the earlier patch idea

The earlier chamber-centered patch was useful as a placeholder, but this anchor-first picture is structurally stronger because it gives:

- explicit privileged local sites
- explicit anchor roles
- an obvious central reference
- a natural local/global scaffold
- a rigid support set around which non-anchor structure may move

## Bridge to the toy framed layer

Toy local notions now map more naturally as:

- toy local carrier -> anchored vertex
- toy chart selector -> local chart at anchored site
- toy chart-relative exit -> local continuation class relative to the anchor scaffold
- toy parity-like quantity -> local framed reversal class on anchored paths
- toy displacement-like quantity -> net anchored framed bias along short paths

## Immediate next step

Define an explicit schema for an anchored support patch with:

- anchor id
- anchor role
- local chart
- incoming incidence
- candidate continuations
- chart-relative partition
- local reversal data
- short anchored return neighborhood

## Strongest sentence

The first G60 framed bridge object is not just a chamber-centered patch; it is an anchored support patch on the rigid 15-anchor cube skeleton.

