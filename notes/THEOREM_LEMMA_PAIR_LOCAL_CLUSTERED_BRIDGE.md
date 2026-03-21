# Theorem/Lemma Pair: Local Clustered Bridge Structure

## Setup

Let the current seeded local signed-lift neighborhood carry the derived mod-2 edge state
\[
\varepsilon : E \to \mathbb Z_2.
\]

Let the current bridge signature be read through the class representatives:

- return-type representative:
  \[
  q0 \to q1 \to q0
  \]
- square-type representative:
  \[
  q0 \to q1 \to q6 \to q3 \to q0
  \]
- twist-type representative:
  \[
  q0 \to q1 \to q5 \to q2 \to q0
  \]

and let the current observed bridge signature be
\[
(\mathrm{return},\mathrm{square},\mathrm{twist})=(0,0,1).
\]

Define:

- rigid anchor
  \[
  a := e00
  \]
- twist cluster
  \[
  T := \{e01,e04,e07\}
  \]
- square cluster
  \[
  S := \{e02,e05,e10\}.
  \]

---

## Lemma (Cluster dependence)

In the current seeded local model, the class-based bridge signature depends essentially on the rigid anchor \(a\) together with the two 3-edge clusters \(T\) and \(S\).

More precisely:

1. flipping \(a=e00\) destroys the bridge signature;

2. flipping any one tested edge of \(T\) destroys the bridge signature;

3. flipping any one tested edge of \(S\) destroys the bridge signature;

4. some double flips inside \(T\) restore the signature;

5. some double flips inside \(S\) restore the signature;

6. the full triple flip of \(T\) destroys the twist class;

7. the full triple flip of \(S\) destroys the square class.

### Proof sketch

This is the direct content of the robustness sweeps:

- single-flip odd/even sweeps identified
  \[
  e00,e01,e02,e04,e05,e07,e10
  \]
  as essential tested edges;

- double-flip sweeps showed restoring pairs within the two 3-edge clusters;

- triple-flip tests showed:
  - flipping all of \(T\) sends
    \[
    (0,0,1)\mapsto(0,0,0),
    \]
    hence kills the twist sector;
  - flipping all of \(S\) sends
    \[
    (0,0,1)\mapsto(0,1,1),
    \]
    hence kills the square sector.

So the bridge is controlled by a clustered support pattern rather than isolated loop labels alone.

---

## Theorem (Stable local clustered bridge checkpoint)

In the current seeded local signed-lift neighborhood, the local/global bridge is governed by a stable clustered mod-2 support structure with the following properties:

1. the mismatch channel remains kernel-only:
   \[
   dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2;
   \]

2. the local lift register
   \[
   \lambda=\texttt{lift\_bit}
   \]
   remains the active local binary observable;

3. the global side separates into class representatives with
   \[
   \mathrm{return}=0,\qquad
   \mathrm{square}=0,\qquad
   \mathrm{twist}=1;
   \]

4. the square-type representative belongs to the even 4-cycle family, while the twist-type representative belongs to the odd family;

5. this class split is stably supported not by arbitrary cycle choices, but by the clustered support
   \[
   \{a\}\cup T\cup S
   \]
   where \(a=e00\), \(T=\{e01,e04,e07\}\), and \(S=\{e02,e05,e10\}\).

### Conclusion

At this checkpoint, the local/global bridge is best understood as a class-based mod-2 bridge carried by:

- a rigid anchor edge,
- a twist-support cluster,
- a square-support cluster,

with surrounding tested boundary edges acting as spectators rather than essential carriers.

---

## Short reading

The current local theorem is no longer just:

- “these named loops happen to match.”

It is now:

- one anchor edge matters,
- one 3-edge packet controls twist,
- one 3-edge packet controls square,
- the local lift bit matches that class split,
- and nearby boundary perturbations often do not destroy it.

That is the strongest current theorem-shaped reading of the seeded local actual-edge data.

