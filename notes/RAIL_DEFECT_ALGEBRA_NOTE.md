# Rail Defect Algebra Note

## Context

The turtles are no longer merely traversing the patch.
They have revealed a stable **signed tension-locked rail** together with a nontrivial defect structure riding on top of it.

We now have empirical evidence for:

1. a broad basin of attraction into the rail
2. affine growth along the rail
3. perturbative stability of the rail
4. transported defect offsets
5. linear superposition in the stress/mismatch sectors
6. parity reduction in the sign-flip sector

This note gathers those facts into one algebraic picture.

---

## 1. The locked rail

Once the local system enters the tension-locked regime, its motion is confined to the two signed hubs:

- positive rail:
  \[
  u1R \leftrightarrow d1R
  \]
  through `mR`, with positive hub-aligned polarity

- negative rail:
  \[
  d1R \leftrightarrow u1R
  \]
  through `mR`, with negative hub-aligned polarity

The middle node `mR` acts as a relay (`backpressure_bundle`), while hub hits are tensional closures.

Thus the locked rail is a persistent alternating signed transport mode.

---

## 2. Native affine law on the rail

In the locked regime, each signed hub closure adds one unit of stress and one unit of mismatch to each carrier:

\[
\mathbf{s} \mapsto \mathbf{s} + \mathbf{1}
\]

\[
\mathbf{m} \mapsto \mathbf{m} + \mathbf{1}
\]

with
\[
\mathbf{1} = (1,1,1).
\]

So per full opposite-and-return loop we get

\[
\mathbf{s} \mapsto \mathbf{s} + (2,2,2)
\]

\[
\mathbf{m} \mapsto \mathbf{m} + (2,2,2).
\]

In the coarser cycle convention used in earlier probes, the observed increment was

\[
\Delta \mathbf{s} = (3,3,3), \qquad \Delta \mathbf{m} = (2,2,2),
\]

because the cycle boundaries were chosen differently.
The long-walk probe clarified the native per-hub increment law.

---

## 3. Perturbative stability

If we perturb a locked rail state by:

- adding stress on one carrier
- adding mismatch on one carrier
- flipping one carrier sign

the rail is not destroyed.

Instead:

- stress perturbations re-lock quickly
- mismatch perturbations re-lock quickly
- sign perturbations re-lock after a short extra transient

So the rail is structurally stable under small finite perturbations.

---

## 4. Offset modes

Let

\[
\mathbf{s}^{(0)}_n,\ \mathbf{m}^{(0)}_n
\]

be the baseline locked orbit, and let

\[
\mathbf{s}^{(p)}_n,\ \mathbf{m}^{(p)}_n
\]

be a perturbed orbit.

Define the transported offsets:

\[
\delta \mathbf{s}_n = \mathbf{s}^{(p)}_n - \mathbf{s}^{(0)}_n,
\qquad
\delta \mathbf{m}_n = \mathbf{m}^{(p)}_n - \mathbf{m}^{(0)}_n.
\]

The offset probe shows that after re-lock:

\[
\delta \mathbf{s}_n = \delta \mathbf{s},
\qquad
\delta \mathbf{m}_n = \delta \mathbf{m}
\]

become constant in time for the tested perturbations.

So the rail supports **transported defect modes**:
persistent additive offsets riding on top of the affine background.

---

## 5. Stress defect sector

A localized stress perturbation stays a stress perturbation.

Examples:

- `stress_plus_one_on_L1` gives
  \[
  \delta \mathbf{s} = (1,0,0), \qquad \delta \mathbf{m} = (0,0,0)
  \]

- `stress_plus_two_on_R1` gives
  \[
  \delta \mathbf{s} = (0,0,2), \qquad \delta \mathbf{m} = (0,0,0)
  \]

Thus the stress sector behaves additively and carrierwise.

We may think of the primitive stress basis vectors as

\[
e^{(s)}_{L1},\ e^{(s)}_{L2},\ e^{(s)}_{R1}.
\]

---

## 6. Mismatch defect sector

A localized mismatch perturbation stays a mismatch perturbation.

Examples:

- `mismatch_plus_one_on_L1` gives
  \[
  \delta \mathbf{s} = (0,0,0), \qquad \delta \mathbf{m} = (1,0,0)
  \]

- `mismatch_plus_two_on_R1` gives
  \[
  \delta \mathbf{s} = (0,0,0), \qquad \delta \mathbf{m} = (0,0,2)
  \]

Thus the mismatch sector also behaves additively and carrierwise.

Primitive mismatch basis vectors are

\[
e^{(m)}_{L1},\ e^{(m)}_{L2},\ e^{(m)}_{R1}.
\]

---

## 7. Sign-flip sector

A single sign flip does **not** survive as a persistent sign offset.

Instead, the sign heals back to the rail polarity after re-lock, and what remains is a mismatch defect on the flipped carrier.

