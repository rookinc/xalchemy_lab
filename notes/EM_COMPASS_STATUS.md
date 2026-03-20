# EM Compass Status
## Tri-turtle polarity, tension, stress transport, and damping
## Verbose working note

This note summarizes the current state of the tri-turtle machinery toy as it now stands in `xalchemy_lab`.

It is not a proof of physics.
It is not a claim about electromagnetism.
It is a structured status note for a toy system whose behavior is now rich enough to justify an EM-inspired vocabulary.

The right framing is:

- we are using electromagnetism as a **compass**
- not as an identity claim
- not as an interpretive shortcut
- not as permission to smuggle in Maxwell before the toy earns it

The toy has now reached a point where it supports meaningful distinctions among:

- local polarity
- transported polarity
- mismatch
- tensioned closure
- discharge
- hub-local stress
- turtle-borne stress
- stress deposition
- free-flight damping

That is enough structure to pause and write down what the machine is actually doing.

---

# 1. Minimal scaffold

The current local scaffold is the small two-hub transport graph:

- upper chain:
  - `u3L -> u2L -> u1T`
  - `u3R -> u2R -> u1T`

- lower chain:
  - `d3L -> d2L -> d1T`
  - `d3R -> d2R -> d1T`

- spine:
  - `u1T <-> d1T`

The class-1 hubs are:

- `u1T`
- `d1T`

The class-2 nodes are:

- `u2L`, `u2R`, `d2L`, `d2R`

The class-3 nodes are:

- `u3L`, `u3R`, `d3L`, `d3R`

The hub polarity assignment is currently:

- `u1T = +`
- `d1T = -`

This assignment is not yet a theorem. It is a modeling choice that has produced useful behavior.

---

# 2. Turtles

There are three turtles in the current toy:

- `L1` : left-chiral turtle
- `L2` : left-chiral turtle
- `R1` : right-chiral turtle

The important point is not “left” and “right” as physical handedness in a finished theory. The important point is that the toy distinguishes:

- same-hand interaction (`LL`)
- mixed-hand interaction (`LR`)
- triple interaction (`LLR`)

The initial successful configuration was:

- `L1 @ u3L`
- `L2 @ u3R`
- `R1 @ d1T`

This produced:

1. same-hand consolidation at the upper hub
2. then triple closure at the upper hub

The mirrored lower configuration produced the corresponding lower result.

That was the first sign that the toy had a stable local choreography.

---

# 3. First stable collision laws

The earliest robust result was:

- `LL` first occurs at a class-1 hub
- `LLR` closure follows there
- in the split case, `LR` occurs at the opposite class-1 hub

So the first local law was:

- class-3 nodes are not the first collision sites
- class-2 nodes are approach funnels
- class-1 hubs are the first true interaction and exchange sites

That remains one of the strongest structural observations in the toy.

---

# 4. Face-event vocabulary

The toy then acquired a face/event register.

This began as a crude qualitative logging mechanism, but it quickly became informative.

The signed face-event vocabulary now includes:

- `B+`
- `B-`
- `ABC+_closed`
- `ABC-_closed`
- `ABC+_tension`
- `ABC-_tension`
- `sign_transfer+`
- `sign_transfer-`

Interpretation at the toy level:

- `LL @ signed hub` stamps a local support state `B±`
- `LR @ signed hub` logs sign transfer at that site
- `LLR @ signed hub` either closes cleanly or closes under tension

These names are still toy names, but they now correspond to repeatable behavior.

---

# 5. Local polarity vs transported polarity

A major improvement came when the model separated:

- **hub sign**
- **carry sign**

That was the key EM-inspired distinction.

## Hub sign
A hub has a fixed local polarity:
- `u1T = +`
- `d1T = -`

## Carry sign
A turtle can carry a polarity:
- `+`
- `-`
- or `None`

This created a crucial split in the model:

a turtle can arrive at a hub carrying one sign while the hub itself has the opposite sign.

That is the first place the toy became genuinely interesting.

The split case showed exactly this:

- `L1` acquired `+` at `u1T`
- `L1` then moved to `d1T`
- `d1T` is `-`
- `L1` retained carried `+` on arrival

This produced a difference between:
- what the turtle brought
- where it arrived

That distinction is foundational now.

---

# 6. Site-sign history and mismatch

To make that distinction measurable, the toy gained:

- `site_sign_history`
- `mismatch_count`

This changed the toy from “sign labels” to an actual process trace.

## Site-sign history
Each turtle remembers the signs of the hubs it has encountered.

Example:
- `['+', '-']`

This means the turtle encountered a positive site and later a negative site.

## Mismatch count
Whenever a turtle carrying sign `s` arrives at a hub of opposite sign, the mismatch counter increments.

This gave the split case a very clear signature.

One of the most important states observed was:

- carried sign `+`
- site history `['+', '-']`
- mismatch count `1`

That is the first point at which the toy explicitly represented:
**transported polarity surviving contact with opposite local polarity.**

