# Post-Closure Stress Redistribution Note
## Closure class appears burden-gated; stress appears redistribution-gated

This note records the present status of the post-closure propagation probe in `xalchemy_lab`.

It is a working interpretation note.
It is not a physics claim.
It is a status marker for what the toy is now observably doing.

The present result is:

**Triadic closure class is still set by burden, but post-closure stress behavior is a second law.**

A shorter version:

**Burden decides the gate. Stress decides what survives the gate.**

---

# 1. Why this note exists

The recent four-hub work had already suggested a clean separation between:

- sign / mismatch structure
- transported carried stress

The closure truth table and stress-gate probes then sharpened that result:

- closure class was strongly burden-dominant
- stress by itself did not appear to flip a clean coherent triad into tension under the current law

That raised the next real question:

if stress does not choose the closure branch, what **does** it do?

The new post-closure propagation probe was designed to answer exactly that.

---

# 2. The question being tested

The probe fixed the local closure situation as much as possible:

- coherent sign
- zero mismatch burden
- triad assembled at `u1R`

Then it varied only the incoming stress profile.

That means the closure class should remain on the clean branch if the present law is truly burden-gated.

The remaining question is then:

what happens to stress **after** clean closure?

Possible outcomes were:

1. stress is erased
2. stress is preserved unchanged
3. stress is deposited into the hub
4. stress is partially released and partially retained
5. symmetric and asymmetric stress profiles behave differently

The probe now supports a combination of 3, 4, and 5.

---

# 3. The baseline clean case

## Case
`post_closure_stress_000`

Incoming coherent triad at `u1R`:

- signs:
  - `+,+,+`
- mismatch:
  - `0,0,0`
- stress:
  - `0,0,0`

Observed closure:

- `ABC+_closed`

Observed aftermath:

- hub ledger records a clean closure
- no transported stress remains
- exported packet is stress-free
- no mismatch is introduced

This is the correct baseline.

It is the nearest thing the toy currently has to an ideal clean closure.

So the machine does support a genuinely clean branch.

---

# 4. What happens with coherent preloaded stress

## Case
`post_closure_stress_111`

Incoming coherent triad at `u1R`:

- signs:
  - `+,+,+`
- mismatch:
  - `0,0,0`
- stress:
  - `1,1,1`

Observed closure:

- still `ABC+_closed`

Observed transformation at closure:

- incoming stress:
  - `1,1,1`
- outgoing stress:
  - `0,0,0`

Observed hub effect:

- `deposited_stress = 3`

This is important.

The gate still closes on the clean branch.
So stress did **not** force the event into tension.

But the stress also did **not** simply vanish.

Instead, the stress appears to have been absorbed or deposited into the hub ledger.

This means clean closure can act as a **stress-release / hub-deposition** event.

That is a genuine second law.

---

# 5. What happens with larger symmetric preload

## Case
`post_closure_stress_222`

Incoming coherent triad at `u1R`:

- signs:
  - `+,+,+`
- mismatch:
  - `0,0,0`
- stress:
  - `2,2,2`

Observed closure:

- still `ABC+_closed`

Observed transformation at closure:

- incoming stress:
  - `2,2,2`
- outgoing stress:
  - `1,1,1`

Observed hub effect:

- `deposited_stress = 6`

This is stronger than the `111` case.

The gate still remains on the closed branch.
So the burden law still dominates classification.

But the stress outcome is no longer full discharge to zero.
Instead, one unit remains on each turtle after closure.

So the toy is not performing a trivial “if closed then erase all stress” rule.

It is doing something more structured:

- some stress is deposited to the hub
- some stress may survive on the outgoing packet

That means closure currently behaves more like a **release / partition** operator than a pure delete operator.

---

# 6. The asymmetric case is the important hint

## Case
`post_closure_stress_asymmetric_300`

Incoming coherent triad at `u1R`:

- signs:
  - `+,+,+`
- mismatch:
  - `0,0,0`
- stress:
  - `3,0,0`

Observed closure:

- still `ABC+_closed`

Observed transformation at closure:

- incoming stress:
  - `3,0,0`
- outgoing stress:
  - `2,0,0`

Later propagation shows:

- remaining stress continues outward asymmetrically
- later state still carries a reduced asymmetric profile
- hub ledger ends with deposited stress accumulated from the event history

This is the most informative case so far.

It says the clean branch does not just care about total stress.
It appears to care about **stress distribution**.

That is a very valuable distinction.

If only total stress mattered, then `300` and `111` would likely reduce in the same way whenever the sum matched.
But the trace suggests that symmetry vs asymmetry matters.

