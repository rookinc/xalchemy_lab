# Triadic Closure Rule Proposition
## Current local rule extracted from the patch experiments

This note records the present local rule suggested by the recent `xalchemy_lab` patch tests.

It is a proposition about the toy.
It is not yet a proof.
It is the cleanest rule statement supported by the observed traces.

---

# Proposition (current toy form)

Let `H` be a signed hub in the patch, with hub sign `σ(H) ∈ {+, -}`.

Suppose three turtles are assembled at `H`, producing a triadic event `LLR @ H`.

Then the toy presently supports the following rule:

## 1. Closure admissibility
**Triadic co-presence is sufficient for closure.**

That is, once a true three-body assembly occurs at a signed hub, the hub closes.
The triad does not need:
- simultaneous arrival,
- uninterrupted staging,
- or a unique path history.

Broken staging, delayed arrival, and partial assembly all remained closure-capable once the triad was eventually assembled.

---

## 2. Sign normalization
**The hub normalizes the outgoing triad to its own sign.**

If the closure occurs at a positive hub, the outgoing signs become:
- `+,+,+`

If the closure occurs at a negative hub, the outgoing signs become:
- `-,-,-`

This appears to hold even when the incoming triad is sign-mixed.

---

## 3. Closure class
The hub supports two closure classes:

- `ABCσ_closed`
- `ABCσ_tension`

The evidence now suggests:

### Clean closure criterion
A triad closes cleanly exactly when it arrives with:

- sign coherence with the hub closure state, and
- zero active mismatch burden

### Tension closure criterion
A triad closes under tension when mismatch is present or induced.

This includes at least two experimentally confirmed cases:

1. **pre-existing mismatch**
2. **incoming sign incoherence that generates mismatch locally**

---

# Equivalent local rule

A compact way to state the current law is:

**Every triad closes at a signed hub.  
The hub normalizes sign to its own polarity.  
Closure is clean iff mismatch is zero.  
Otherwise closure is tensioned.**

---

# Evidence by case

## Case A: coherent triad, zero mismatch
Observed result:
- `ABC+_closed`

Behavior:
- no sign inversion burden
- no mismatch increase
- carried stress can be discharged
- closure counted as clean

This is the clean reference case.

---

## Case B: coherent triad, nonzero mismatch
Observed result:
- `ABC+_tension`

Behavior:
- incoming visible signs can still be `+,+,+`
- but nonzero mismatch residue is enough to force tension
- carried stress is created on closure

This shows that visible sign coherence alone is not sufficient for clean closure.

---

## Case C: mixed-sign triad, zero prior mismatch
Observed result:
- `ABC+_tension`

Behavior:
- incoming signs such as `-,+,-`
- incoming mismatch can be artificially set to zero
- the hub itself creates mismatch locally
- outgoing signs normalize to `+,+,+`

This shows that sign incoherence is a direct local source of mismatch at closure.

---

## Case D: coherent triad with carried stress only
Observed result:
- `ABC+_closed`

Behavior:
- coherent signs
- nonzero incoming carried stress
- stress can be discharged rather than amplified
- no forced tension if mismatch is zero

This shows:

**stress alone is not sufficient to force tension.**

---

# Working interpretation

The experiments support the following hierarchy:

## Primary gate
- triadic occupancy at a signed hub

## Primary burden variable
- mismatch

## Local source of mismatch
- sign incoherence at the closure site

## Secondary transported cargo
- carried stress

So the best current interpretation is:

**Mismatch is the burden variable.  
Sign incoherence is a local producer of mismatch.  
Stress is cargo that can be discharged in clean closure or loaded further in tension closure.**

---

# Minimal case form

Let `M` denote whether total mismatch burden at closure is zero or nonzero.

Then the current toy law is approximately:

- if triad assembled and `M = 0`, then `ABCσ_closed`
- if triad assembled and `M > 0`, then `ABCσ_tension`

with the additional observation that:
- incoming sign incoherence can itself create `M > 0` at the closure event.

---

# Compact slogan

The shortest faithful version is:

**Triads always close.  
The hub sets the sign.  
Mismatch chooses the flavor.**

A slightly more descriptive version is:

**Closure normalizes; mismatch loads.**

---

# Next mathematical target

The natural next step is to move from scenario language to a local state functional.

The question is now:

**Can the closure class be written as a deterministic function of local triad state, for example**
- hub sign,
- occupancy,
- incoming sign pattern,
- total mismatch,
- carried stress,
- stored tension?

The current experiments suggest that such a local classification should be possible.

