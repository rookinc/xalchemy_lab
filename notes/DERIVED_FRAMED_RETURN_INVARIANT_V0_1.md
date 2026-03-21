# Derived Framed Return Invariant v0.1

## Goal

Replace the coarse framed return classifier based only on initial and final chart symbol with a derived invariant computed from the full chart trace.

## Chart trace

Let a loop produce a chart trace

\[
(c_1,\dots,c_n)
\]

where each \(c_k\) is either:

- `chart_left`
- `chart_right`

## Transition sign

Define the local transition sign

\[
\tau(c_k,c_{k+1})=
\begin{cases}
+1 & c_{k+1}=c_k\\
-1 & c_{k+1}\neq c_k
\end{cases}
\]

Interpretation:

- same chart symbol = +1
- chart flip = -1

## Framed return invariant

Define

\[
H(c_1,\dots,c_n)=\prod_{k=1}^{n-1}\tau(c_k,c_{k+1})
\]

This is the parity of chart flips along the trace.

## Interpretation

- \(H=+1\) means an even number of chart flips
- \(H=-1\) means an odd number of chart flips

So this gives a first derived framed return class.

## Check on current probes

### return_A
Trace:
- chart_right
- chart_left
- chart_right

Transitions:
- flip
- flip

So:
- \(H = (-1)(-1)=+1\)

### return_B
Trace:
- chart_left
- chart_right
- chart_left

Transitions:
- flip
- flip

So:
- \(H = (+1)\) after multiplication of two flips

### return_C
Trace:
- chart_right
- chart_right
- chart_right

Transitions:
- same
- same

So:
- \(H = (+1)(+1)=+1\)

### return_D
Trace:
- chart_right
- chart_left
- chart_left

Transitions:
- flip
- same

So:
- \(H = (-1)(+1)=-1\)

## Strongest conclusion

This derived invariant agrees with the current coarse return-class split:

- A, B, C belong to the \(H=+1\) class
- D belongs to the \(H=-1\) class

## Strongest sentence

The first derived framed return invariant is the parity of chart-coordinate flips along the transport trace.

## Next step

Upgrade the framed return probe so it computes and records:

- chart trace
- transition signs
- framed return invariant \(H\)

