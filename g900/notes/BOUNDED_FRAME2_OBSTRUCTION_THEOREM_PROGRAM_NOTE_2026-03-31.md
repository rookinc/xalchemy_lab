# BOUNDED_FRAME2_OBSTRUCTION_THEOREM_PROGRAM_NOTE_2026-03-31

## Status

Working theorem-program note.

This note reformulates the current computational results as a theorem-shaped program. It does not claim a final universal proof. Instead, it states the strongest bounded-regime formalization currently supported by the computational ladder and identifies the exact proof obligations that remain.

The aim is to convert a long exploratory computation into a compact and defensible mathematical position.

---

## 1. Executive summary

The current evidence supports a sharply localized obstruction picture.

After exact-preference repairs the dominant reachable frame-0 chamber, the residual basin funnels toward a frame-2 near-action seam. The key local fact is that exact frame-2 closure requires the normalized slot value `t2` at position 4.

The main bounded result is:

- starting from the distinguished locked frame-2 witness subset
- allowing bounded escape-and-return exploration with action distance cap 3
- exploring to saturation, observed by depth 6

the reachable bounded regime contains:

- no exact frame-2 closure
- no state with normalized slot 4 equal to `t2`

In the saturated bounded regime, the observed slot-4 symbol family is almost complete but uniquely excludes `t2`, the exact closure key. On the frame-2 seam itself, the observed slot-4 alphabet is the balanced 8-symbol set

- `{o4, s0, s2, s3, s4, t0, t3, t4}`

again excluding `t2`.

The cleanest current summary is:

> the residual frame-2 obstruction is a bounded-regime one-slot exclusion law: within the saturated bounded escape-and-return regime, the exact key `t2` at normalized position 4 never appears, so exact frame-2 closure never occurs.

---

## 2. Background computational ladder

The theorem program rests on the following established ladder.

### 2.1 Baseline rule

The baseline two-step action policy is monotone in normalized action distance on the sampled run, but it produces no nontrivial exact closure.

This established the first structural slogan:

> contraction without closure.

### 2.2 Exact-preference repair

Adding exact-preference resolves the dominant reachable frame-0 fringe.

On the sampled run this yields:

- 402 exact repairs out of 599 non-exact starts

So the dominant frame-0 failure was not geometric impossibility.
It was a policy-selection failure.

### 2.3 Residual frame-2 seam

After exact-preference, the residual near-action fringe at distance 1 is concentrated on frame 2 and has no exact one-edit closure.

This identifies frame 2 as the true bottleneck.

### 2.4 Feeder chambers

The deeper residual chambers do not remain separate.
By depth 4, the frame-1 / frame-4 side chamber feeds into the frame-2 near-action seam.

So the residual geometry is layered but convergent.

### 2.5 One-slot reduction

The frame-2 near-action witnesses are all Hamming-1 from the exact frame-2 target, and the mismatch is always at normalized position 4.

The exact frame-2 target requires:

- slot 4 = `t2`

So the entire residual closure problem reduces to a one-slot installation problem.

### 2.6 Corridor and escape-return probes

A strict corridor probe to depth 6 and a bounded escape-return sweep to depth 8 both fail to produce:

- exact frame-2 closure
- or the slot value `t2`

The bounded regime saturates by depth 6.

This is the backbone of the current obstruction result.

---

## 3. Definitions

We now formalize the objects needed for the theorem program.

### 3.1 Action representatives

For each frame \(i\), let \(A_i\) denote the exact action-cell representative at frame \(i\).

In particular, the frame-2 exact target is:

\[
A_2 = (o4,s4,t2,s2,t0,s0)
\]

up to normalization.

### 3.2 Normalization

Let \(N(c)\) denote the normalized form of a cycle \(c\), obtained by minimizing over cyclic rotations and reversal.

All structural statements below are phrased in normalized coordinates.

### 3.3 Normalized action distance

Define normalized action distance by

\[
d_A(c) := \min_i \operatorname{Ham}(N(c), N(A_i)),
\]

where \(\operatorname{Ham}\) is Hamming distance between normalized cycles of equal length.

This is the action-distance quantity used throughout the probes.

### 3.4 Frame-2 seam

Define the frame-2 seam by

\[
\Sigma_2 := \{\, c \mid c \text{ is action-cell nearest, } 2 \in F(c),\ d_A(c)=1 \,\},
\]

where \(F(c)\) is the set of nearest action frames returned by classification.

So \(\Sigma_2\) consists of cycles that are exactly one normalized coordinate away from the frame-2 action family and whose nearest action representatives include frame 2.

### 3.5 Slot projection

