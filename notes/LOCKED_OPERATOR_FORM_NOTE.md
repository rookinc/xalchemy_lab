# Locked Operator Form Note

## Context

The latest probes strongly suggest that the signed tension-locked rail is governed by an exact operator form rather than merely an empirical pattern.

We now have evidence for:

- a broad basin into the locked rail
- polarity-preserving re-lock
- exact affine background growth
- exact transported stress defects
- exact transported mismatch defects
- exact superposition in the tested stress/mismatch sectors
- parity-controlled injection of sign-flip sources into mismatch

This note freezes the current operator picture.

---

## 1. Background rail state

Let the locked rail carry a background state

\[
(\mathbf{s}, \mathbf{m})
\]

where

- \(\mathbf{s} \in \mathbb{Z}^3\) is the stress vector
- \(\mathbf{m} \in \mathbb{Z}^3\) is the mismatch vector

with carriers ordered as

\[
(L1, L2, R1).
\]

In the locked regime, the sign configuration is no longer a free degree of freedom.
It is pinned to hub polarity:

- `+++` at `u1R`
- `---` at `d1R`

So sign is part of the rail orientation, not an independent transported amplitude.

---

## 2. Native hub-hit operator

The long-walk probe showed that every hub hit in the locked regime increments all stress and mismatch coordinates by one:

\[
T_{\mathrm{hub}}(\mathbf{s}, \mathbf{m})
=
(\mathbf{s} + \mathbf{1},\ \mathbf{m} + \mathbf{1})
\]

where

\[
\mathbf{1} = (1,1,1).
\]

So one tensional hub closure is an affine translation.

---

## 3. Native return-loop operator

A full opposite-and-return loop consists of two hub hits.
Therefore the loop operator is

\[
T_{\mathrm{loop}}(\mathbf{s}, \mathbf{m})
=
(\mathbf{s} + 2\mathbf{1},\ \mathbf{m} + 2\mathbf{1}).
\]

Equivalently,

\[
T_{\mathrm{loop}}(\mathbf{s}, \mathbf{m})
=
(\mathbf{s} + (2,2,2),\ \mathbf{m} + (2,2,2)).
\]

This is the clean locked background law.

---

## 4. Defect variables

Now let us add transported defect offsets:

- \(\delta \mathbf{s} \in \mathbb{Z}^3\)
- \(\delta \mathbf{m} \in \mathbb{Z}^3\)

These are defined relative to a baseline locked orbit:

\[
\delta \mathbf{s}
=
\mathbf{s}^{(p)} - \mathbf{s}^{(0)},
\qquad
\delta \mathbf{m}
=
\mathbf{m}^{(p)} - \mathbf{m}^{(0)}.
\]

The offset probes and large-amplitude sweeps indicate that after re-lock:

\[
\delta \mathbf{s},\ \delta \mathbf{m}
\]

are time-independent in the tested regime.

So the defect transport operator is simply

\[
D(\delta \mathbf{s}, \delta \mathbf{m})
=
(\delta \mathbf{s}, \delta \mathbf{m}).
\]

That is, defects are carried rigidly by the rail.

---

## 5. Stress defect sector

Stress defects behave exactly additively in the tested range.

Examples:

- adding stress \(a\) on `L1` yields
  \[
  \delta \mathbf{s} = (a,0,0)
  \]

- adding stress \(a\) on all carriers yields
  \[
  \delta \mathbf{s} = (a,a,a)
  \]

with no induced mismatch offset.

So the stress defect sector is

\[
\mathcal{D}_s \cong \mathbb{Z}^3.
\]

---

## 6. Mismatch defect sector

Mismatch defects also behave exactly additively in the tested range.

Examples:

- adding mismatch \(a\) on `L1` yields
  \[
  \delta \mathbf{m} = (a,0,0)
  \]

- adding mismatch \(a\) on `R1` yields
  \[
  \delta \mathbf{m} = (0,0,a)
  \]

with no induced stress offset.

So the mismatch defect sector is

\[
\mathcal{D}_m \cong \mathbb{Z}^3.
\]

---

## 7. Flip-source sector

Sign flips do not survive as persistent sign defects.

Instead, after re-lock:

- final signs return to rail polarity
- the only residual memory is a mismatch offset

For a fixed carrier \(i\), repeated flips reduce by parity:

\[
n_i \mapsto n_i \bmod 2.
\]

If \(e_i\) is the mismatch basis vector on carrier \(i\), then the injected mismatch defect is

