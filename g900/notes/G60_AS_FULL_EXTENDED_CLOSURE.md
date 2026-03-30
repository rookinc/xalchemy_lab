# G60 as Full Extended Closure

## Status
Working note

## Core claim

If the state is extended to

\[
(x,\varepsilon,h,m)
\]

with:

- \(x\) = host placement
- \(\varepsilon \in \mathbb Z_2\) = sign
- \(h \in \mathbb Z_4\) = launch class
- \(m \in \mathbb Z_4\) = orthogonal stabilization phase

and the cycle law is

\[
\widehat W(x,\varepsilon,h,m)=
\bigl(x,-\varepsilon,\phi(h),\mu(h,m)\bigr)
\]

with Type III:

\[
\phi(0)=0,\quad \phi(2)=2,\quad \phi(1)=3,\quad \phi(3)=1
\]

and stabilization update

\[
\mu(h,m)=
\begin{cases}
m & h\in\{0,2\} \\
m+1 \pmod 4 & h\in\{1,3\},
\end{cases}
\]

then:

- one G15 cycle flips sign and advances orthogonal stabilization by one phase
- one G30 cycle restores walker state and launch class, but advances orthogonal stabilization by two phases
- one G60 cycle restores walker state, launch class, and orthogonal stabilization phase

So:

\[
G30 = \text{closure of the lower machine}
\]
\[
G60 = \text{first full closure of the extended machine}
\]

This is the first nontrivial higher-order closure law currently available.
