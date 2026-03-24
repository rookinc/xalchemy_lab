# G900 Branch Completion Theorem v0.1

## Goal
State the final proof target for the 900 closure law in the sharpest possible form.

## Fixed observed centered prism
\[
(140,145,150)=(I-5,\ I,\ I+5),\qquad I=145.
\]

This immediately gives the paired boundary observable:
\[
(I-5)+(I+5)=2I=290.
\]

So:
\[
B=290.
\]

That part is already closed.

---

## Remaining target
Prove the closure observable:
\[
C=900.
\]

The intended form is
\[
900=180+2\cdot 360.
\]

The issue is not arithmetic.
The issue is the geometric/topological realization of the two branches.

---

## Closure ladder
Use the 4→5→6 closure ladder:

- 4 = first closed triangular seed
- 5 = exactly two complementary departures
- 6 = completed enclosure of each departure

This yields the decomposition:

\[
4 \Rightarrow 180,
\qquad
5 \Rightarrow 2,
\qquad
6 \Rightarrow 360 \text{ per branch}.
\]

Hence:
\[
C=180+2\cdot 360=900.
\]

---

## Branch Completion Theorem
### Statement
In the 4→5→6 closure ladder, each stage-5 complementary departure is realized at stage 6 by the unique minimal closed curve that encloses the stage-4 seed.

Therefore each branch has winding number 1 and contributes exactly:
\[
360.
\]

Since stage 5 supplies two such branches, total closure is:
\[
180+360+360=900.
\]

---

## Proof spine

### Lemma 1. Seed lemma
Stage 4 is the first closed triangular cell.

So the seed contributes:
\[
180.
\]

### Lemma 2. Split lemma
Stage 5 produces exactly two complementary departures.

So the branch count is:
\[
2.
\]

### Lemma 3. Branch completion lemma
A stage-5 branch cannot realize closure as:

- an open spur,
- a local fold-back,
- a partial arc with winding 0,
- or a multiply wound loop with winding \(>1\).

Reason:
- open objects are not closure,
- local returns that do not enclose the seed are not outer completion,
- winding 0 does not separate inside from outside,
- winding \(>1\) duplicates the same enclosure class and is nonminimal.

Therefore the only admissible realization is a simple enclosing loop of winding number 1.

Hence each branch contributes exactly:
\[
360.
\]

### Conclusion
\[
C=180+2\cdot 360=900.
\]

QED, provided the 4→5→6 ladder is the correct realization of the construction.

---

## Coupled result
For the centered prism
\[
(140,145,150)=(I-5,\ I,\ I+5),
\]
the two coupled observables are:

### Boundary observable
\[
B=290.
\]

### Closure observable
\[
C=900.
\]

So:
\[
(140,145,150)\Rightarrow (290,900).
\]

---

## Exact frontier
The final burden is now isolated to one sentence:

> each stage-5 complementary departure is realized at stage 6 by a unique minimal enclosing loop of the seed.

If that identification is secured from the construction, the 900 closure law is fully closed.

