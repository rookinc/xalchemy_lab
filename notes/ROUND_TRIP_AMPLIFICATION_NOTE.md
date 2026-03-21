# Round-Trip Amplification Note

## Context

We have now tested more than isolated local closures. The turtles have been driven through a full two-hub circulation:

- coherent triad closure at `u1R`
- export through `mR`
- triad closure at `d1R`
- export through `mR`
- return closure at `u1R`

This upgrades the picture from “local collision rules” to an actual **circulating transport process** on the patch.

---

## Main observation

A coherent zero-mismatch positive triad at `u1R` closes cleanly on its first visit, but after transport through the opposite signed hub and return, the stress profile is **larger than it started**.

This means the system is not merely dissipative and not merely neutral.
It exhibits a **round-trip gain law**.

---

## First local law: coherent clean closure at `u1R`

For coherent zero-burden input
\[
(+,+,+), \qquad \text{mismatch} = (0,0,0),
\]
the closure class is
\[
ABC+_{\mathrm{closed}}.
\]

The outgoing stress law is componentwise:
\[
s_i' = \max(s_i - 1, 0).
\]

Equivalently,
\[
\mathbf{s}' = \mathbf{s} - \mathbf{1}_{\mathbf{s}>0},
\]
where the indicator is taken componentwise.

Examples already verified:

- `300 -> 200`
- `303 -> 202`
- `330 -> 220`
- `333 -> 222`
- `421 -> 310`
- `431 -> 320`
- `444 -> 333`

This is the **clean discharge law**.

---

## Second local law: tension closure at the opposite hub

When the exported bundle reaches the opposite signed hub `d1R`, the closure is tensional:
\[
ABC-_{\mathrm{tension}}.
\]

The outgoing stress law is:
\[
\mathbf{r}' = \mathbf{r} + \mathbf{1}.
\]

So each participating channel gains one unit of stress.

For example:

- `200 -> 311`
- `310 -> 421`
- `333 -> 444`
- `522 -> 633`

This is the **uniform triadic excitation law**.

---

## Third step: return to `u1R`

After the `d1R` tension event, the bundle returns to `u1R`.
At that point the returning triad is no longer on the original clean branch.
It closes tensionally at `u1R` as well.

So the full observed sequence is:

\[
\mathbf{s}
\;\xrightarrow{u1R\ \mathrm{closed}}\;
\mathbf{s} - \mathbf{1}_{\mathbf{s}>0}
\;\xrightarrow{d1R\ \mathrm{tension}}\;
\mathbf{s} - \mathbf{1}_{\mathbf{s}>0} + \mathbf{1}
\;\xrightarrow{u1R\ \mathrm{return\ tension}}\;
\mathbf{s} - \mathbf{1}_{\mathbf{s}>0} + 2\mathbf{1}.
\]

This gives the empirical round-trip operator:

\[
\boxed{
\Phi_{\mathrm{round\text{-}trip}}(\mathbf{s})
=
\mathbf{s} + 2\mathbf{1} - \mathbf{1}_{\mathbf{s}>0}
}
\]

---

## Verified examples

The round-trip probe gave:

- `000 -> 222`
- `100 -> 222`
- `111 -> 222`
- `300 -> 422`
- `421 -> 532`
- `444 -> 555`
- `633 -> 744`

Interpretation:

- if a channel was initially occupied, it gains `+1` over a full round trip
- if a channel was initially empty, it gains `+2` over a full round trip

So the loop is **amplifying**, not fixed and not conservative.

---

## Structural meaning

This is the first real indication that the tri-patch behaves like a **pump** rather than a passive relay.

The local ingredients are:

1. **clean discharge** on coherent zero-burden closure
2. **uniform excitation** on tension closure
3. **sign-flip transport** across opposite hubs
4. **return tension** after circulation

Together these generate a stress-gain mechanism over one loop.

So the turtles are no longer merely “walking the terrain.”
They have found a **circulating gain mechanism on the terrain**.

---

## Conjecture

### Round-Trip Amplification Conjecture

For coherent zero-mismatch positive input \(\mathbf{s}\) at `u1R`, one full two-hub circulation acts by
\[
\Phi_{\mathrm{round\text{-}trip}}(\mathbf{s})
=
\mathbf{s} + 2\mathbf{1} - \mathbf{1}_{\mathbf{s}>0}.
\]

That is:

- occupied channels gain `+1`
- empty channels gain `+2`

after one full loop.

---

## Important consequence

This means stress is **not** a branch selector in the present model, but it is very much a **dynamical payload**.

More precisely:

- branch choice appears to be burden-driven
- stress does not promote a coherent zero-mismatch triad into tension on first contact
- however, stress participates in a transport loop that generates downstream and return amplification

So stress is not structural at entry, but it becomes structural through circulation.

---

## Where we are now

We now have evidence for three empirical laws:

1. **Closed branch law**
   \[
   \Phi_{\mathrm{closed}}(\mathbf{s}) = \mathbf{s} - \mathbf{1}_{\mathbf{s}>0}
   \]

2. **Tension branch law**
   \[
   \Phi_{\mathrm{tension}}(\mathbf{s}) = \mathbf{s} + \mathbf{1}
   \]

3. **Round-trip law**
   \[
   \Phi_{\mathrm{round\text{-}trip}}(\mathbf{s}) = \mathbf{s} + 2\mathbf{1} - \mathbf{1}_{\mathbf{s}>0}
   \]

This is the first genuinely dynamical transport law discovered on the patch.

---

## Next conjecture

The next natural question is whether repeated round trips produce:

- linear growth
- affine growth by channel occupancy class
- eventual branch lock-in
- saturation
- or a new periodic regime

So the next experiment should be:

### Multi-cycle amplification sweep

Take a seed profile such as

- `000`
- `111`
- `300`
- `421`
- `444`

and iterate multiple full loops, recording after each cycle:

- sign vector
- stress vector
- mismatch vector
- closure class at each hub
- ledger totals at `u1R` and `d1R`

That will tell us whether the turtles have found:

- a pump,
- an attractor,
- or an instability.

---

## Working summary

The turtles have learned the terrain well enough to do more than traverse it.
They now appear to enact a **local discharge / opposite-hub recharge / return overcharge cycle**.

That is the first serious hint that the tri-patch is not just a kinematic toy but a **circulatory dynamical machine**.