This was the decisive step in setting the EM compass.

---

# 7. Clean closure vs tensioned closure

At first, every `LLR` event at a signed hub simply closed as:

- `ABC+_closed`
- `ABC-_closed`

That was too coarse.

So the closure rule was upgraded:

- if participating turtles are mismatch-free, closure is clean
- if any participating turtle has mismatch, closure becomes tensioned

This yielded:

- `ABC+_closed`
- `ABC-_closed`
- `ABC+_tension`
- `ABC-_tension`

This was a real conceptual jump.

Now closure quality depends on prior polarity disagreement.

That means the toy can distinguish between:

- a hub that closes in local agreement
- a hub that closes only after a stressed interaction history

This is one of the strongest current laws in the toy.

---

# 8. Discharge

Once tensioned closure existed, the next natural question was:
can a stressed hub relax?

The answer is yes, in the current toy.

A tensioned hub can later undergo a clean closure with matching signs, and this acts like a discharge event.

That means the toy now supports a three-stage process:

1. mismatch accumulation
2. tensioned closure
3. clean discharge closure

This was encoded through:
- `stored_tension`
- closure statistics
- stress-energy bookkeeping

This is still toy logic, but it now has real memory and relaxation behavior.

---

# 9. Hub ledger

To move beyond per-turtle local state, the model acquired a hub ledger.

Each signed hub now tracks:

- `plus_arrivals`
- `minus_arrivals`
- `unsigned_arrivals`
- `mismatch_events`
- `transfers`
- `clean_closures`
- `tension_closures`
- `stored_tension`
- `stress_energy`
- `deposited_stress`

This is the first field-style bookkeeping layer.

It lets the toy say things like:

- this hub is receiving opposite-signed traffic
- this hub is tension-prone
- this hub has discharged
- this hub still remembers cumulative stress cost

This is the first point where the model really stopped being just combinatorial choreography and started behaving like a small dynamical ledger.

---

# 10. Stress-energy

A scalar stress-like quantity was then introduced:

- `stress_energy`

This is not physical energy.
It is a toy scalar intended to measure accumulated stress cost.

In the current model, stress-energy can increase through:

- mismatch events
- tension closures
- deposited turtle-borne stress

It can decrease through:

- clean closure / discharge

But importantly, clean closure does **not** erase all memory.

This distinction matters.

The toy now separates:

- `stored_tension` = current loaded state
- `stress_energy` = accumulated residue / cost

That is a good distinction, and it should probably remain.

---

# 11. Turtle-borne stress

The next major upgrade was:

- `carried_stress`

This allows turtles themselves to carry stress packets.

Current rule:
- tension closure increases `carried_stress` on participating turtles
- clean closure decreases `carried_stress` on participating turtles

This was a crucial addition, because it made stress mobile.

Now stress is not only:
- in the hub
- or in the mismatch count

It can ride the turtles.

That made it possible to ask:
can one stressed hub load another hub?

The answer is yes.

---

# 12. Stress deposition

A further rule allowed turtle-borne stress to be deposited into a hub upon collision:

- turtle arrives carrying stress
- hub ledger increments `deposited_stress`
- hub `stress_energy` rises accordingly

This means hubs now have at least three distinct stress channels:

1. mismatch-generated stress
2. tension-closure stress
3. imported deposited stress

That is a very meaningful upgrade.

It creates a distinction between:
- stress born locally
- stress imported from elsewhere

That difference should probably stay central in future versions.

---

# 13. Stress transport

The `stress_transport` scenario was one of the most important experiments so far.

The behavior observed was:

1. form `+` support at `u1T`
2. move a `+` packet into `d1T`
3. create mismatch at `d1T`
4. force `ABC-_tension`
5. let turtles carry stress back toward `u1T`
6. at `u1T`, the returning stressed turtles trigger `ABC+_tension`

The key observation:

**stress generated at one hub can be transported and re-expressed at another hub.**

That is the strongest “networked field toy” result so far.

It means the model now supports:

- local stress generation
- mobile stress transport
- hub-to-hub stress inheritance

That is big.

---

# 14. Free-flight damping

The next question was whether stress always propagates, or can dissipate in transit.

The answer is yes, it can dissipate.

The current damping rule is:

- if a turtle moves during a tick
- and does not collide during that tick
- then `carried_stress` decreases by 1, floored at 0

This produced a clean distinction between two transport regimes.

## Interaction-dense regime
If turtles move quickly from one stressed interaction into another collision, stress survives and can amplify.

## Free-flight regime
If turtles move without colliding, stress damps away.

This was demonstrated clearly in the `free_flight_damping` scenario.

After tension at `d1T`, the turtles separated:
- no collisions
- carried stress dropped to zero
- no stress reached another hub

This is one of the clearest and nicest toy laws now present.

---

# 15. Current effective laws of the toy

The system currently behaves as though the following toy laws hold.

## Law A: class-1 hubs are primary interaction sites
Same-hand consolidation and closure occur first at hubs, not at outer leaves.

