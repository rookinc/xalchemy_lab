# Exact Payload Branching and Punctured Branch Closure

## Status
Established from socket-neighborhood verification

## Purpose
Record the clearest current machine-level picture of the local frame-2 seam:

- at the exact payload \(t2\), the seam neighborhood opens into the full normalized Hamming-1 shell around the exact prototype;
- at punctured payloads, the seam neighborhood closes on the scaffold-preserving socket slice.

This note upgrades the local theory from a static slice description to a branching/closure picture.

---

## 1. Exact local machine state

The exact normalized frame-2 prototype is
\[
E_2=[o4,s0,t0,s2,t2,s4].
\]

In witness-assembly language:
\[
[W,X,Y,Z,T,I]=[o4,s0,t0,s2,t2,s4].
\]

Thus the exact local install condition is
\[
\operatorname{load}(\mathcal T)=t2,
\]
where \(\mathcal T=T\) is the socket.

---

## 2. Ambient shell

Let
\[
\Sigma_2^{\mathrm{full}}
\]
denote the full normalized frame-2 seam. This is the normalized Hamming-1 shell around \(E_2\), restricted to action-cell states with frame \(2\) among nearest action frames.

This shell decomposes into six coordinate slices
\[
\Sigma_2^{\mathrm{full}}=\bigsqcup_{j=0}^5 \Sigma_2^{(j)}.
\]

The distinguished scaffold-preserving punctured slice is
\[
\Sigma_2^{(4)}
=
\{[o4,s0,t0,s2,x,s4]: x\neq t2 \text{ and the state lies in the seam}\}.
\]

---

## 3. Exact payload neighborhood

Socket-neighborhood verification at the exact payload
\[
\operatorname{load}(\mathcal T)=t2
\]
yields:

- seam child count: \(47\),
- mismatch patterns relative to \(E_2\):
  \[
  [0],[1],[2],[3],[4],[5],
  \]
- the seam children therefore occupy all six coordinate directions of the ambient Hamming-1 shell.

### Proposition 3.1. Exact payload branching
At the exact socket payload \(t2\), the seam-to-seam local neighborhood opens into the full normalized Hamming-1 shell around \(E_2\).

### Interpretation
The exact installed state is the local branch point of the full seam shell.

---

## 4. Punctured payload neighborhoods

Socket-neighborhood verification at punctured payloads such as \(o4\) and \(t3\) yields:

- seam child count: \(9\),
- mismatch pattern relative to \(E_2\):
  \[
  [4]
  \]
  only,
- no child restores the exact payload \(t2\),
- no child leaves the scaffold-preserving socket slice.

### Proposition 4.1. Punctured branch closure
If
\[
\operatorname{load}(\mathcal T)\neq t2
\]
and the local state lies in the scaffold-preserving socket slice, then its seam-to-seam local neighborhood remains inside that same slice.

Equivalently, punctured payload neighborhoods are closed on the scaffold-preserving branch.

### Interpretation
Once the local machine leaves the exact payload, local seam evolution no longer branches through the full shell. It remains committed to the socket branch.

---

## 5. Branch-point formulation

The local frame-2 seam therefore has the following branching structure:

- the exact state \(E_2\) is the branch point,
- the full Hamming-1 shell opens at \(E_2\),
- the scaffold-preserving socket slice is one distinguished branch,
- once the socket payload is punctured away from \(t2\), local seam dynamics remain on that branch.

Thus the punctured slot-4 slice is not merely a subset of the seam shell. It is a dynamically closed branch of that shell rooted at the exact install state.

---

## 6. Assembly-level reading

In witness-assembly language:

- scaffold register:
  \[
  \mathcal S=(W,X,Y,Z,I)=(o4,s0,t0,s2,s4),
  \]
- socket:
  \[
  \mathcal T=T,
  \]
- exact payload:
  \[
  \operatorname{load}(\mathcal T)=t2.
  \]

Then:

- at exact payload, the neighborhood opens into the full shell,
- at punctured payload, the neighborhood closes on the socket branch.

So the socket branch is a closed payload family attached to the exact install point.

---

## 7. Consequence for the local theorem stack

The local theorem stack can now be read as:

1. the full frame-2 seam is the normalized Hamming-1 shell around \(E_2\),
2. the exact payload state is the branch point of that shell,
3. the scaffold-preserving socket slice is one distinguished branch,
4. punctured payloads remain on that branch under seam-to-seam local evolution,
5. the exact payload \(t2\) is absent from the punctured branch.

This is the cleanest current local machine picture.

---

## 8. What remains open

The local branching/closure structure is now clear.

The remaining question is not whether the punctured socket branch is locally closed. That is established.

The remaining question is:

> why does the larger retained dynamics generated from the locked witnesses enter and remain on this scaffold-preserving socket branch, rather than returning to the exact branch point or escaping through other nonlocal routes?

That is now the next structural frontier.

