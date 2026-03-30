# G60 Stabilization Variable Note

## Status
Working note

## Purpose

This note introduces the smallest possible stabilization variable needed to test whether G60 can be more than a trivial repetition of G30.

The central question is:

> What is the smallest extra state component that lets the orthogonal companion sector carry genuine higher-order closure?

---

## 1. Minimal first-order machine

The locked first-order machine is:

\[
W(x,\varepsilon,h)=(x,-\varepsilon,\phi(h))
\]

with Type III:

\[
\phi(0)=0,\quad \phi(2)=2,\quad \phi(1)=3,\quad \phi(3)=1.
\]

This already gives:

- sign flip on one cycle
- identity restoration on two cycles
- axial classes fixed
- orthogonal classes exchanged

But by itself it does not make G60 new.

---

## 2. Smallest extension idea

To make G60 potentially nontrivial, the orthogonal sector must carry an additional stabilization memory.

So extend the state by one new variable:

\[
m.
\]

The extended state becomes:

\[
(x,\varepsilon,h,m).
\]

The new cycle law is:

\[
\widehat W(x,\varepsilon,h,m)=(x,-\varepsilon,\phi(h),\mu(h,m)).
\]

The problem is to choose the smallest useful state set for \(m\) and the smallest useful update rule \(\mu\).

---

## 3. First attempt: binary stabilization bit

Take

\[
m\in\mathbb Z_2=\{0,1\}.
\]

Interpretation:

- \(m=0\): not yet stabilized
- \(m=1\): stabilized or completed

Define the update law:

\[
\mu(h,m)=
\begin{cases}
m & h\in\{0,2\} \\
1-m & h\in\{1,3\}.
\end{cases}
\]

So:

- axial sector leaves \(m\) unchanged
- orthogonal sector flips \(m\)

---

## 4. Result of the binary model

This binary model is the smallest nontrivial extension.

It succeeds in giving the orthogonal sector a distinct role:

- axial relaunches do not advance stabilization
- orthogonal relaunches do

However, two orthogonal passes restore the bit:

\[
m \to 1-m \to m.
\]

So the full extended state still restores too quickly.

Conclusion:

> the binary stabilization bit is enough to enrich the orthogonal sector, but not enough to make G60 genuinely new.

This is a useful negative result.

---

## 5. First serious candidate: four-phase stabilizer

To get a genuinely longer completion cycle, take instead:

\[
m\in\mathbb Z_4=\{0,1,2,3\}.
\]

Define:

\[
\mu(h,m)=
\begin{cases}
m & h\in\{0,2\} \\
m+1 \pmod 4 & h\in\{1,3\}.
\end{cases}
\]

So:

- axial sector does not advance \(m\)
- orthogonal sector advances \(m\) by one phase each time

This is the smallest useful multi-phase stabilizer.

---

## 6. Why Z4 is the first serious candidate

The \(\mathbb Z_4\) model has exactly the right features:

- it preserves the Type III relaunch split
- it keeps the axial sector quiet
- it makes the orthogonal sector genuinely accumulative
- it introduces a four-step completion law

Under repeated orthogonal action:

\[
0 \to 1 \to 2 \to 3 \to 0.
\]

So the orthogonal companion sector can now carry a full stabilization cycle of its own.

This is the first extension that makes recursive G60 plausible.

---

## 7. Working interpretation

Under the \(\mathbb Z_4\) stabilization model:

- the walker can restore at G30
- the orthogonal sector can still be mid-cycle in stabilization phase
- only after further orthogonal completion does the higher-order machine close

This is the sense in which G60 may become a true higher-order closure rather than a repetition of G30.

---

## 8. Strong current conclusion

The strongest current conclusion is:

- a binary stabilization bit is too small
- a four-phase orthogonal stabilizer is the first serious candidate for a genuinely new G60 closure law

So if recursive G60 is real, it most likely lives on top of a \(\mathbb Z_4\)-type orthogonal stabilization cycle rather than a \(\mathbb Z_2\) one.

---

## 9. One-line summary

The smallest nontrivial stabilization variable is binary, but the smallest stabilization variable capable of making G60 genuinely new is four-phase and should be advanced only by the orthogonal companion sector.

