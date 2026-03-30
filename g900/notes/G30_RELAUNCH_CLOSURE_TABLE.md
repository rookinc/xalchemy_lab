# G30 Relaunch Closure Table

## Status
Working test note

## Purpose

This note defines the next strictly mathematical test after the G15/G30 minimal machine.

The aim is to classify the four post-G30 relaunches without relying on internal orientation intuition.

We do not yet ask which relaunch is “inward,” “outward,” “shadow,” or “geodesic.”

We ask only:

- does it close?
- if it closes, how?
- if it does not close, what orbit behavior does it show?

This note is therefore intentionally neutral.

---

## Locked core

Let \(W\) denote one full G15 cycle operator.

The locked working machine is:

\[
W(n) = -n
\]
\[
W^2(n) = n
\]

Equivalently:

\[
n_{15} = -n_0
\]
\[
n_{30} = n_0
\]

This is the only structural law currently treated as locked.

---

## Restored hinge

After two full G15 passes, the walker returns to the lawful restored state:

\[
n_{30} = n_0
\]

This restored state is the hinge from which all relaunch tests begin.

So every relaunch below must be understood as beginning from the same restored state.

That is what makes the comparison fair.

---

## Relaunch operators

Define four abstract relaunch operators:

\[
Q_0,\ Q_{90},\ Q_{180},\ Q_{270}
\]

with the meanings:

- \(Q_0\): relaunch from the restored state with original recovered heading
- \(Q_{90}\): relaunch from the restored state with heading rotated by 90 degrees
- \(Q_{180}\): relaunch from the restored state with heading rotated by 180 degrees
- \(Q_{270}\): relaunch from the restored state with heading rotated by 270 degrees

At this stage these are purely formal heading classes.

No geometric interpretation is assumed yet.

---

## Test operators

For each relaunch class, define the corresponding cycle test:

\[
W_0 = W \circ Q_0
\]
\[
W_{90} = W \circ Q_{90}
\]
\[
W_{180} = W \circ Q_{180}
\]
\[
W_{270} = W \circ Q_{270}
\]

These are the four objects to classify.

---

## Questions to ask for each relaunch

For each \(W_\theta\), ask the following in order.

### Q1. One-pass closure
Does one relaunch cycle give

\[
W_\theta(n_0) = -n_0
\]

?

### Q2. Two-pass restoration
Does two relaunch cycles give

\[
W_\theta^2(n_0) = n_0
\]

?

### Q3. Alternate closure
If not, does the relaunch close to some other lawful state or orbit class?

### Q4. Orbit transfer
If not, does the relaunch transfer into a neighboring or companion orbit?

### Q5. Non-closure
If no closure appears in the tested period, does the relaunch remain non-closing?

These are the only questions under test here.

---

## Allowed outcome types

Each relaunch should be classified into one of the following neutral categories.

### Type A. Sign-closing
\[
W_\theta(n_0) = -n_0
\]

This means one pass returns the sign-flipped original state.

### Type B. Identity-restoring in two passes
\[
W_\theta^2(n_0) = n_0
\]

This means the relaunch reproduces the same two-pass restoration law as the base machine.

### Type C. Different closed orbit
The relaunch closes, but not to the original state class within 15 or 30 steps.

### Type D. Non-closing in tested period
The relaunch does not close within the tested period.

### Type E. Orbit transfer
The relaunch leaves the original orbit class and enters a different lawful orbit or companion chain.

These are meant to be descriptive, not interpretive.

---

## Neutral classification table

\[
\begin{array}{c|c|c|c}
\text{Relaunch} & \text{15-step result} & \text{30-step result} & \text{Classification} \\
\hline
Q_0 & ? & ? & ? \\
Q_{90} & ? & ? & ? \\
Q_{180} & ? & ? & ? \\
Q_{270} & ? & ? & ?
\end{array}
\]

This is the primary table to fill.

---

## Strong discipline rule

While this table is being filled, do **not** assign names such as:

- inward
- outward
- shadow
- side-channel
- geodesic
- coherence
- emission
- contraction
- expansion

Those words may become useful later, but only after the closure behavior is known.

For now, only use neutral mathematical language:

- sign-closing
- identity-restoring
- different closed orbit
- orbit transfer
- non-closing in tested period

---

## Expected baseline

The current cautious baseline is:

- \(Q_0\) is expected to reproduce the locked machine
- \(Q_{180}\) may be related to inverse or companion behavior
- \(Q_{90}\) and \(Q_{270}\) are genuinely open

This is not yet a result.
It is only the current testing posture.

---

## Why this matters

The system will become much clearer once the relaunch classes are separated by closure type rather than by intuition.

At present, internal visualization has become unreliable enough that interpretation must yield to closure behavior.

So this note marks the point where the project proceeds by neutral classification first.

Only after the table is filled should any geometric or philosophical interpretation be promoted.

---

## Immediate next procedure

For each relaunch \(Q_\theta\):

1. start from the restored state \(n_0\)
2. relaunch with the chosen heading class
3. run one cycle
4. test whether the result is \(-n_0\)
5. if not, run a second cycle
6. test whether the result is \(n_0\)
7. if not, classify whether the relaunch has entered another orbit or remains non-closing

This is the next clean mathematical program.

---

## One-line principle

Follow closure first.
Interpretation second.

