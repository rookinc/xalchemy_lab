# G15 / G30 Minimal Machine

## Status
Locked working core

## Purpose

This note freezes the smallest non-conjectural machine currently supported by the project conversation.

The goal is not to explain everything.
The goal is to isolate the minimal cycle law that can be treated as a working structural backbone.

This note therefore stops at G15 and G30.

Anything beyond that is explicitly marked as conjectural.

---

## 1. Core machine

Let \(W\) denote one full G15 cycle operator acting on the current walker state.

The locked rule is:

\[
W(n) = -n
\]

Applying the cycle twice restores identity:

\[
W^2(n) = n
\]

Equivalently, in the indexed notation already in use:

\[
n_{15} = -n_0
\]
\[
n_{30} = n_0
\]

This is the minimal machine.

---

## 2. Meaning of the minus sign

The symbol

\[
-n
\]

does **not** mean ordinary arithmetic negation.

It means:

> same host site, opposite sidedness or opposite sheet orientation

So one full G15 cycle returns to the same lawful host location, but on the opposite side of the sheet from the starting stance.

The second cycle flips that sidedness again and restores the original state.

Thus:

- one cycle is **sign-closing**
- two cycles are **identity-restoring**

---

## 3. What is locked

The following statements are now treated as the locked working core.

### 3.1 One-cycle rule
\[
n_{15} = -n_0
\]

### 3.2 Two-cycle rule
\[
n_{30} = n_0
\]

### 3.3 Meaning of G15
G15 is the sign-closing host cycle.

### 3.4 Meaning of G30
G30 is the identity-restoring double cycle.

### 3.5 Reverse traversal
If one full forward cycle carries \(n_0\) to \(-n_0\), then reverse traversal is an inverse mode returning the walker to the original stance.

So there is a meaningful distinction between:
- forward completion
- reverse unwinding

### 3.6 Post-G30 relaunch
Once \(n_{30}=n_0\), the walker is restored to a lawful launch stance and may be relaunched under a new heading choice.

This makes G30 a hinge.

---

## 4. Minimal state language

The machine only requires a very light state language.

At minimum, a state must distinguish:

- host placement
- sidedness

So the minimal state can be written schematically as:

\[
n = (x,\varepsilon)
\]

where:

- \(x\) = host placement or local host role
- \(\varepsilon \in \{+,-\}\) = sidedness

Then the cycle law is simply:

\[
W(x,\varepsilon) = (x,-\varepsilon)
\]

and therefore:

\[
W^2(x,\varepsilon) = (x,\varepsilon)
\]

No larger machinery is required to state the minimal machine.

---

## 5. What this does not yet claim

This note does **not** yet claim:

- a full face-transport formalism
- a full chamber/heading model
- a proof of left/right chirality assignment
- a proof of G60
- a proof of geodesic propagation
- a proof that AT4val[60,6] realizes the larger state space

Those are all beyond the minimal machine.

---

## 6. Locked versus conjectural boundary

### Locked working core
- one G15 cycle is sign-closing
- two G15 cycles restore identity
- G30 is the restored hinge
- post-G30 relaunch is meaningful

### Conjectural extension
- exact left/right inward-outward assignment
- geodesic of superpositions
- neighboring-host witness propagation as a formal theorem
- G60 as subjective closure plus objective extension
- AT4val[60,6] as realization of a higher resolved host state space

This boundary should be preserved going forward.

---

## 7. G30 as hinge

Because

\[
n_{30}=n_0
\]

G30 is not merely “the same thing twice.”

It is the first point at which the walker is restored to original stance and may make a fresh lawful heading choice.

So G30 is the restored hinge of the system.

From G30, the walker may choose:
- no turn
- 90-degree turn
- 180-degree turn
- 270-degree turn

These define new launch classes to be tested.

---

## 8. Four post-G30 launch classes

Let the restored state after G30 be \(n_0\) with heading \(h\).

Then define four relaunch classes:

### Class 0
\[
(n_0,h)
\]

This is the recovered original launch.

### Class 90
\[
(n_0,R_{90}(h))
\]

This is the quarter-turned relaunch.

### Class 180
\[
(n_0,R_{180}(h))
\]

This is the inverted or shadow-facing relaunch.

### Class 270
\[
(n_0,R_{270}(h))
\]

This is the opposite quarter-turned relaunch.

These classes are not yet fully formalized, but they are the correct next experiment inside the minimal machine.

---

## 9. Immediate next experiment

The next experiment is:

> classify the four post-G30 relaunches

The expected working classification is:

- 0° = original recovery class
- 180° = inverse / shadow class
- 90° = orthogonal companion class
- 270° = opposite orthogonal companion class

This classification is still exploratory, but it stays close to the locked machine and does not require jumping into higher conjectures.

---

## 10. Plain-language summary

One time around, I come back on the other side of myself.

Two times around, I come back to myself.

That is the whole minimal machine.

Everything else should be built only after keeping that core fixed.

---

## 11. One-line locked rule

\[
W(n)=-n,\qquad W^2(n)=n
\]

This is the minimal G15/G30 machine.

