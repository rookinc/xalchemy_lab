# Theorem: Stable Local Class-Based Bridge Checkpoint

## Statement

In the current seeded local signed-lift neighborhood over the `G15` template, the local/global binary bridge organizes into a stable class-based split with the following properties.

### 1. Kernel channel
The local mismatch channel remains kernel-only:
\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

So mismatch parity continues to function as a selection rule, not as the active bridge observable.

### 2. Active local observable
The local lift register
\[
\lambda=\texttt{lift\_bit}
\]
remains the active local binary observable distinguishing the tested bridge rows.

### 3. Global class split
On the actual-edge side, the supported local 4-cycles split into two parity families:

- an **even 4-cycle family**
- an **odd 4-cycle family**

In the current completed seeded local template, the scan yields:
\[
18 \text{ supported 4-cycles},\qquad
13 \text{ even},\qquad
5 \text{ odd}.
\]

### 4. Class representatives
The bridge representatives now admit the following actual-edge readings:

#### Return-type representative
\[
q0 \to q1 \to q0
\]
which is even.

#### Square-type representative
A chosen representative of the even 4-cycle family:
\[
q0 \to q1 \to q6 \to q3 \to q0
\]
which is even.

#### Twist-type representative
A chosen representative of the odd family:
\[
q0 \to q1 \to q5 \to q2 \to q0
\]
which is odd.

### 5. Bridge match
Across the tested rows of the current local/global bridge table, the local lift bit matches the global parity classes:
\[
\text{return-type} \mapsto 0,\qquad
\text{square-type} \mapsto 0,\qquad
\text{twist-type} \mapsto 1.
\]

and the tested rows continue to report `MATCH`.

---

## Conclusion

At this checkpoint, the local/global bridge is best understood not as a match between local data and three isolated named loops, but as a match between:

- the local lift observable \(\lambda\), and
- global parity **classes** consisting of
  - even return/square-type representatives
  - odd twist-type representatives.

So the strongest current theorem-shaped claim is:

> **In the present seeded local signed-lift neighborhood, the tri-patch lift bit realizes the same binary class split as the actual-edge global parity data, while mismatch parity remains only the kernel condition.**

---

## Plain-English reading

The important result is not that one special loop called “square” happened to work.

The stronger result is:

- the local model has one meaningful bit: `lift_bit`
- the global side separates into even and odd loop classes
- return and square lie in the even class
- twist lies in the odd class
- and the local bit matches that split on the tested bridge rows

So the bridge has become class-based and geometric, not merely symbolic.

---

## Honesty clause

This is still a **local seeded theorem checkpoint**, not the final global theorem for the full Thalean lift.

What has been established is:

- a stable local actual-edge bridge pattern
- a stable even/odd family split
- and agreement between the local lift bit and the current actual-edge class representatives

What remains open is whether this persists under fuller lift completion and in the broader global construction.