## Law B: local polarity and transported polarity are distinct
A turtle may carry one sign into a hub of opposite sign.

## Law C: mismatch is preserved as history
Opposite-sign encounters do not get erased; they are recorded by mismatch and site history.

## Law D: closure quality depends on history
Closure is either clean or tensioned depending on prior mismatch.

## Law E: tension can be discharged
A stressed hub can later undergo clean closure and reduce its immediate tension.

## Law F: stress is both local and mobile
Stress can live in hub ledgers and on turtles.

## Law G: hubs can inherit imported stress
Returning stressed turtles can load a different hub.

## Law H: free flight damps stress
Stress survives interaction-dense transport but decays in no-collision travel.

These are not physical laws. They are the current operational laws of the toy.

But they are now coherent enough to guide further development.

---

# 16. Best current vocabulary

The vocabulary that seems safest and most useful right now is:

- hub sign
- carry sign
- site sign history
- mismatch
- transfer
- clean closure
- tensioned closure
- stored tension
- stress energy
- carried stress
- deposited stress
- free-flight damping

These terms are specific enough to support experimentation, while still remaining modest.

Avoid overpromoting them prematurely into:
- charge
- field
- current
- magnetic flux
- photon
- gauge boson

Not because those are forbidden forever, but because the toy has not earned them yet.

Right now the model is strongest as a **polarity–tension–transport toy**.

---

# 17. What the toy most resembles conceptually

The current toy most resembles a hybrid of:

- local polarity stamping
- packet transport
- mismatch accumulation
- stress/tension bookkeeping
- lossy propagation away from collisions

The EM compass has been useful precisely because it encouraged the following distinctions:

- source vs transported state
- local polarity vs arriving polarity
- interaction vs free flight
- loading vs discharge
- local residue vs mobile stress

That is the real value of the EM analogy so far.

Not equations.
Not claims.
Distinctions.

---

# 18. What is strongest right now

The strongest current results are:

## (1) Hub-first collision structure
The toy robustly prefers the class-1 hubs as primary interaction/closure sites.

## (2) Polarity survives transport
A sign can move into an opposite-signed hub without immediate erasure.

## (3) Tensioned closure is real
Closure quality changes when mismatch exists.

## (4) Stress can be exported
Turtles can carry stress away from one hub.

## (5) Stress can be imported elsewhere
A different hub can inherit transported stress.

## (6) Free flight dissipates stress
Stress is not immortal; transport regime matters.

Those six together make the toy worth continuing.

---

# 19. What is still weak or provisional

Several things are still provisional.

## (1) Sign assignment
The current `u1T=+`, `d1T=-` assignment is useful, but still a chosen gauge of the toy.

## (2) Event names
`B+`, `ABC-_tension`, etc. are operationally useful, but still local naming choices.

## (3) Stress-energy formula
The current scalar bookkeeping is hand-built and heuristic.

## (4) Damping law
The present damping rule is plausible and useful, but not canonical.

## (5) Transport geometry
The current graph is intentionally tiny. It is a local machinery scaffold, not yet the full carrier.

## (6) Physical interpretation
None of this yet licenses a direct claim of actual electromagnetism.

That said, the toy is no longer vague. It is now specific enough to be critiqued and improved.

---

# 20. Most likely next experiments

Several next experiments now make sense.

## Option A: hub relaxation
Add slow passive decay to hub `stored_tension` or `stress_energy`.

## Option B: stress-threshold effects
Make closure or transfer rules change when hub stress exceeds a threshold.

## Option C: sign-dependent damping
Maybe `+` and `-` packets dissipate differently under different local conditions.

## Option D: larger transport lattice
Embed the same rules into a wider local patch instead of only two hubs.

## Option E: stress-dependent routing
Let turtles with high stress prefer certain paths or become closure-resistant.

## Option F: explicit flux summaries
Aggregate total stress flow and sign flow over many ticks.

If I had to choose the best immediate next step, I would probably choose:
**a slightly larger local patch with the same rules**, so that stress propagation can be observed over more than one spine hop.

---

# 21. Current bottom line

The toy is now much stronger than it was at the beginning.

It started as:
- three turtles
- two hubs
- a vague sense of chirality and collision

It now supports:
- polarity
- transport
- mismatch
- closure quality
- discharge
- hub memory
- mobile stress
- stress deposition
- transport between hubs
- damping in free flight

That is enough to say the toy has crossed a threshold.

It is no longer just a picture-driven hunch.
It is a small but real dynamical rule system.

The EM compass has been productive because it pushed the model toward meaningful distinctions:
- local vs transported
- interaction vs free flight
- tension vs discharge
- residue vs mobile load

That is where the current strength lies.

The safest present summary is:

**The tri-turtle toy now behaves like a polarity-and-stress transport machine with hub-local loading, turtle-borne stress propagation, tensioned closure, discharge, and free-flight damping.**

That is a real result for the toy.