Define the normalized slot-4 projection by

\[
\pi_4(c) := N(c)_4.
\]

This is the local coordinate at which the lock appears.

### 3.6 Distinguished witness set

Define the locked witness subset \(W\) by the four normalized frame-2 seam states:

\[
W =
\{
(o4,s0,t0,s2,t4,s4),\,
(o4,s0,t0,s2,o4,s4),\,
(o4,s0,t0,s2,s3,s4),\,
(o4,s0,t0,s2,s0,s4)
\}.
\]

Each element of \(W\):

- lies in \(\Sigma_2\),
- is Hamming-1 from \(N(A_2)\),
- and differs from \(N(A_2)\) only at position 4.

### 3.7 Bounded escape-return regime

Let \(B\) be the bounded escape-return regime generated from \(W\) under the one-edit move grammar with the following admissibility rule:

- retain exact frame-2 states,
- otherwise retain states with normalized action distance at most 3.

Computationally, this regime saturates by depth 6.

This is the precise bounded regime for the current theorem program.

---

## 4. Empirical propositions already supported

The following propositions are now computationally supported.

### Proposition 4.1 (monotone contraction without nontrivial closure)
The baseline two-step rule is monotone in normalized action distance on the sampled run, but produces no nontrivial exact repairs.

### Proposition 4.2 (repairability of the dominant chamber)
The dominant frame-0 reachable chamber is repairable by exact-preference; hence the dominant baseline failure mode is policy-selection failure rather than geometric impossibility.

### Proposition 4.3 (frame-2 seam concentration)
After exact-preference, the residual near-action obstruction concentrates on frame 2.

### Proposition 4.4 (one-slot mismatch)
Every distinguished witness in \(W\) is Hamming-1 from \(N(A_2)\), and the unique mismatch occurs at normalized position 4.

### Proposition 4.5 (no exact one-edit closure on \(W\))
None of the four distinguished witnesses in \(W\) has an exact frame-2 one-edit child.

### Proposition 4.6 (bounded saturation)
The bounded escape-return regime \(B\) saturates computationally by depth 6; no additional states are found at depths 7 and 8.

### Proposition 4.7 (slot-4 exclusion in \(B\))
No state in \(B\) satisfies \(\pi_4(c)=t2\).

### Proposition 4.8 (no exact frame-2 closure in \(B\))
No state in \(B\) is exact frame 2.

Together these propositions form the current bounded obstruction result.

---

## 5. Alphabet formulation

The computational evidence becomes even cleaner when phrased symbolically.

### 5.1 Global bounded alphabet

Define the global slot-4 alphabet of the bounded regime by

\[
\mathcal A_B := \{\, \pi_4(c) \mid c \in B \,\}.
\]

The observed bounded alphabet is:

