# G900 Generator and Lens Note
## A working note on admissibility, legibility, and the division between generator and lens

Date: 2026-03-29

---

## 0. Why this note exists

This note exists to record an important clarification in the G900 project language.

Earlier schema work made it increasingly clear that the strict JSON/binning layer should not be thought of as the object itself, nor as the law itself, but as the kernel of a lens through which lawful structure becomes visible.

That much remains true.

But there is now a sharper distinction available, and it improves the whole stack:

> The simulator is the generator that walks only admissible action and emits lawful states.
> The strict schema is the kernel of the lens through which that lawful output becomes legible.

This matters because it separates two jobs that should not be conflated:

- **generation of lawful states**
- **legibility of lawful states**

The generator does the first.
The lens does the second.

This note records that division cleanly so it can anchor future vocabulary.

---

## 1. The central distinction

The strongest compact formulation currently available is:

> Admissibility belongs to the generator.
> Legibility belongs to the lens.

This is a very strong sentence because it prevents several kinds of confusion at once.

It prevents the mistake of treating the schema as if it were responsible for deciding whether the output is valid.
It prevents the mistake of treating the generator as if its only job were to emit raw uninterpreted clutter.
It prevents the mistake of treating residue as error by default.
And it prevents the mistake of collapsing the production of lawful states into the interpretation of those states.

The point is simple:

- the generator already guarantees lawful production
- the lens organizes lawful appearance

So the lens is not a validator in the deepest sense.
It is a reader.

---

## 2. Generator

### Working definition

The **generator** is the simulator that walks only admissible action and emits lawful states.

This should now be considered the preferred term for the simulator in the G900 stack.

“Simulator” is still fine in practical contexts, but “generator” says more precisely what matters here.

The object is not being sampled from arbitrary possibility.
It is not being corrupted and then filtered.
It is not throwing noise that later needs to be purified.

It is walking a lawful family of actions.

So the output stream is not a mixture of valid and invalid states.
It is a stream of admissible states by construction.

### Consequence

This means the generator is already the **admissibility engine**.

That is a major conceptual gain.

It means that the project can stop asking, at the schema level, “is this output clean?”
The answer is already yes, by construction, so long as the generator is doing what it is supposed to do.

The real questions now become higher-order questions:

- what kinds of lawful forms appear?
- which regularities recur?
- what is stable across scale?
- what becomes compressible?
- what survives quotienting?
- what remains as lawful residue?

Those are much stronger questions than mere validity checking.

### Strong phrasing

> The generator writes lawful history.

That feels right and likely worth keeping.

---

## 3. Lens

### Working definition

The **lens** is the structured observational frame through which lawful output becomes legible.

This continues the earlier lens language, but now with sharper placement in the stack.

The lens does not decide which states are admissible.
The generator already did that.

The lens does not purify the output.
The output is already lawful.

The lens does not impose truth from outside.
It organizes visibility from within a disciplined observational frame.

So the lens is responsible for:

- selecting channels of visibility
- grouping measurements into bins
- preserving useful distinctions
- stabilizing comparison
- rendering lawful appearance in structured form

Examples of lens outputs include:

- shell profiles
- shell-transition images
- growth-generation summaries
- transport-role distributions
- pair-distance tables
- quotient-fiber summaries
- spectral-band maps
- residue maps

These are not the carrier itself.
They are not necessarily the law itself.
They are images produced through the lens.

### Strong phrasing

> The lens extracts intelligibility from lawful output.

That is probably a keeper sentence.

---

## 4. Why this is better than validation language

Without this distinction, there is a temptation to burden the schema with a job it does not really have.

One might say:
- the schema validates the object
- the bins decide whether the state is good
- the readout cleans the simulation
- the observational layer acts like a gatekeeper

That now appears wrong, or at least too weak.

If the generator walks only admissible action, then the observational layer is not a gatekeeper over validity.
Its job is not to separate good states from bad states.
Its job is to preserve distinctions among already lawful states.