\[
(n_i \bmod 2)\,e_i.
\]

Thus the flip source sector is naturally

\[
\mathcal{F} \cong (\mathbb{Z}_2)^3.
\]

---

## 8. Parity injection map

The sign-flip sector enters the transported defect algebra through a parity map

\[
\phi : (\mathbb{Z}_2)^3 \to \mathbb{Z}^3
\]

given componentwise by

\[
\phi(f_1,f_2,f_3) = (f_1,f_2,f_3),
\]

where each \(f_i \in \{0,1\}\) is the parity of the flip count on carrier \(i\).

Operationally:

- even flips inject nothing
- odd flips inject one unit mismatch on that carrier

So the effective mismatch defect becomes

\[
\delta \mathbf{m}_{\mathrm{eff}}
=
\delta \mathbf{m} + \phi(\mathbf{f}).
\]

---

## 9. Combined defect operator

Putting the pieces together, the stabilized defect operator is

\[
D(\delta \mathbf{s}, \delta \mathbf{m}, \mathbf{f})
=
(\delta \mathbf{s},\ \delta \mathbf{m} + \phi(\mathbf{f})).
\]

Here:

- \(\delta \mathbf{s} \in \mathbb{Z}^3\)
- \(\delta \mathbf{m} \in \mathbb{Z}^3\)
- \(\mathbf{f} \in (\mathbb{Z}_2)^3\)

This is semilinear because the transported sectors are additive, while the flip-source sector enters only through parity reduction.

---

## 10. Full locked operator form

The total locked dynamics may therefore be written as:

### Background
\[
T_{\mathrm{hub}}(\mathbf{s}, \mathbf{m})
=
(\mathbf{s} + \mathbf{1},\ \mathbf{m} + \mathbf{1})
\]

or over a full return loop

\[
T_{\mathrm{loop}}(\mathbf{s}, \mathbf{m})
=
(\mathbf{s} + 2\mathbf{1},\ \mathbf{m} + 2\mathbf{1}).
\]

### Defect transport
\[
D(\delta \mathbf{s}, \delta \mathbf{m}, \mathbf{f})
=
(\delta \mathbf{s},\ \delta \mathbf{m} + \phi(\mathbf{f})).
\]

### Combined observed state
\[
(\mathbf{s}, \mathbf{m})_{\mathrm{observed}}
=
(\mathbf{s}, \mathbf{m})_{\mathrm{background}}
+
(\delta \mathbf{s},\ \delta \mathbf{m} + \phi(\mathbf{f})).
\]

This is the current empirical operator form.

---

## 11. Superposition law

The superposition probe showed:

\[
\delta \mathbf{s}_{12}
=
\delta \mathbf{s}_1 + \delta \mathbf{s}_2,
\qquad
\delta \mathbf{m}_{12}
=
\delta \mathbf{m}_1 + \delta \mathbf{m}_2
\]

for the tested combined defects, once the flip contributions are first reduced by parity.

Thus the effective defect space is additive after source reduction.

---

## 12. Finite-amplitude exactness

The large-defect threshold sweep found no failure up to amplitude 50 in the tested stress and mismatch families.

So, at least in that window, the operator form appears exact rather than merely infinitesimal.

That is unusually strong.

---

## 13. Working algebraic picture

The rail currently looks like:

\[
\mathbb{Z}^3_s \oplus \mathbb{Z}^3_m
\]

as the transported additive defect sector, together with a source map

\[
(\mathbb{Z}_2)^3 \to \mathbb{Z}^3_m
\]

feeding mismatch by parity.

So the best current verbal description is:

> The signed tension-locked rail carries an affine background flow and an exact semilinear defect algebra.

---

## 14. Conjecture

### Exact Locked Operator Conjecture

In the locked regime, the tri-patch dynamics factor as:

1. an affine background translation on \((\mathbf{s}, \mathbf{m})\)
2. an exact additive transport of stress and mismatch defect offsets
3. a parity-reduced sign-flip source map injecting into the mismatch sector

Equivalently, the rail supports a transported defect algebra of the form

\[
\mathbb{Z}^3_s \oplus \mathbb{Z}^3_m
\quad\text{with source}\quad
(\mathbb{Z}_2)^3 \to \mathbb{Z}^3_m.
\]

---

## 15. Next frontier

The next question is no longer whether this operator form exists locally.
The next question is whether the same operator persists when the turtles are allowed to engage a larger neighborhood of the graph rather than the minimal locked rail.

That is where the local defect algebra becomes a graph-dynamical theory.

