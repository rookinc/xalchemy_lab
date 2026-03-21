# Kernel, Not Cocycle Note

## Context

The tri-patch transport program began by uncovering:

1. an exact bundled affine rail
2. a semilinear defect algebra on that rail
3. an additive holonomy lattice for admissible off-rail route classes
4. a binary parity shadow on that lattice

The parity law was then solved explicitly:

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

So every observed local holonomy class has **even total mismatch parity**.

This immediately suggested a possible bridge to the broader Thalean / signed-lift \(\mathbb Z_2\) cocycle.

The natural question was:

> Is the local tri-patch parity law the cocycle itself, or only a shadow of it?

This note records the answer reached so far.

---

## 1. What the global cocycle does

On the signed-lift side, the project already has a genuine \(\mathbb Z_2\)-valued cocycle associated with loop transport.

That object is:

- global
- loop-sensitive
- not reducible to local scalar overlap data alone
- and known to take nontrivial values on some cycles

So the global cocycle can distinguish an odd sector from an even sector.

That is important.

It means the global binary object is not merely a “kernel law.”
It is a true binary observable.

---

## 2. What the local parity law does

On the local tri-patch side, every observed reachable holonomy class satisfies:

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0 \pmod 2.
\]

So the local transport system enforces a binary selection rule:

> odd total mismatch parity is forbidden.

This is already nontrivial.
It means the local holonomy lattice has a codimension-1 binary shadow.

But this still leaves open two possibilities:

### Possibility A
The local law is the cocycle itself in disguised form.

### Possibility B
The local law is only the kernel of the cocycle, not the cocycle value.

The recent tests now strongly favor **Possibility B**.

---

## 3. First failed bridge attempt: raw local classes

A naive bridge would say:

\[
\omega(\gamma) = dm_{L1}+dm_{L2}+dm_{R1}\pmod 2
\]

for a local route class \(\gamma\).

But this cannot be correct.

Why:

- the global cocycle can be odd on some loops
- the local tri-patch route classes are **always even** in total mismatch parity

So raw local holonomy classes do not realize the odd sector at all.

That kills the simplest identification.

---

## 4. Second failed bridge attempt: local route differences

A more refined bridge idea was:

> perhaps the cocycle is not attached to a single local class, but to the difference between two admissible local histories with the same endpoints.

That is more plausible in spirit, because the global cocycle is loop/history sensitive.

So pairwise route-difference probes were run.

Result:

- every tested route difference still had even total mismatch parity
- no odd binary value appeared

So the route-difference sector still lives entirely inside the same even kernel.

That means the odd global cocycle bit is still absent.

---

## 5. Third failed bridge attempt: composite local words

The next escalation was to compare longer composite route words.

Word-length-3 local comparisons were tested.

Result:

- many composite local word pairs were checked
- still **no odd total mismatch parity** appeared

So longer local word differences still do not realize the odd sector.

This matters because it shows the even-kernel behavior is not just a one-step artifact.

---

## 6. Fourth failed bridge attempt: stitched local charts

The next natural move was to stitch together two local charts.

This was meant to simulate a larger local loop:
- first run one local word,
- flip chart polarity / anchor,
- then run a second local word,
- compare stitched composite histories.

This is much closer to the kind of structure where a global bit might plausibly appear.

But the result was again decisive:

- millions of comparable stitched pairs were checked
- still **zero** odd-total-mismatch examples appeared

So even stitched local chart transport remains trapped in the even kernel.

---

## 7. What this means

The evidence now points to a strong conclusion:

> The tri-patch transport system models the **kernel** of the global signed-lift \(\mathbb Z_2\) cocycle, not the cocycle value itself.

That is, the local system sees the binary constraint

\[
\omega = 0,
\]

but does not yet have enough structure to generate or detect the \(\omega = 1\) sector.

In plain language:

- the local model knows what is allowed
- but it does not yet know how to flip sheets

---

## 8. Best current interpretation

The most coherent interpretation is this:

### Local model
The tri-patch carries:

- affine transport
- defect transport
- additive route holonomy
- even-mismatch parity selection

This is a local transport shadow.

### Missing ingredient
The odd global bit likely requires data that the current local transport model does not contain.

Most plausibly one of:

1. **sheet / lift register**
2. **global loop closure data**
3. **explicit signed-lift state**
4. **inter-patch transition law not captured by naive chart stitching**

So the current model is not wrong.
It is incomplete relative to the full global binary observable.

---

## 9. Why “kernel” is the right word

The word **kernel** is appropriate because:

- the local parity law does not produce arbitrary \(\mathbb Z_2\) values
- instead it selects exactly the even sector
- every tested local comparison lives inside that sector

So the local law behaves like the condition

\[
\omega(\gamma)=0
\]

rather than like the full map \(\omega(\gamma)\in\mathbb Z_2\).

That is exactly what a kernel is.

---

## 10. Structural summary

The current local–global picture is now:

### Global side
A genuine \(\mathbb Z_2\)-valued cocycle on signed-lift loops, with both even and odd sectors.

### Local side
A tri-patch transport system whose holonomy corrections satisfy

\[
dm_{L1}+dm_{L2}+dm_{R1}\equiv 0\pmod 2.
\]

### Bridge relation
The local side appears to realize only the **even sector** of the global binary law.

So the bridge is not:

> local parity = global cocycle value

but rather:

> local parity law = kernel condition of the global cocycle.

---

## 11. Conjecture

### Kernel Not Cocycle Conjecture

The tri-patch transport model realizes the kernel of the global signed-lift \(\mathbb Z_2\) cocycle.
The odd cocycle sector is not visible in the current local transport state space and requires additional lift/sheet information or genuinely global loop closure data.

That is the current best conjecture.

---

## 12. What this suggests next

The next development should not be more brute-force route enumeration on the current state space.

The missing ingredient must be added explicitly.

The most likely next step is to augment the transport model with a **binary lift register** or **sheet flag**.

Then test:

- whether that extra bit can toggle under appropriate stitched transport
- whether odd cocycle-like classes can finally appear
- whether the even-mismatch law survives as the kernel condition of that augmented model

That would be the first real attempt to move from kernel to cocycle.

---

## 13. Working summary

The strongest current conclusion is:

> **The tri-patch transport system appears to model the kernel, not the cocycle.**

More explicitly:

- local transport is rich enough to discover the binary selection rule
- but not rich enough to generate the odd binary sector
- so the missing global \(\mathbb Z_2\) information must live in additional lift-aware structure

That is where the next phase begins.

