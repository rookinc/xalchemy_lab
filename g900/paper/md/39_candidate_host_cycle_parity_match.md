# Candidate Host-Cycle Parity Match

## Status
Working theorem-program note

## Purpose
Record the first successful match between:

- the explicit 15-step host-frame cycle,
- a concrete Hamiltonian realization of that cycle inside \(G_{15}\),
- and a cocycle-parity computation reproducing the sign-closing / identity-restoring law.

This is not yet the final theorem.
It is the first successful host-linked parity match.

---

## 1. The doctrine under test

The current locked cycle law is:

\[
n_{15}=-n_0,
\qquad
n_{30}=n_0.
\]

Interpretation:

- one full G15 cycle is sign-closing,
- two full G15 cycles restore identity.

The question is whether this law is realized by cocycle parity on an explicit host-linked loop in \(G_{15}\).

---

## 2. Canonical host-cycle candidate

The host-frame test example already fixes the 15-step walk

\[
v0 \to v1 \to v2 \to \cdots \to v14 \to v0.
\]

This is the strongest current candidate for the full host-frame G15 cycle.

To compare this with cocycle parity, the host cycle must be realized as a loop in \(G_{15}\cong L(\mathrm{Petersen})\).

---

## 3. Candidate Hamiltonian realization in \(G_{15}\)

A Hamiltonian-cycle search on \(G_{15}\) produced explicit 15-cycles. The first candidate used for testing was

\[
o0-o1-o2-o3-o4-s4-t2-s2-t0-s0-t3-s3-t1-t4-s1-o0.
\]

This gives the provisional host-to-\(G_{15}\) identification:

\[
v0\mapsto o0,
\quad
v1\mapsto o1,
\quad
v2\mapsto o2,
\quad
v3\mapsto o3,
\quad
v4\mapsto o4,
\]
\[
v5\mapsto s4,
\quad
v6\mapsto t2,
\quad
v7\mapsto s2,
\quad
v8\mapsto t0,
\quad
v9\mapsto s0,
\]
\[
v10\mapsto t3,
\quad
v11\mapsto s3,
\quad
v12\mapsto t1,
\quad
v13\mapsto t4,
\quad
v14\mapsto s1.
\]

This map is not yet claimed to be canonical.
It is a successful candidate realization.

---

## 4. Edge-label loop induced by the candidate

Under the explicit \(G_{15}\) edge ordering, the candidate Hamiltonian cycle translates to the loop

\[
(e1,e2,e3,e4,e10,e25,e18,e23,e16,e21,e19,e24,e30,e22,e11).
\]

So the host walk has now been translated into the edge-label language required by the cocycle parity probe.

This is the first host-linked edge-loop candidate currently available.

---

## 5. Cocycle support used in the probe

The first successful parity check used the cocycle support

\[
\{e1,e7,e12,e18,e24,e29\}.
\]

This support is a sample cocycle representative used for explicit testing.
It is not yet claimed to be the canonical representative attached to the actual signed lift.

---

## 6. Parity probe output

Running the parity probe on the candidate host-loop and the chosen cocycle support produced:

- one-cycle parity: \(1\),
- two-cycle parity: \(0\),
- one-cycle sheet effect: `flip`,
- two-cycle sheet effect: `restore`.

Equivalently, the probe returned:

\[
\text{one pass} \Rightarrow \text{odd parity} \Rightarrow \text{sheet flip},
\]
\[
\text{two passes} \Rightarrow \text{even parity} \Rightarrow \text{identity restoration}.
\]

This exactly matches the intended cycle doctrine.

---

## 7. What this establishes

This result establishes the following.

### 7.1
The host-frame walk can be realized concretely as a Hamiltonian loop in \(G_{15}\).

### 7.2
That loop can be translated into explicit \(G_{15}\) edge labels.

### 7.3
The cocycle-parity probe on that host-linked loop reproduces the sign-closing / identity-restoring pattern:

\[
n_{15}=-n_0,
\qquad
n_{30}=n_0.
\]

So the cycle doctrine is now connected to an explicit host-linked parity computation.

This is a substantial theorem-program advance.

---

## 8. What is still open

This note does **not** yet prove the final theorem.

Two canonicality questions remain open:

### 8.1 Host-cycle canonicity
Is the chosen Hamiltonian realization
\[
o0-o1-o2-o3-o4-s4-t2-s2-t0-s0-t3-s3-t1-t4-s1-o0
\]
the canonical realization of the host-frame cycle, or only one successful candidate among many?

### 8.2 Cocycle-representative canonicity
Is the support
\[
\{e1,e7,e12,e18,e24,e29\}
\]
the canonical cocycle representative relevant to the signed lift, or only a successful sample choice?

Until these are resolved, the result remains a candidate match rather than a theorem of uniqueness or inevitability.

---

## 9. Best current interpretation

The strongest honest reading is:

> a concrete Hamiltonian realization of the 15-step host cycle in \(G_{15}\), together with a concrete cocycle representative, yields parity behavior that exactly matches the sign-closing / identity-restoring law.

This is stronger than a toy existence check because the probe is now tied to the actual host-cycle candidate rather than to an unrelated sample loop.

---

## 10. Immediate next theorem tasks

The next tasks are now sharply defined.

### Task 10.1
Determine whether the chosen Hamiltonian host-cycle realization is canonical or one member of a family of equally valid host realizations.

### Task 10.2
Determine whether the cocycle support used in the successful probe is canonically induced by the actual signed lift.

### Task 10.3
Check whether the parity result is stable across all admissible representatives of the same switching class.

### Task 10.4
Check whether alternate host-cycle realizations produce the same parity law.

Only after these checks can the candidate match be promoted toward theorem-level status.

---

## 11. Working summary

The current theorem-program position is now:

- the host cycle is explicit,
- a Hamiltonian realization inside \(G_{15}\) is explicit,
- the resulting edge loop is explicit,
- and the cocycle parity on that explicit loop matches the G15/G30 sign law exactly.

In one line:

> the sign-closing doctrine now has a host-linked Hamiltonian-cycle parity match on \(G_{15}\), though canonicality of the cycle realization and cocycle representative remains open.