That is a more interesting and more demanding role.

The lens must not confuse:
- one lawful regime with another
- one closure mode with another
- one transport class with another
- one quotient behavior with another
- one residual pattern with another

So strictness in the schema is not metaphysical validation.
It is observational hygiene.

### Strong phrasing

> The schema is strict not because the generator is impure, but because the readout must not smear distinct lawful phenomena together.

That sentence captures the whole spirit nicely.

---

## 5. Carrier, generator, lens, image

With this clarification, the stack becomes cleaner.

### Carrier
The underlying grown object or lawful state-stream under study.

### Generator
The simulator that walks only admissible action and emits lawful states.

### Lens
The structured observational frame through which lawful output becomes legible.

### Image
The structured appearance of lawful output under a chosen lens.

This is already a very strong four-part stack.

And it avoids the confusion of treating the lens as if it were the source of admissibility.

The source of admissibility is the generator.
The source of legibility is the lens.

---

## 6. Law and residue under the new picture

The new distinction also sharpens the meaning of **law** and **residue**.

### Law

A **law** is a stable relation visible in the lawful images produced under one or more lenses.

This is stronger now because the input family is already lawful.
So when a pattern persists, it is not surviving random contamination.
It is emerging from within admissible action itself.

That makes discovered relations much more meaningful.

One is not extracting signal from noise.
One is extracting compression from lawful history.

### Residue

**Residue** is lawful remainder not yet compressed by the current lens or proposed law.

This point is crucial.

If the generator only emits lawful states, then residue is no longer to be interpreted as:
- invalidity
- mistake
- glitch
- contamination
- broken output

Instead residue becomes:
- uncompressed lawful structure
- unresolved higher-order organization
- regime boundary
- lens weakness
- law incompleteness
- a sign that additional structure remains to be named

This is a major conceptual upgrade.

It lets residue become informative without shame.

### Strong phrasing

> Residue is not failed admissibility. It is lawful remainder.

That sentence is probably worth preserving exactly.

---

## 7. Admissible action revisited

This clarification also changes how admissible action should be discussed.

Previously one might have said:

> An admissible action is an action whose before-and-after image remains within the lawful family defined by the active lens.

That is still a usable observational definition, but it is now secondary.

The stronger structural definition is:

> An admissible action is an action walked by the generator.

In other words, admissibility is generator-native.
The lens may help characterize or compare the consequences of admissible action, but it does not originate admissibility.

This is cleaner.

The generator defines the lawful action family.
The lens reveals the morphology of that family.

So a good division is:

- **generator-native admissibility**
- **lens-mediated legibility**

That may become important later when multiple lenses exist over the same generator.

---

## 8. Discovery

Once admissibility belongs to the generator and legibility belongs to the lens, a new layer becomes clearer.

That layer is **discovery**.

A useful working definition is:

> Discovery is the extraction of stable relations from lawful images across one or more lenses.

This is helpful because it places discovery downstream of both lawful generation and disciplined observation.

The generator alone does not discover.
It emits lawful states.

The lens alone does not discover.
It renders them legible.

Discovery occurs when stable relations are extracted from the images the lens provides.

This makes the overall stack:

carrier -> generator -> lens -> image -> law -> discovery

And that is a strong programmatic ladder.

---

## 9. The readout system

This suggests a very clean way to understand the current schema work.

It is not the kernel of the object.
It is not the kernel of admissibility.
It is not the kernel of the theorem.

It is the kernel of the **readout system**.

But with the new language, even that can be sharpened.

The readout system is not passive.
It is the lens machinery through which lawful output becomes comparable, compressible, and eventually theorem-bearing.

So perhaps the best phrasing is:

> The strict schema is the kernel of the readout lens for lawful output.

Or even more simply:

> The strict schema is the kernel of the lens through which admissible action becomes legible.

That may be the sentence most worth carrying forward.

---