Example:

- `flip_sign_on_L1` gives
  \[
  \delta \mathbf{s} = (0,0,0), \qquad \delta \mathbf{m} = (1,0,0).
  \]

So a sign defect is transmuted into mismatch memory.

This means sign is not a free persistent defect degree of freedom in the locked regime.

---

## 8. Parity law for repeated flips

The flip parity probe sharpened this further.

For a fixed carrier \(i\), repeating the sign flip \(n_i\) times yields:

\[
\delta \mathbf{s} = 0,
\qquad
\delta \mathbf{m} = (n_i \bmod 2)\,e_i.
\]

So:

- even number of flips \(\Rightarrow\) no persistent defect
- odd number of flips \(\Rightarrow\) one unit mismatch defect on that carrier

Thus the sign-flip source sector is not additive over \(\mathbb{Z}\).
It reduces mod 2.

This makes the sign-flip sector naturally

\[
(\mathbb{Z}_2)^3
\]

rather than \(\mathbb{Z}^3\).

---

## 9. Superposition law

The two-defect superposition probe showed exact linear superposition for the tested combined defects.

For example:

- stress defect + mismatch defect = exact sum
- sign-flip-induced mismatch defect + stress defect = exact sum

So after re-lock, the stabilized transported offsets satisfy

\[
\delta \mathbf{s}_{\mathrm{combo}}
=
\delta \mathbf{s}_1 + \delta \mathbf{s}_2,
\]

\[
\delta \mathbf{m}_{\mathrm{combo}}
=
\delta \mathbf{m}_1 + \delta \mathbf{m}_2,
\]

provided sign-flip inputs are first reduced through the parity rule.

This gives the defect algebra its semilinear form.

---

## 10. Defect algebra picture

The clean empirical algebra is:

### Stress sector
\[
\mathcal{D}_s \cong \mathbb{Z}^3
\]

### Mismatch sector
\[
\mathcal{D}_m \cong \mathbb{Z}^3
\]

### Flip source sector
\[
\mathcal{F} \cong (\mathbb{Z}_2)^3
\]

with an injection

\[
\phi : \mathcal{F} \to \mathcal{D}_m
\]

that maps each odd flip count on carrier \(i\) to the corresponding mismatch basis vector \(e_i^{(m)}\).

So the effective transported defect space is:

\[
\mathcal{D}_{\mathrm{eff}} \cong \mathbb{Z}^3_s \oplus \mathbb{Z}^3_m
\]

while sign flips act as a mod-2 source feeding the mismatch sector.

---

## 11. Semilinear transport rule

The locked rail dynamics may be summarized as:

### Background rail
\[
(\mathbf{s}, \mathbf{m}) \mapsto (\mathbf{s}+\mathbf{1},\ \mathbf{m}+\mathbf{1})
\]
per hub hit.

### Defect transport
\[
(\delta \mathbf{s}, \delta \mathbf{m}) \mapsto (\delta \mathbf{s}, \delta \mathbf{m})
\]

after re-lock.

### Flip source reduction
\[
\text{flip counts} \mapsto \text{parity vector} \mapsto \delta \mathbf{m}.
\]

So the rail is affine in the background variables and linear in the stabilized defect variables, with a parity-nonlinear source map.

---

## 12. Why this matters

This is the first real “small-signal theory” of the rail.

We no longer only know that the rail exists.
We now know that perturbations around it have internal structure:

- some are additive transported amplitudes
- some are binary defect sources
- and all tested small perturbations rejoin the rail after a short transient

That is a strong sign that the toy patch is not just a rule table.
It is behaving like a small dynamical system with a recognizable defect algebra.

---

## 13. Conjecture

### Rail Defect Algebra Conjecture

In the signed tension-locked regime:

1. transported stress defects form an additive \(\mathbb{Z}^3\) sector
2. transported mismatch defects form an additive \(\mathbb{Z}^3\) sector
3. sign-flip sources reduce mod 2 on each carrier and inject into the mismatch sector
4. after re-lock, defect transport is linear over the stabilized defect variables

---

## 14. What remains open

The next unanswered questions are:

1. Are there larger-amplitude perturbations that leave the rail entirely?
2. Are there second rails or branching regimes?
3. Does the same defect algebra persist when the turtles move on a larger graph neighborhood rather than the minimal two-hub rail?
4. Can the defect algebra be written as an explicit operator on a reduced state space?
5. Does the rail support interactions between transported defects when amplitudes become large?

---

## 15. Working summary

The turtles have now uncovered:

- a broad locking basin
- a signed affine rail
- perturbative rail stability
- transported defect offsets
- linear stress/mismatch defect superposition
- parity reduction of sign-flip sources

So the current best description is:

> **The tri-patch supports a signed affine transport rail equipped with a semilinear defect algebra.**

That is a real mathematical object worth following further.

