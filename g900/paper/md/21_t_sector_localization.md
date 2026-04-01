# T-Sector Localization on the Frame-2 Seam

## Status
Working bridge note

## Purpose
Translate the frozen-five seam theorem into the preferred hexagonal witness language \(WXYZTIW\) and localize the obstruction to the \(T\)-sector.

---

## 1. Witness identification

Identify the normalized seam cycle
\[
[o4,s0,t0,s2,x,s4]
\]
with the hexagonal witness
\[
[W,X,Y,Z,T,I].
\]

Thus
\[
W=o4,\quad X=s0,\quad Y=t0,\quad Z=s2,\quad T=x,\quad I=s4.
\]

---

## 2. Frozen-five theorem in witness language

The retained frame-2 seam consists exactly of witnesses of the form
\[
WXYZTIW=[o4,s0,t0,s2,x,s4,o4]
\]
with
\[
x\in\{o4,s0,s2,s3,s4,t0,t3,t4\}.
\]

So \(W,X,Y,Z,I\) are rigid and only \(T\) varies.

---

## 3. Edge localization

Since only \(T\) varies, the only variable perimeter edges are the two incident to \(T\):
\[
ZT,\qquad TI.
\]

The other perimeter edges are rigid:
\[
WX,\qquad XY,\qquad YZ,\qquad IW.
\]

Thus the seam obstruction is localized to the \(T\)-sector.

---

## 4. Diad/coupler form

Using the preferred decomposition

- diads: \(WX,\ YZ,\ TI\),
- couplers: \(XY,\ ZT,\ IW\),

the retained seam has:

- frozen diads: \(WX,\ YZ\),
- frozen couplers: \(XY,\ IW\),
- variable sector: \(ZT,\ TI\).

So the obstruction is a one-sector installation problem.

---

## 5. Exact closure

The exact frame-2 prototype is
\[
[o4,s0,t0,s2,t2,s4].
\]

Hence exact closure corresponds to the special \(T\)-value
\[
T=t2.
\]

The retained seam realizes all observed admissible seam values of \(T\) except \(t2\).

Therefore the frame-2 obstruction is not global witness failure. It is failure to install the exact \(T\)-value on an otherwise rigid witness scaffold.