## 10. Multiple lenses over one generator

This clarification also makes plurality easier to think about.

A single generator may support multiple lenses.

For example:

### Shell lens
Reveals radial occupancy and shell-transition structure.

### Growth lens
Reveals birth ticks, epochs, and developmental phases.

### Transport lens
Reveals role classes, attachments, coupling, and closure modes.

### Quotient lens
Reveals effective descent, fiber structure, and coarse-grained law.

### Spectral lens
Reveals mode structure, low-band coherence, and compression candidates.

### Cocycle lens
Reveals parity memory, twist, sheet structure, and holonomy behavior.

All of these can read the lawful stream emitted by the same generator.

This is excellent because it means admissibility can remain fixed while legibility varies.

That separation is very powerful.

It means:
- one lawful history
- many lawful readings

And this lets the project ask which features are:
- lens-specific
- lens-invariant
- lens-emergent
- or only visible in compound lens stacks

---

## 11. The role of strict schema under this picture

Under this clarified stack, the strict schema has a very precise role.

It exists to:

- stabilize the channels of legibility
- preserve distinctions among lawful outputs
- support reproducible comparison
- prevent observational drift
- keep images from becoming ambiguous
- protect downstream law extraction from smeared categories

In other words, schema strictness is not there because the object is doubtful.
It is there because the observation must be disciplined.

This is probably the cleanest statement of all:

> The generator guarantees admissibility. The schema protects legibility.

That sentence feels very strong.

---

## 12. What this means for theorem-hunting

If everything emitted by the sim is already lawful, then theorem-hunting becomes more interesting.

The project is no longer primarily about screening valid from invalid.
It becomes about studying the morphology of lawful emergence.

That means the important questions become:

- which patterns recur across lawful growth?
- which images compress well?
- which quantities become stable under quotient?
- which relations survive rerooting or lens change?
- which residues persist across all lawful runs?
- which laws are local shadows of deeper global structure?

This is a real research program.

Not validation.
Not cleanup.
Not post-hoc patching.

It is the study of the structure of lawful output.

That is a much stronger posture.

---

## 13. Compact vocabulary block

Here is the updated compact block.

### Carrier
The underlying object or lawful state-stream under study.

### Generator
The simulator that walks only admissible action and emits lawful states.

### Lens
The structured observational frame through which lawful output becomes legible.

### Image
The structured appearance of lawful output under a chosen lens.

### Law
A stable relation visible in one or more lawful images.

### Residue
Lawful remainder not yet compressed by the current lens or proposed law.

### Discovery
The extraction of stable relations from lawful images across one or more lenses.

This block should likely be preserved.

---

## 14. Immediate application to G900

Using this language, the current project state may be described as follows.

### Carrier
G900 understood as a lawful growth object or lawful state-stream.

### Generator
The simulator that walks admissible action and emits only lawful states.

### Lens kernel
The strict JSON/binning schema now under construction.

### Image
The shell, role, transition, quotient, residue, and spectral summaries generated through that lens.

### Candidate law
Any stable relation that compresses those lawful images.

### Residue
Any lawful remainder not yet compressed by the candidate law or current lens.

### Discovery task
Determine which relations are stable across runs, roots, quotients, and lenses.

That is already a coherent program.

---

## 15. Closing orientation

The best short statement currently available may be this:

> The simulator guarantees admissibility.
> The lens extracts intelligibility.

And the best fuller statement may be:

> The strict G900 schema is not the carrier and not the source of admissibility. It is the kernel of the lens through which the lawful output of admissible action becomes legible.

That feels right because it preserves all the necessary divisions:

- the generator is responsible for lawful production
- the lens is responsible for lawful visibility
- the image is the structured appearance of lawful output
- the law is what compresses that appearance
- the residue is what remains lawfully uncompressed
- discovery belongs to the comparison of images across lenses

This is enough for now.

The generator writes lawful history.
The lens reads its grammar.