\[
\mathcal A_B =
\{o0,o1,o2,o3,o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

This is an almost-complete natural local family, but it excludes:

\[
t2.
\]

### 5.2 Seam alphabet

Define the seam slot-4 alphabet by

\[
\mathcal A_{\Sigma_2} := \{\, \pi_4(c) \mid c \in B \cap \Sigma_2 \,\}.
\]

The observed seam alphabet is:

\[
\mathcal A_{\Sigma_2} =
\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

Again, this excludes:

\[
t2.
\]

So the frame-2 seam supports a small, balanced wrong-value alphabet while excluding the exact key.

### Corollary 5.3 (unique key exclusion)
Within the saturated bounded regime, the exact closure key `t2` is uniquely excluded from the observed slot-4 symbol family relevant to frame-2 closure.

This is one of the strongest current corollaries.

---

## 6. The bounded obstruction theorem (computational form)

We can now state the main theorem-shaped claim.

### Theorem 6.1 (bounded frame-2 slot-4 exclusion law)
Let \(W\) be the distinguished locked frame-2 witness subset and let \(B\) be the bounded escape-return regime generated from \(W\) with normalized action-distance cap 3.

Then the following hold computationally:

1. \(B\) saturates by depth 6.
2. No state in \(B\) is exact frame 2.
3. No state in \(B\) satisfies \(\pi_4(c)=t2\).

Equivalently, within the saturated bounded regime, exact frame-2 closure fails because the required slot-4 key value `t2` never appears.

This is the strongest current bounded-regime theorem-shaped statement.

---

## 7. Chamber formulation

The local theorem should be read in the context of the full basin structure.

### Proposition 7.1 (layered chamber structure)
The sampled action geometry decomposes into:

1. a reachable frame-0 chamber, repaired by exact-preference;
2. a frame-2 near-action seam, where the residual closure obstruction concentrates;
3. deeper feeder chambers which funnel into the frame-2 seam by depth 4.

Thus the residual basin is layered, but converges on the same local bottleneck.

This ties the local obstruction theorem back to the global geometry.

---

## 8. Informative action corollary

The theorem also sharpens the meaning of informative action.

### Definition 8.1
Call a move policy **directionally informative** if its realized trajectories monotonically reduce normalized action distance.

Call a move policy **closure-sufficiently informative** if it additionally installs the exact local datum required for closure.

### Corollary 8.2 (direction without installation)
The sampled dynamics exhibit directionally informative action but not closure-sufficient informative action on the frame-2 seam.

That is:

- trajectories remain organized around the correct objective-adjacent chamber,
- but the exact local datum \(t2\) is not installed at normalized position 4 within the saturated bounded regime.

So the experiments distinguish:

- information that finds the lock,
from
- information that carries the key.

This is the cleanest current bridge from the computational results back to informative action.

---

## 9. Subjective / objective corollary

The theorem also refines the interpretation of the subjective–objective gap.

### Corollary 9.1 (localized closure gap)
After chamber-level alignment is achieved, the residual subjective–objective gap is not primarily global.
It localizes to the unsatisfied installation condition

\[
\pi_4(c)=t2
\]

on the frame-2 seam.

So the final gap is no longer one of broad directionality.
It is one of local closure content.

This is one of the strongest philosophical consequences of the theorem program.

---

## 10. Objective seam leakage corollary

The theorem also sharpens the meaning of objective seam leakage.

### Definition 10.1
Objective seam leakage is the transition behavior from seam-adjacent states that fails to produce exact closure and instead preserves wrong local slot values or spills into ambiguous neighboring regions.

### Corollary 10.2 (leakage as obstruction signature)
Objective seam leakage is the observable local signature of the frame-2 lock.

The computational evidence shows:

- stable wrong-value persistence on the seam,
- bounded local circulation among an 8-symbol seam alphabet,
- and exclusion of the exact key `t2`.

So seam leakage is no longer just metaphorical drift. It is the local behavioral signature of the one-slot obstruction.

---

## 11. Proof program

The current result is computationally saturated in the bounded regime, but not yet formally proved in a universal sense.

The next proof program is now clear.

### Step 1
Define the bounded regime \(B\) purely graph-theoretically, independent of the implementation details of the search scripts.

### Step 2
Prove that \(B\) is finite and that the search plateau corresponds to actual closure of the bounded reachable set.

### Step 3
Prove the slot-4 exclusion law:

\[
\forall c \in B,\ \pi_4(c) \neq t2.
\]

This is the central proof obligation.

### Step 4
Deduce exact closure exclusion:

if exact frame-2 closure requires \(\pi_4(c)=t2\), then no \(c\in B\) is exact frame 2.

### Step 5
Derive the seam alphabet analytically, if possible, and explain why `t2` is uniquely absent.

This would convert the current computational law into a real theorem.

---

## 12. What is now resolved

The following are now resolved at the bounded-regime level.

1. The frame-0 dominant reachable chamber is repairable.
2. The deeper side chambers funnel into frame 2.
3. The frame-2 bottleneck reduces to a one-slot mismatch at normalized position 4.
4. The distinguished locked witness subset \(W\) has no exact one-edit closure.
5. The bounded regime \(B\) saturates by depth 6.
6. The bounded regime contains no state with slot-4 value `t2`.
7. The bounded regime contains no exact frame-2 closure.
8. The frame-2 seam supports a balanced 8-symbol wrong-value alphabet.

This is already a substantial theorem ladder.

---

## 13. What remains open

The following remain open.

1. Whether `t2` becomes reachable only in a qualitatively broader regime than the bounded one.
2. Whether there is a symbolic, parity-like, orbit-like, or transport-law explanation for the exclusion of `t2`.
3. Whether the seam alphabet can be derived analytically rather than only observed computationally.
4. Whether the bounded obstruction theorem can be made fully formal without expanding the regime.

These are now the right next mathematical questions.

---

## 14. Best short theorem summary

After exact-preference repairs the dominant reachable chamber, the residual basin funnels into a frame-2 seam whose bounded escape-return regime saturates by depth 6.

Within that saturated regime:

- the exact slot value `t2` at normalized position 4 never appears,
- exact frame-2 closure never occurs,
- and the seam supports only a balanced 8-symbol wrong-value alphabet.

So the current evidence supports a bounded-regime one-slot exclusion law for frame 2.

Or more compactly:

> the seam is found, the basin saturates, and the key is uniquely excluded.

