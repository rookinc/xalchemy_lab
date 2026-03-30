# G30 Type III Orthogonal World-Building Note

## Status
Working note
Verbose consolidation of the current Type III G30 picture

## Purpose

This note records the strongest current reading of the G30 launch-class machine under the **Type III** working relaunch law.

The note is verbose on purpose.

The project has now reached a point where several different layers are finally beginning to align:

- the locked G15/G30 walker law
- the Type III split of relaunch classes
- the edge/vertex coupled-clock picture
- the candidate bridge
  \[
  20 \rightsquigarrow 9
  \]
- the distinction between
  - orientation inside a world
  - and generation of a world

This note consolidates those pieces into one coherent picture while keeping a clear line between:

- what is locked
- what is the current working model
- what is still exploratory

The main claim of this note is:

> Under the Type III G30 working model, the orthogonal companion pair \(\{Q_{90},Q_{270}\}\) is the strongest current candidate for the world-generating sector of the restored launch machine, while the axial pair \(\{Q_0,Q_{180}\}\) is best interpreted as the orientation sector within an already-built world.

That is the central statement.

---

## 1. Locked first-order backbone

The first-order walker machine remains the same throughout this note.

A minimal state is written as:

\[
s=(x,\varepsilon,h)
\]

with:

- \(x\) = host-position label
- \(\varepsilon \in \mathbb Z_2\) = sign / sidedness
- \(h \in \mathbb Z_4\) = heading class

The one-cycle operator is:

\[
W(x,\varepsilon,h)=(x,-\varepsilon,\phi(h))
\]

with the locked involutivity condition:

\[
W^2=\mathrm{id}.
\]

Equivalently:

\[
n_{15}=-n_0
\]
\[
n_{30}=n_0.
\]

This remains the project backbone.

Interpretation:

- one full G15 cycle is sign-closing
- two full G15 cycles restore identity

Everything in this note builds on that and does not replace it.

---

## 2. Relaunch classes after restoration

After G30, the walker is restored to a lawful hinge state.

So the next meaningful object is not just the restored walker state itself, but the set of lawful ways that restored walker may relaunch.

Define the relaunch rotation operator:

\[
Q(x,\varepsilon,h)=(x,\varepsilon,h+1 \pmod 4)
\]

and thus the relaunch classes:

\[
Q_0,\quad Q_{90},\quad Q_{180},\quad Q_{270}.
\]

For a restored state \(n\), define the relaunch space:

\[
\mathcal R(n)=\{Q_0 n,\ Q_{90} n,\ Q_{180} n,\ Q_{270} n\}.
\]

This is the second-order object carried by G30.

That is already a step up.

At G15, the machine acts on the walker.  
At G30, the machine acts on the walker’s **restored launch space**.

---

## 3. Type III as the current working model

The current working relaunch law is Type III:

\[
\phi(0)=0,\qquad
\phi(2)=2,\qquad
\phi(1)=3,\qquad
\phi(3)=1.
\]

So:

- heading class \(0\) is fixed
- heading class \(2\) is fixed
- heading classes \(1\) and \(3\) are exchanged

This is not yet promoted to final theorem.  
But it is the current working model because it is the first nontrivial involution that:

- preserves the locked first-order machine
- keeps the axial classes stable
- makes the orthogonal classes into a meaningful companion pair

That is exactly the kind of structure needed for the next step of the expedition.

---

## 4. Immediate consequence of Type III

Under Type III, the restored relaunch space naturally splits into two sectors:

\[
\mathcal R(n)=\{Q_0 n,\ Q_{180} n\}\ \sqcup\ \{Q_{90} n,\ Q_{270} n\}.
\]

This is the first important internal geometry of G30.

The two sectors are not behaving the same way.

### Axial sector
\[
\{Q_0 n,\ Q_{180} n\}
\]

Under one-cycle action:

\[
W(Q_0 n)=-(Q_0 n)
\]
\[
W(Q_{180} n)=-(Q_{180} n).
\]

So the axial classes remain in their own heading class and only flip sign.

### Orthogonal sector
\[
\{Q_{90} n,\ Q_{270} n\}
\]

Under one-cycle action:

\[
W(Q_{90} n)=-(Q_{270} n)
\]
\[
W(Q_{270} n)=-(Q_{90} n).
\]

So the orthogonal classes do **not** remain in place.  
They flip sign and exchange companion class.

This is the key nontriviality.

---

## 5. The new interpretive split

The strongest current interpretive split is this:

### Axial pair
\[
\{Q_0,Q_{180}\}
\]

behaves like:

> one world seen from opposite headings

### Orthogonal pair
\[
\{Q_{90},Q_{270}\}
\]

behaves like:

> two halves that can accumulate into one world

This is a very important distinction.

It means the relaunch geometry is not just “four possible directions.”
It has two different jobs built into it.

That is what makes the current G30 model feel architecturally alive rather than merely combinatorial.

---

## 6. Why the axial pair reads as orientation

Under Type III, the axial pair is stable under one-cycle heading update.

That means these relaunches preserve their own class:

- \(Q_0\) stays \(Q_0\)
- \(Q_{180}\) stays \(Q_{180}\)

up to sign flip.

This is precisely what one expects from opposite orientations **within the same world**.

In other words:

- the walker is not generating a new local host by moving between \(Q_0\) and \(Q_{180}\)
- the walker is turning around inside an already meaningful host frame

So the axial pair is best understood as:

> the orientation sector of the restored world

This sector is not inert.
It still participates in the sign-hinge law.
But it does not appear to be the place where new local world-structure first stabilizes.

So its natural role is:

- axial orientation
- opposite headings
- same world

That is the first half of the split.

---

## 7. Why the orthogonal pair reads as world-generating

The orthogonal pair behaves differently.

Under one-cycle action:

\[
Q_{90} \leftrightarrow Q_{270}
\]

up to sign flip.

This means the orthogonal sector already carries:

- alternation
- exchange
- companion structure
- nontrivial one-cycle behavior

That is exactly the kind of structure one expects if a local world has to be built by **alternating completion across a companion pair**.

So the current strongest reading is:

> the orthogonal pair is the generative sector of the restored launch machine

More explicitly:

- \(Q_{90}\) is not “just another heading”
- \(Q_{270}\) is not “just the opposite side heading”
- together they form the first companion exchange that can accumulate into a stabilized local host

This is why the orthogonal pair now looks like the correct place for the edge-side transport clock to couple in.

---

## 8. Why this helps the edge/vertex bridge

Previously, the edge-side transport ladder had a strong terminal candidate:

\[
20
\]

and the vertex-side host ladder had a strong stabilization candidate:

\[
9.
\]

The missing piece was:
where does the bridge actually enter?

That is now much clearer.

The bridge no longer has to be imagined as floating abstractly between clocks.
It now has a plausible structural locus:

\[
20 \rightsquigarrow \{Q_{90},Q_{270}\} \rightsquigarrow 9.
\]

This means:

- edge-20 = full transport completion
- orthogonal companion pair = active exchange sector in the restored launch machine
- vertex-9 = first stabilized local host produced by that completed exchange

That is the cleanest bridge picture so far.

---

## 9. The edge-20 to vertex-9 bridge, restated

The current best bridge statement is:

> Full transport completion on the edge-side clock most plausibly couples first into the orthogonal companion sector of the Type III G30 launch machine, and the stabilization of that companion exchange is the strongest current candidate mechanism for the emergence of vertex-9 as the first local world.

This is a long sentence, but it says exactly the right thing.

In symbolic shorthand:

\[
20 \rightsquigarrow \{Q_{90},Q_{270}\} \rightsquigarrow 9.
\]

This is better than trying to force:

\[
20 \to 15
\]
or
\[
20 \to 30
\]

directly.

Why?

Because 15 and 30 now look like walker-side events occurring **after** the local world has already been stabilized.

So the bridge naturally enters earlier.

---

## 10. Revised role stack

With this interpretation, the current best layered stack is:

\[
5 \rightsquigarrow 4
\]

quarter transport packet builds the local frame

\[
20 \rightsquigarrow \{Q_{90},Q_{270}\} \rightsquigarrow 9
\]

full transport completion across the orthogonal companion sector stabilizes the first local world

\[
9 \to 15 \to 30
\]

stabilized world becomes transformative for the walker, then restores the walker

