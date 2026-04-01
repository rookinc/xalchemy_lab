# Local Machine Readout

## Status
Cockpit note

## Purpose
Provide the shortest operational readout of the local frame-2 obstruction theory in witness-assembly language.

This note is not for proof. It is for orientation.

---

## 1. Exact local machine state

The exact normalized frame-2 prototype is
\[
E_2=[o4,s0,t0,s2,t2,s4].
\]

In witness-assembly form:
\[
[W,X,Y,Z,T,I]=[o4,s0,t0,s2,t2,s4].
\]

So the exact local install condition is:

- socket position:
  \[
  T,
  \]
- exact payload:
  \[
  t2.
  \]

---

## 2. Assembly split

Define the scaffold register:
\[
\mathcal S=(W,X,Y,Z,I).
\]

Define the input socket:
\[
\mathcal T = T.
\]

Define the socket payload by
\[
\operatorname{load}(\mathcal T)=x.
\]

For the local frame-2 machine:

- the scaffold register is fixed,
- the input socket is fixed,
- only the socket payload varies.

Concretely,
\[
\mathcal S=(o4,s0,t0,s2,s4)
\]
is rigid.

---

## 3. Local seam family

The distinguished local seam slice is
\[
[W,X,Y,Z,T,I]=[o4,s0,t0,s2,x,s4]
\]
with
\[
x\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

So the local seam is the admissible payload family for the socket \(\mathcal T\):
\[
\operatorname{load}(\mathcal T)\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

The exact payload
\[
t2
\]
is missing.

---

## 4. What is rigid and what moves

Rigid scaffold:
\[
W=o4,\quad X=s0,\quad Y=t0,\quad Z=s2,\quad I=s4.
\]

Fixed socket:
\[
\mathcal T=T.
\]

Variable payload:
\[
\operatorname{load}(\mathcal T)=x.
\]

So the local obstruction is not scaffold drift and not socket loss. It is failure to realize the exact payload on an otherwise rigid scaffold with a live socket.

---

## 5. Edge readout

Primary hexagon:
\[
WXYZTIW.
\]

Perimeter edges:
\[
WX,\ XY,\ YZ,\ ZT,\ TI,\ IW.
\]

Rigid edges:
\[
WX,\ XY,\ YZ,\ IW.
\]

Variable edges:
\[
ZT,\ TI.
\]

So the local obstruction lives entirely in the socket sector.

---

## 6. Local dynamics

The seam-to-seam retained one-edit dynamics close on the admissible payload family.

So once the local machine is in the seam family, it stays in that family under local seam evolution.

Operationally:

- the scaffold register stays fixed,
- the socket stays live,
- the payload varies inside a closed alphabet,
- the exact payload never appears.

---

## 7. Ambient shell

The full normalized frame-2 seam is larger than this local family.

It is the normalized Hamming-1 shell around the exact prototype \(E_2\).

The local family studied here is one distinguished slice of that shell:
- the punctured slice,
- the scaffold-preserving slice,
- the socket-payload slice.

So the local machine readout is a readout of one special shell direction, not of the whole shell.

---

## 8. What is proved

Local proved facts:

1. the bounded locked regime never realizes the exact payload \(t2\),
2. the distinguished seam slice is exactly
   \[
   [o4,s0,t0,s2,x,s4],
   \]
3. seam-to-seam local dynamics close on this slice,
4. the scaffold register is rigid,
5. the socket is fixed,
6. only the payload varies.

---

## 9. What remains open

The main remaining local question is not what the seam family is.

That is known.

The remaining question is:

> why does the local machine expose exactly this payload alphabet at the socket, and why is the exact payload \(t2\) excluded?

Equivalently:

> why do the locked witness dynamics select and preserve this unique scaffold-preserving punctured socket slice of the full frame-2 Hamming shell?

That is the next structural frontier.

---

## 10. One-line machine summary

Fixed scaffold register:
\[
\mathcal S=(W,X,Y,Z,I)=(o4,s0,t0,s2,s4).
\]

Live socket:
\[
\mathcal T=T.
\]

Closed payload alphabet:
\[
\operatorname{load}(\mathcal T)\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

Exact payload would be:
\[
\operatorname{load}(\mathcal T)=t2.
\]

But that value is missing.

