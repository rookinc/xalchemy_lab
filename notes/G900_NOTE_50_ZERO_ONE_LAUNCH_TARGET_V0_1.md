# G900 Note 50 — 0:1 Launch Target v0.1

## Purpose
Test whether the layer-pair 0:1 is the unique first outward launch relation in the current G900 carrier.

## Why this matters
The current staged grammar needs a clean launch primitive.

If layer 0 contacts only layer 1 in the cross-bit adjacency structure, then:

- 0:1 is the first outward boundary
- 0:1 is the cleanest launch candidate
- later stages can be treated separately as commit and reconcile

## Current target
Check whether:
- (0,1) is present
- (0,1) is unique among zero-layer outward contacts

