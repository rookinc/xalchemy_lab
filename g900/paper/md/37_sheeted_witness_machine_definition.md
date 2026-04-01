# Sheeted Witness Machine Definition

## Status
Working algebraic definition

## Purpose
Give the first clean algebraic closure of the current subjective/objective and sheet-tracking doctrine.

The goal is to define a minimal state space in which:

- the subjective/objective split is explicit,
- the hidden sheet bit is explicit,
- one full G15 cycle is sign-closing,
- two full G15 cycles restore identity,
- and the quotient-visible witness on \(G_{15}\) forgets the sheet coordinate.

This note does **not** yet prove that the sheet coordinate is canonically identical to the actual lift sheet of \(G_{30}\to G_{15}\). It defines the smallest algebraic machine consistent with the current verified behavior.

---

## 1. State space

Define the sheeted witness state space by
\[
\mathcal X := \mathbb Z_5 \times \mathbb Z_2 \times \mathbb Z_2.
\]

Write a state as
\[
(i,\phi,\sigma),
\]
where:

- \(i\in\mathbb Z_5\) is the frame index,
- \(\phi\in\mathbb Z_2\) is the family bit,
- \(\sigma\in\mathbb Z_2\) is the sheet bit.

Interpretation:

- \(\phi=0\): subjective family,
- \(\phi=1\): objective family,
- \(\sigma=0\): \(+\) sheet,
- \(\sigma=1\): \(-\) sheet.

So the machine has three registers:

1. frame register,
2. subjective/objective family register,
3. hidden sheet register.

---

## 2. Visible witness realization

Define the witness realization map
\[
\Psi:\mathcal X \to \{\text{normalized 6-cycles on }G_{15}\}
\]
by forgetting the sheet bit and using the subjective/objective cycle formulas.

### Subjective family
For \(\phi=0\),
\[
\Psi(i,0,\sigma)
=
[o_i,o_{i+1},o_{i+2},s_{i+2},t_i,s_i].
\]

### Objective family
For \(\phi=1\),
\[
\Psi(i,1,\sigma)
=
[o_i,o_{i+1},o_{i+2},s_{i+3},t_{i+3},s_i].
\]

Thus the quotient-visible witness depends only on \((i,\phi)\), not on \(\sigma\).

This is the first algebraic formulation of the current doctrine:

> the core \(G_{15}\) sees the family bit but forgets the sheet bit.

---

## 3. Family invariants

Define three family-profile functions:

\[
a(\phi),\qquad s(\phi),\qquad f(\phi),
\]
with

\[
a(0)=\mathrm{return},\qquad a(1)=\mathrm{forward},
\]
\[
s(0)=4,\qquad s(1)=5,
\]
\[
f(0)=26,\qquad f(1)=18.
\]

So the subjective/objective family split is encoded algebraically as:

- subjective: return-aligned, spread \(4\), fiber \(26\),
- objective: forward-aligned, spread \(5\), fiber \(18\).

These values match the currently verified transport-family bifurcation on \(G_{15}\).

---

## 4. Basic operators

### 4.1 Frame advance
Define
\[
\tau(i,\phi,\sigma):=(i+1,\phi,\sigma).
\]

This advances the frame and preserves family and sheet.

Since \(i\in\mathbb Z_5\),
\[
\tau^5=\mathrm{id}.
\]

### 4.2 Family toggle
Define
\[
\mu(i,\phi,\sigma):=(i,\phi+1,\sigma).
\]

This toggles subjective/objective and preserves frame and sheet.

Thus
\[
\mu^2=\mathrm{id}.
\]

### 4.3 Full G15 cycle operator
Define the sign-closing full G15 operator
\[
W(i,\phi,\sigma):=(i,\phi,\sigma+1).
\]

This preserves frame and family but flips the sheet bit.

Hence
\[
W^2=\mathrm{id}.
\]

This is the algebraic form of the locked project rule:

\[
n_{15}=-n_0,\qquad n_{30}=n_0.
\]

One full G15 circuit is sign-closing. Two full G15 circuits restore identity.

---

## 5. Quotient-visible machine

Define the quotient map
\[
\pi:\mathcal X\to \mathbb Z_5\times\mathbb Z_2
\]
by
\[
\pi(i,\phi,\sigma)=(i,\phi).
\]

Then \(\pi\) forgets the sheet bit.

So the visible machine on the quotient core is exactly the \((\text{frame},\text{family})\) projection of the sheeted machine.

In particular,
\[
\pi\circ W=\pi.
\]

Thus the full G15 sign flip is invisible at the quotient-visible witness level.

This is the algebraic version of the current interpretive claim:

> the \(G_{15}\) witness sees the subjective/objective family but not the hidden sheet.

---

## 6. The minimal machine package

The **sheeted witness machine** is the system
\[
(\mathcal X,\Psi,\tau,\mu,W,\pi),
\]
where:

\[
\mathcal X=\mathbb Z_5\times\mathbb Z_2\times\mathbb Z_2,
\]
\[
\tau(i,\phi,\sigma)=(i+1,\phi,\sigma),
\]
\[
\mu(i,\phi,\sigma)=(i,\phi+1,\sigma),
\]
\[
W(i,\phi,\sigma)=(i,\phi,\sigma+1),
\]
with \(\Psi\) and \(\pi\) as above.

It satisfies:
\[
\tau^5=\mathrm{id},\qquad
\mu^2=\mathrm{id},\qquad
W^2=\mathrm{id},
\]
and
\[
\pi\circ W=\pi.
\]

---

## 7. Interpretation

This machine separates three currently distinct phenomena.

### 7.1 Frame transport
The frame register \(i\) records cyclic position.

### 7.2 Subjective/objective transport family
The family register \(\phi\) records the verified transport bifurcation:
- subjective = return / spread 4 / fiber 26,
- objective = forward / spread 5 / fiber 18.

### 7.3 Hidden sign/sheet
The sheet register \(\sigma\) records the hidden sign bit required to model:

- one full G15 cycle = sign closure,
- two full G15 cycles = identity restoration.

So the machine now has an explicit algebra for the phenomenon that the current cockpit already demonstrates computationally.

---

## 8. Current status

This definition is intentionally modest.

It does **not** yet prove that:

- the sheet bit \(\sigma\) is canonically identical to the actual lift sheet of \(G_{30}\to G_{15}\),
- the signed cocycle is literally the transport law on \(\sigma\),
- the local frame-2 socket branch is already the quotient shadow of a fully defined upstairs sheet law.

Those are next-step theorem problems.

What this note does provide is the first algebraic object in which the currently verified behavior is forced rather than merely narrated.

---

## 9. Working summary

The current best algebraic closure of the doctrine is:

- state space:
  \[
  \mathcal X=\mathbb Z_5\times\mathbb Z_2\times\mathbb Z_2,
  \]
- visible witness:
  depends on frame and family,
- hidden sign:
  carried by the sheet bit,
- one full G15 cycle:
  flips sheet,
- two full G15 cycles:
  restore identity.

In one line:

> the subjective/objective witness machine becomes algebraically coherent once one adjoins a hidden \(\mathbb Z_2\) sheet register that is invisible on the quotient-visible witness but flips under the full G15 cycle.

