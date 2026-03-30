# G15 State and Operator Note

## Status
Working note

## Purpose

This note defines the minimum formal machinery needed to test the G15 host-frame thesis at the level of **pathing**.

The immediate goal is not to prove the whole architecture.

The goal is to make the anchor walk executable in principle.

---

## 1. Core idea

A bare vertex is not enough.

If we want the actions

- `lift`
- `left`
- `right`
- `move`

to be meaningful and repeatable, then a traversal element must include more than location.

So we define a **state** rather than a bare position.

---

## 2. State model

A traversal state is

\[
s = (v,\sigma,h)
\]

where:

- \(v\) is the ambient host location
- \(\sigma\) is the layer, sheet, sign, or register
- \(h\) is the heading

Interpretation:

- \(v\) says **where**
- \(\sigma\) says **on which register**
- \(h\) says **which way you are facing**

This is the minimum structure needed for pathing.

---

## 3. Ambient host locations

Let the host frame \(G15\) have ambient location set

\[
V = \{v_0,v_1,\dots,v_{14}\}.
\]

These are host locations, not yet the full traversal states.

A traversal state lives over one host location at a time.

---

## 4. Registers

Let \(\sigma\) range over a finite register set.

For testing, we begin with the smallest useful version:

\[
\Sigma = \{0,1,2\}.
\]

Interpretation:

- \(\sigma = 0\): base register
- \(\sigma = 1\): middle register
- \(\sigma = 2\): upper register

This matches the current intuition that the anchor walk begins with two lifts before beginning its lateral routing.

This choice is provisional.  
It can later be replaced by:

- signed sheets
- chamber classes
- polarity states
- a richer layered index

But \(\{0,1,2\}\) is enough to begin.

---

## 5. Headings

Let \(h\) range over a finite heading set.

For testing, use

\[
H = \{0,1,2,3\}.
\]

Interpretation:

- \(h=0\): forward / north / up in the chosen local chart
- \(h=1\): right / east
- \(h=2\): back / south
- \(h=3\): left / west

These labels are not absolute geometric directions.  
They are local orientation labels.

The only thing that matters initially is that headings can be turned consistently.

---

## 6. Primitive operators

We define four primitive operators on states.

### 6.1 Left
\[
L(v,\sigma,h) = (v,\sigma,h-1 \bmod 4)
\]

This changes heading but does not change host location or register.

### 6.2 Right
\[
R(v,\sigma,h) = (v,\sigma,h+1 \bmod 4)
\]

This changes heading but does not change host location or register.

### 6.3 Lift
\[
U(v,\sigma,h) = (v,\sigma+1,h)
\]

provided \(\sigma+1\) is admissible.

For the initial test model:

- \(U(v,0,h)=(v,1,h)\)
- \(U(v,1,h)=(v,2,h)\)
- \(U(v,2,h)\) is undefined unless a wrap or ceiling rule is later added

So the current anchor walk naturally starts at \(\sigma=0\) and lifts twice.

### 6.4 Move
\[
M(v,\sigma,h) = (\mu_\sigma(v,h),\sigma,h)
\]

where \(\mu_\sigma\) is the host transition rule for register \(\sigma\).

This is the most important operator.

`move` does not just “go somewhere.”  
It advances along a heading-dependent host adjacency rule.

So the real burden of the model is to specify the maps

\[
\mu_0,\mu_1,\mu_2 : V \times H \to V.
\]

---

## 7. Determinism requirement

The host thesis requires determinism.

That means:

For every admissible state \(s\),

- \(L(s)\) is unique
- \(R(s)\) is unique
- \(U(s)\) is unique when defined
- \(M(s)\) is unique when defined

If any operator depends on drawing intuition or a hidden choice, the host/pathing thesis weakens.

So the first implementation target is:

> a fully explicit transition dictionary for `move`

---

## 8. Projection maps

We need to distinguish full pathing state from ambient landing location.

### 8.1 Ambient landing projection
\[
\pi(v,\sigma,h)=v
\]

This forgets register and heading.

### 8.2 Register projection
\[
\rho(v,\sigma,h)=\sigma
\]

### 8.3 Heading projection
\[
\eta(v,\sigma,h)=h
\]

These let us inspect a path at three levels:

- ambient landing trace
- register trace
- heading trace

---

## 9. Anchor walk in operator form

Let the chosen start state be

\[
n_0=(v_a,0,h_a).
\]

Then define

\[
n_1=U(n_0)
\]
\[
n_2=U(n_1)
\]
\[
n_3=M(R(M(L(n_2))))
\]
\[
n_4=M(M(R(n_3)))
\]
\[
n_5=M(M(R(n_4)))
\]
\[
n_6=M(M(R(n_5)))
\]
\[
n_7=M(L(M(R(n_6))))
\]
\[
n_8=M(M(R(n_7)))
\]
\[
n_9=M(M(n_8))
\]
\[
n_{10}=M(M(n_9))
\]
\[
n_{11}=M(L(M(R(n_{10}))))
\]
\[
n_{12}=M(M(n_{11}))
\]
\[
n_{13}=M(M(n_{12}))
\]
\[
n_{14}=M(M(n_{13}))
\]
\[
n_{15}=M(L(M(n_{14}))).
\]

The first exact closure claim to test is:

\[
n_{15}=n_0.
\]

---

## 10. Pathing traces to record

For each \(n_k\), record:

- full state \(n_k\)
- ambient landing \(\pi(n_k)\)
- register \(\rho(n_k)\)
- heading \(\eta(n_k)\)

This gives four synchronized traces:

1. full state trace
2. landing trace
3. register trace
4. heading trace

These traces are how we inspect whether pathing is genuinely coherent.

---

## 11. Minimal admissibility rules

For the initial test, use the following minimal admissibility policy:

- all states with \(v \in V\), \(\sigma \in \{0,1,2\}\), \(h \in \{0,1,2,3\}\) are admissible
- `left` and `right` are always defined
- `lift` is defined only when \(\sigma < 2\)
- `move` is defined only when the transition table contains an entry for \((\sigma,v,h)\)

This is deliberately strict.

Undefined transitions should be treated as failures, not patched informally.

---

## 12. What remains unspecified

The current note intentionally leaves one thing open:

\[
\mu_\sigma(v,h)
\]

That is the actual host motion law.

This is where the pathing thesis becomes concrete.

Until \(\mu_\sigma\) is defined, the operator system is only a scaffold.

Once \(\mu_\sigma\) is tabulated, the anchor walk can be executed exactly.

---

## 13. Immediate implementation target

The next concrete artifact should define a test transition dictionary.

Suggested structure:

- one chosen start vertex \(v_a\)
- one chosen start heading \(h_a\)
- a transition table for only the states touched by the anchor walk
- exact closure target \(n_{15}=n_0\)

This yields a minimal executable host witness before attempting a full G15 motion law.

---

## 14. Working interpretation

At this stage, the state model should be read as follows:

- \(V\) provides the rigid host places
- \(\Sigma\) provides layered or lifted registration
- \(H\) provides orientation
- \(L,R,U,M\) provide pathing
- the anchor walk is a candidate closed lawful word in this state grammar

So the immediate question is no longer vague.

It is:

> Can we define a deterministic `move` law on G15 states such that the proposed path closes exactly?

That is the first hard test.

