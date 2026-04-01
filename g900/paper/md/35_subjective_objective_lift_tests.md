# Subjective / Objective Lift Tests

## Status
Test-plan note

## Purpose
Turn the subjective/objective lift hypothesis into explicit finite checks.

---

## 1. Core question

The signed 2-lift
\[
G_{30}\to G_{15}
\]
already exists, together with its nontrivial \(\mathbb Z_2\)-valued cocycle. The working question is whether the two sheets can be interpreted as subjective/objective transport modes. 1

---

## 2. Minimal test doctrine

We seek a labeling
\[
\lambda: V(G_{30})\to\{S,O\}
\]
such that:

1. each fiber over a core vertex has one \(S\)-sheet and one \(O\)-sheet;
2. transport across a lifted edge preserves or flips the label according to the edge sign/cocycle;
3. loop holonomy parity matches subjective/objective return versus swap.

---

## 3. Test 1: fiber labeling

For each vertex \(v\in V(G_{15})\), verify that its two lifts can be labeled
\[
v^S,\ v^O.
\]

This is the structural minimum for the doctrine.

---

## 4. Test 2: edge transport parity

For each base edge \(uv\in E(G_{15})\):

- if the lift is parallel, transport preserves the \(S/O\) label;
- if the lift is crossed, transport swaps the \(S/O\) label.

This is the edge-level realization of the doctrine.

---

## 5. Test 3: loop holonomy

For each cycle \(C\subseteq G_{15}\), compute cocycle parity
\[
\omega(C)\in\mathbb Z_2.
\]

Then verify:

- even parity: lifted transport returns to the same \(S/O\) label,
- odd parity: lifted transport returns to the opposite \(S/O\) label.

This is the first real invariant test.

---

## 6. Test 4: local compression to frame-2 socket behavior

For selected core states involved in the frame-2 local machine, identify their two lifts in \(G_{30}\), then ask whether the exact junction / punctured branch picture on the core is the quotient image of a two-sheet local law upstairs.

This is the bridge from lift doctrine to the recent local machine work.

---

## 7. Success criterion

The doctrine is strongly supported if:

- every fiber admits a coherent \(S/O\) labeling,
- edge transport agrees with lift sign,
- loop parity agrees with \(S/O\) return/swap,
- and local core behavior can be read as the quotient shadow of the two-sheet law.