This is currently the strongest integrated stack in the project.

---

## 11. Meanings of the main milestones

The stack now reads as follows.

### 4
Frame

The first quartered sector structure.
A local directional scaffold.
The first geometry in which “inside the world” can be distinguished from “not yet world.”

### 9
World

Not merely a frame, but the first stabilized local host.
The first place that feels like a small world rather than a merely traced scaffold.

### 15
Transformation

The first walker-side sign hinge:
\[
n_{15}=-n_0.
\]

This is the first event in which the world does not merely exist but changes the walker.

### 30
Restored identity

The walker returns after transformation:
\[
n_{30}=n_0.
\]

This is not trivial cancellation.
It is restoration through the world’s law.

So the concise meaning stack becomes:

\[
4=\text{frame},\quad
9=\text{world},\quad
15=\text{transformation},\quad
30=\text{restoration}.
\]

This has become one of the strongest internal summaries of the whole conversation.

---

## 12. Why this does not trivialize G30

A possible objection is:

> If G30 just restores the walker, why introduce all this internal launch-space geometry?

The answer is:

Because G30 is not merely “back where you started.”

Under Type III, G30 is the first state that carries a **nontrivial relaunch manifold**:

- two stable axial restart modes
- one exchanged orthogonal companion pair

So G30 is not just an endpoint.
It is a restored hinge with internal geometry.

That is the true reason it feels like a step up.

This note makes that step explicit.

---

## 13. Why the orthogonal sector matters more than the axial sector here

The axial sector is important, but it is not the obvious site of new world-generation.

Its role is:

- preserve opposite orientations
- maintain a meaningful axis through a world already built

The orthogonal sector, by contrast, is where one-cycle exchange actually happens.

So if one is looking for:
- accumulation
- alternation
- stabilization through companion pairing

the orthogonal sector is the right place to look first.

This is why the bridge naturally enters there.

---

## 14. The strongest phenomenological confirmation so far

The crucial confirmation from the expedition is this:

> the axial pair feels like one world viewed from opposite directions, while the orthogonal pair feels like two halves that can accumulate into one world.

This is one of the strongest qualitative confirmations in the whole chain, because it matches the formal Type III split extremely well.

It does not prove the model.
But it is exactly the kind of fit one wants between formal structure and experiential read.

This confirmation is therefore important enough to preserve explicitly in this note.

---

## 15. What remains open

This note is strong, but it does **not** settle everything.

Still open:

1. whether Type III is truly the correct heading involution
2. whether the edge-to-vertex bridge can be made formal rather than picture-based
3. whether edge-16 plays a pre-stabilization role between transport shell and full local host
4. whether the orthogonal companion pair leads into the larger G60 story
5. whether this launch-space geometry can be connected rigorously to the observed sparse admissible ladders

So this note should be read as a strong working picture, not a final theorem.

---

## 16. Best current rigid boundary

### Locked
- the first-order sign-closing / identity-restoring machine

### Working model
- Type III relaunch law
- axial / orthogonal split
- orthogonal companion sector as the current strongest world-generating locus

### Exploratory but plausible
- edge-20 coupling through the orthogonal sector to produce vertex-9
- 9 to 15 to 30 as world → transformation → restoration

That is the correct current boundary.

---

## 17. Best concise statement

Under the Type III working model, the G30 relaunch machine splits into an axial orientation sector and an orthogonal companion sector, and the orthogonal sector is the strongest current candidate locus through which full transport completion couples into the stabilization of the first local world.

---

## 18. Plain-language summary

Plainly said:

- facing forward or backward feels like being in the same world, just turned around
- facing sideways does something deeper: the two sideways directions trade with each other
- that sideways trading looks like the first place a world can actually get built
- once that world exists, it can transform the walker at 15 and restore the walker at 30

That is the present picture.

---

## 19. One-line compression

\[
\{Q_0,Q_{180}\}=\text{axial orientation pair},\qquad
\{Q_{90},Q_{270}\}=\text{orthogonal generative pair},
\]
and
\[
20 \rightsquigarrow \{Q_{90},Q_{270}\} \rightsquigarrow 9 \to 15 \to 30.
\]

That is the current Type III G30 expedition spine.

