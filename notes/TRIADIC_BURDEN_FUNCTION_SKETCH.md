# Triadic Burden Function Sketch
## Toward a local state functional for closure class

This note records the next mathematical compression step after the recent 4-hub patch experiments.

The question is no longer merely which scenarios work.

The question is:

**Can the closure class at a signed hub be written as a deterministic local function of the incoming triad state?**

---

# 1. Local closure picture

Let `H` be a signed hub with sign `σ(H) ∈ {+, -}`.

Let `T = (t1, t2, t3)` be a triad assembled at `H`.

The experiments now support three distinct outputs at closure:

1. closure occurs
2. outgoing sign is normalized to `σ(H)`
3. closure class is either:
   - `ABCσ_closed`
   - `ABCσ_tension`

So the local rule appears to factor into:

- an admissibility condition
- a normalization rule
- a closure-class rule

---

# 2. Admissibility rule

Current evidence supports:

**Triadic occupancy at a signed hub is sufficient for closure.**

That is, once an actual three-body assembly occurs at a signed hub, closure happens.

This appears insensitive to:
- exact arrival simultaneity
- broken staging
- delayed third arrival
- route history

provided the triad is eventually assembled.

So the first gate can be written schematically as:

`Admissible(H, T) = 1` iff `|T| = 3` at a signed hub.

---

# 3. Normalization rule

Current evidence supports:

**The outgoing closure sign is the hub sign.**

So if closure occurs at:
- a positive hub, outgoing signs become `+,+,+`
- a negative hub, outgoing signs become `-,-,-`

This holds even when the incoming triad is sign-mixed.

So the second rule is approximately:

`OutgoingSign(H, T) = σ(H)`

applied to all three turtles.

---

# 4. Closure-class rule

This is now the main target.

The experiments suggest:

- coherent triad with zero mismatch -> `closed`
- coherent triad with nonzero mismatch -> `tension`
- mixed-sign triad with zero prior mismatch -> `tension`
- mixed-sign triad induces mismatch locally at closure
- carried stress alone does not force tension if mismatch is zero

This strongly suggests that the decisive variable is a local **burden** quantity.

---

# 5. Candidate burden variable

The cleanest first candidate is:

`B(T,H) = total mismatch burden at closure`

with the understanding that this burden may include:

1. **pre-existing mismatch residue**
2. **mismatch induced locally by sign incoherence with respect to the hub sign**

So the current first-pass law is:

- `ABCσ_closed` iff `B(T,H) = 0`
- `ABCσ_tension` iff `B(T,H) > 0`

This is the strongest compact rule supported so far.

---

# 6. Induced mismatch

The experiments further suggest that sign incoherence is not merely correlated with mismatch.

It can create mismatch at the closure site itself.

In particular:
- an artificially prepared mixed-sign triad with zero prior mismatch
- still closed under tension
- and mismatch appeared immediately at the event

So sign incoherence seems to act as a **local source term** for burden.

That suggests a decomposition like:

`B(T,H) = M_prior(T) + M_induced(T,H)`

where:
- `M_prior(T)` is incoming mismatch residue
- `M_induced(T,H)` is mismatch created at closure by sign disagreement relative to hub polarity

---

# 7. Role of carried stress

The current tests suggest that carried stress is not the primary gate variable.

Evidence:
- coherent triad + carried stress can still close cleanly
- mixed-sign or mismatched triads close under tension
- tension closure can increase carried stress
- clean closure can discharge carried stress

So the present best interpretation is:

**stress is cargo, not the main closure classifier**

though it may still couple to ledger loading and post-closure export.

---

# 8. First functional form

The simplest present form is:

## Admissibility
`A(H,T) = 1` iff signed hub and triadic occupancy

## Outgoing sign
`S_out(H,T) = σ(H)`

## Burden
`B(H,T) = M_prior(T) + M_induced(T,H)`

## Closure class
- if `A(H,T)=1` and `B(H,T)=0`, then `ABCσ_closed`
- if `A(H,T)=1` and `B(H,T)>0`, then `ABCσ_tension`

This is not yet a proof.
It is the current best state-functional sketch supported by the traces.

---

# 9. Best compact wording

The local law currently appears to be:

**Every triad at a signed hub closes.  
The hub sets the sign.  
Burden chooses clean versus tension.  
Mismatch is the main burden variable.**

---

# 10. Immediate next technical step

The next implementation step is to mirror this in code.

In particular, the closure logic should be refactored into named helpers such as:

- `triad_induced_mismatch(...)`
- `triad_burden(...)`
- `triad_closure_class(...)`

That would bring the code and the notes into direct alignment.

