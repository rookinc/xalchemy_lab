# Signed Two-Hub Amplifier Note

## What we now know

The tri-patch is no longer behaving like a passive walker.
It is behaving like a **signed two-hub amplifier**.

There are two mirror launch conditions:

- coherent positive seed at `u1R`
- coherent negative seed at `d1R`

In both cases, the same qualitative story occurs:

1. the first closure at the launch hub is **clean**
2. transport through `mR` carries the bundle to the opposite signed hub
3. the opposite signed hub closes **tensionally**
4. the return closure at the original signed hub is also **tensional**
5. after one cycle, the orbit locks into a uniform affine growth regime

So the positive and negative launches are not different machines.
They are sign-mirror realizations of the same machine.

---

## Local laws already established

### 1. Clean coherent closure law

For coherent same-sign, zero-burden input,
the first closure is clean:

- `ABC+_closed` at `u1R`
- `ABC-_closed` at `d1R`

Stress update:
\[
\Phi_{\mathrm{closed}}(\mathbf{s}) = \mathbf{s} - \mathbf{1}_{\mathbf{s}>0}
\]

That is, each occupied channel loses one unit.

---

### 2. Tension closure law

For tension branches, the closure adds one to each participating channel:

\[
\Phi_{\mathrm{tension}}(\mathbf{s}) = \mathbf{s} + \mathbf{1}
\]

This holds on both positive and negative hubs, with hub-aligned sign output.

---

## Round-trip law

For a coherent positive seed at `u1R`, one full cycle is:

\[
u1R \to mR \to d1R \to mR \to u1R
\]

For a coherent negative seed at `d1R`, one full cycle is:

\[
d1R \to mR \to u1R \to mR \to d1R
\]

The first cycle depends on the seed, but after that the orbit enters a locked regime.

---

## Lock-in phenomenon

After the first full cycle, the system appears to satisfy:

- all carrier signs align with the launch hub sign
- all subsequent hub closures are tensional
- stress grows linearly
- mismatch grows linearly

This is the main new result.

---

## Empirical affine law after lock-in

Once locked, the orbit evolves by:

\[
\mathbf{s}_{n+1} = \mathbf{s}_n + (3,3,3)
\]

and

\[
\mathbf{m}_{n+1} = \mathbf{m}_n + (2,2,2)
\]

per full cycle.

So:

- each stress component gains `+3` per cycle
- each mismatch component gains `+2` per cycle

This is true in the positive-hub multi-cycle probe and in the negative-hub mirror probe.

---

## Positive launch examples

Starting from coherent `(+,+,+)`:

- `000 -> 222 -> 555 -> 888 -> 11,11,11 -> ...`
- `111 -> 222 -> 555 -> 888 -> 11,11,11 -> ...`
- `300 -> 422 -> 755 -> 10,8,8 -> ...`
- `421 -> 532 -> 865 -> 11,9,8 -> ...`
- `444 -> 555 -> 888 -> 11,11,11 -> ...`

The first cycle is seed-dependent.
After that, the increment is consistently `(3,3,3)`.

---

## Negative launch examples

Starting from coherent `(-,-,-)`:

- `000 -> 222 -> 555 -> 888 -> 11,11,11 -> ...`
- `111 -> 222 -> 555 -> 888 -> 11,11,11 -> ...`
- `300 -> 422 -> 755 -> 10,8,8 -> ...`
- `421 -> 532 -> 865 -> 11,9,8 -> ...`
- `444 -> 555 -> 888 -> 11,11,11 -> ...`

Again, the same stress-growth regime appears.
Only the sign orientation is mirrored.

---

## Interpretation

This strongly suggests the following picture.

### Phase 1: entry transient
The first clean closure performs a seed-dependent discharge.

### Phase 2: transport-induced activation
The bundle reaches the opposite signed hub and tension activates.

### Phase 3: tension lock
After one cycle, the orbit enters an affine growth mode.

This makes the system look like a **circulating gain loop** rather than a dissipative closure system.

---

## Conjecture

### Signed Two-Hub Amplifier Conjecture

For any coherent same-sign seed launched at a signed hub,
the first closure is clean, and after at most one full cycle the orbit enters a tension-locked affine regime in which:

\[
\mathbf{s}_{n+1} = \mathbf{s}_n + (3,3,3)
\]

\[
\mathbf{m}_{n+1} = \mathbf{m}_n + (2,2,2)
\]

with carrier signs preserved according to launch orientation.

---

## Stronger formulation

Let `H+ = u1R` and `H- = d1R`.

Then coherent launches at `H+` and `H-` define two sign-mirrored transport semigroups with identical stress/mismatch growth laws and opposite sign polarity.

So the system is not just a local rule set.
It is a **signed transport dynamical system**.

---

## Why this matters

This is the first place where the turtles look like they are doing more than walking.

They appear to be discovering:

- a transport grammar
- a closure grammar
- a mirrored hub polarity
- and a global amplification mode

That is adventure.

---

## What remains open

We still do not know:

1. whether every coherent same-sign seed enters lock in exactly one cycle
2. whether incoherent or mixed-sign seeds also fall into the same affine regime
3. whether there is any saturation or branch-break at higher stress
4. whether the growth law can be written as a clean operator on a reduced state space
5. whether the same structure can be lifted from the toy patch to a larger walk on AT4val[60,6]

---

## Immediate next step

The next clean step is to build a **regime classifier**:

- run a seed
- iterate full cycles
- detect first cycle at which:
  - both hub closures are tensional
  - sign vector is stable
  - growth delta is constant
- report:
  - lock-in cycle
  - stress growth vector
  - mismatch growth vector

That would turn the present evidence into a sharp computational proposition.