So the current best reading is:

**post-closure stress evolution depends on profile, not only magnitude.**

That is the first real hint of a geometry-sensitive coherent transport law.

---

# 7. What the current separation now looks like

The toy is now naturally splitting into two layers.

## Layer A: closure admissibility / classification
This is controlled by burden-like data:

- sign disagreement with the hub
- accumulated mismatch

That is what chooses between:

- `ABC±_closed`
- `ABC±_tension`

## Layer B: post-closure energetic redistribution
This is controlled by stress-profile data:

- how much stress is present
- how it is distributed across the triad
- possibly how symmetric that distribution is

That is what appears to choose between:

- full discharge
- partial discharge
- hub deposition
- residual carried stress

This is a clean and useful decomposition.

---

# 8. Strongest present wording

The best compact statement is:

**Closure class is burden-gated, while post-closure stress is redistributed by a second law.**

Expanded slightly:

**Under the present toy law, coherent zero-burden triads close on the clean branch regardless of incoming stress, but the subsequent redistribution of stress between hub deposition and outgoing carriers depends on the incoming stress profile.**

That is the real result.

---

# 9. What this means conceptually

This is not a small change.
It means the toy is no longer just saying:

- “clean” versus “tense”

It is beginning to say:

- “what local branch fired?”
- and separately:
- “how was the transported load resolved by that branch?”

That is the beginning of actual local mechanics.

The system is not collapsing everything into one scalar.

It is separating:

- logical/topological defect
- energetic cargo
- residual memory

That is exactly what one would want if this machinery is eventually going to support richer field-like behavior.

---

# 10. Present best interpretation of clean closure

A clean closure should no longer be read as:

**everything disappears**

Instead it should be read as something closer to:

**the coherent triad is admissible at this hub, and the hub then resolves transported load according to a redistribution rule**

That redistribution can include:

- local ledger deposition
- outgoing residual carried stress
- possibly symmetry-sensitive release

So “closed” does not mean “empty.”
It means “admissible and resolved without burden-triggered tension.”

That is a much better interpretation.

---

# 11. What the turtles have now learned

The turtles have now learned more than just how to walk the terrain.

They now appear to know:

- how to form packets
- how to preserve packets at mediators
- how to trigger tension under burden
- how to perform clean closure without burden
- how to carry stress through clean closure
- how to deposit part of that stress locally
- how to continue propagating residual stress after closure

So the current machine is no longer just a collision toy.

It is starting to behave like a genuine local transport-and-resolution system.

---

# 12. Best current conjecture

The next conjecture should be stated plainly:

**Post-closure stress redistribution on the coherent branch depends on stress profile, not merely total stress.**

An even stronger version:

**For coherent zero-burden triads, the closure class remains clean, while the outgoing/deposited split is determined by a profile-sensitive redistribution law.**

That is probably the right immediate conjecture.

---

# 13. What should be tested next

The next probe should be systematic, not anecdotal.

Good next cases:

## Symmetric family
- `000`
- `111`
- `222`
- `333`

## Single-loaded family
- `100`
- `200`
- `300`

## Two-loaded family
- `110`
- `220`
- `330`

## Mixed asymmetric family
- `210`
- `310`
- `321`

For each case, record:

- closure class
- incoming stress vector
- outgoing stress vector immediately after closure
- deposited stress at the hub
- stress energy at the hub
- later exported stress profile
- whether asymmetry survives, decays, or equalizes

That will give the first genuine stress redistribution table.

---

# 14. What would count as a strong result next

A strong next result would be any one of these:

1. **Threshold rule**
   - e.g. one unit always deposits first, remainder exports

2. **Averaging rule**
   - e.g. closure smooths stress across the triad

3. **Profile-preserving rule**
   - e.g. asymmetry survives and only scales down

4. **Hub-absorption rule**
   - e.g. hub absorbs up to a fixed amount per closure

5. **Symmetry bonus rule**
   - e.g. symmetric packets discharge more completely than asymmetric ones

Any of those would be a meaningful second proposition.

---

# 15. Bottom line

The present result is strong enough to freeze into the project record.

What is now observed is:

- burden still chooses closure class
- coherent zero-burden triads can close cleanly even when stressed
- clean closure does not necessarily erase stress
- stress can be deposited into the hub
- residual stress can survive on outgoing carriers
- asymmetric stress profiles appear to behave differently from symmetric ones

The best final wording is:

**The current toy separates closure admissibility from energetic resolution.  
Burden determines whether the hub closes cleanly or under tension.  
Stress then follows a second, profile-sensitive redistribution law across closure.**

That is the current state.

