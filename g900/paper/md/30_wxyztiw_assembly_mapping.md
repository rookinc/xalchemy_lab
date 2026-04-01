# WXYZTIW Assembly Mapping

## Status
Canonical interpretation note

## Purpose
Promote the preferred \(WXYZTIW\) witness language to the assembly layer of the local frame-2 obstruction theory.

This note defines the canonical mapping from normalized seam states to the witness-assembly representation and records the corresponding scaffold/defect semantics.

---

## 1. Motivation

The witness machine natively presents local states as normalized 6-cycles. For the distinguished frame-2 seam slice, the native machine form is
\[
[o4,s0,t0,s2,x,s4].
\]

This note declares the preferred hexagonal witness language
\[
WXYZTIW
\]
to be the assembly layer for that local theory.

Thus the machine-level cycle and the witness-level hexagon are treated as two representations of the same local object.

---

## 2. Canonical assembly map

Define the witness-assembly projection
\[
\Phi_{\mathrm{hex}}:\Sigma_2^{(4)}\to (W,X,Y,Z,T,I)
\]
by
\[
\Phi_{\mathrm{hex}}([o4,s0,t0,s2,x,s4])=(W,X,Y,Z,T,I)
\]
with
\[
W=o4,\quad X=s0,\quad Y=t0,\quad Z=s2,\quad T=x,\quad I=s4.
\]

Equivalently, for every state in the distinguished slot-4 slice,
\[
[W,X,Y,Z,T,I]=[o4,s0,t0,s2,x,s4].
\]

The corresponding closed witness word is
\[
WXYZTIW=[o4,s0,t0,s2,x,s4,o4].
\]

---

## 3. Exact prototype in assembly form

The normalized exact frame-2 prototype is
\[
E_2=[o4,s0,t0,s2,t2,s4].
\]

Under the assembly map this becomes
\[
[W,X,Y,Z,T,I]=[o4,s0,t0,s2,t2,s4].
\]

So exact frame-2 closure corresponds to the exact assembly install
\[
T=t2.
\]

---

## 4. Seam family in assembly form

The distinguished slot-4 slice is
\[
[o4,s0,t0,s2,x,s4],
\qquad
x\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

In assembly form this is:
\[
[W,X,Y,Z,T,I]=[o4,s0,t0,s2,x,s4],
\qquad
T\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

So the seam family is exactly the punctured \(T\)-family of the exact witness assembly, with \(T=t2\) missing.

---

## 5. Scaffold register and defect register

Define the scaffold register by
\[
\mathcal S=(W,X,Y,Z,I).
\]

For the distinguished frame-2 seam slice,
\[
\mathcal S=(o4,s0,t0,s2,s4)
\]
is rigid.

Define the defect register by
\[
\mathcal D=T.
\]

Then:

- the scaffold register is fixed,
- the defect register varies,
- exact closure is the install condition
  \[
  \mathcal D=t2.
  \]

So the local seam theory is naturally described as a fixed scaffold register plus a punctured defect register.

---

## 6. Edge semantics

The primary witness hexagon is
\[
WXYZTIW.
\]

Its perimeter edges are:
\[
WX,\ XY,\ YZ,\ ZT,\ TI,\ IW.
\]

On the distinguished seam slice:

- rigid edges:
  \[
  WX,\ XY,\ YZ,\ IW,
  \]
- variable edges:
  \[
  ZT,\ TI.
  \]

So the defect register \(T\) localizes the obstruction to the \(T\)-sector of the witness hexagon.

---

## 7. Diad/coupler interpretation

Using the preferred decomposition:

- diads:
  \[
  WX,\ YZ,\ TI,
  \]
- couplers:
  \[
  XY,\ ZT,\ IW,
  \]

the distinguished slot-4 seam slice has:

- frozen diads:
  \[
  WX,\ YZ,
  \]
- frozen couplers:
  \[
  XY,\ IW,
  \]
- variable sector:
  \[
  ZT,\ TI.
  \]

So the local obstruction is a one-sector install problem on an otherwise rigid witness assembly.

---

## 8. Assembly-level reading of the theorem stack

In witness-assembly language, the local theorem stack becomes:

1. the full normalized frame-2 seam is the ambient shell around the exact witness assembly,
2. the distinguished slot-4 slice is the unique scaffold-preserving punctured slice,
3. the scaffold register
   \[
   \mathcal S=(W,X,Y,Z,I)
   \]
   is fixed,
4. the defect register
   \[
   \mathcal D=T
   \]
   varies over the punctured alphabet
   \[
   \{o4,s0,s2,s3,s4,t0,t3,t4\},
   \]
5. exact closure would require
   \[
   \mathcal D=t2,
   \]
   but that value is missing,
6. the seam-to-seam retained dynamics close on this \(T\)-register family.

So the distinguished frame-2 seam is the dynamically closed punctured defect register of a primary witness assembly.

---

## 9. Working use

This note promotes \(WXYZTIW\) from informal metaphor to working assembly language for the local frame-2 obstruction theory.

Accordingly:

- machine-native form:
  \[
  [o4,s0,t0,s2,x,s4],
  \]
- assembly form:
  \[
  [W,X,Y,Z,T,I],
  \]
- structural read:
  fixed scaffold register \(\mathcal S\), punctured defect register \(\mathcal D\).

This is the preferred intermediate representation for future reasoning.

